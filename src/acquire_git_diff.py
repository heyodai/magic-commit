"""
We found an excellent GitHub commit dataset on Kaggle. However, it doesn't list what each commit actually changed.

Fortunately, it looks like this can be done via the GitHub API.

@see https://github.com/heyodai/magic-commit/issues/1
"""
import pandas as pd
import requests
import logging
import time
import pickle
import sqlite3
import os
from rich import print
from dotenv import load_dotenv

GITHUB_API_TOKEN = os.environ['GITHUB_API_TOKEN']

def main():
    # Set up logging
    epoch = int(time.time())
    logging.basicConfig(
        filename='logs/{}_acquire_git_diff.log'.format(epoch),
        filemode='w',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    log = logging.getLogger(__name__)

    # Load the current_row variable from the pickle file
    try:
        with open('data/current_row.pickle', 'rb') as f:
            current_row = pickle.load(f)
    except FileNotFoundError:
        current_row = 0

    # Load the sqlite3 database connection
    con = sqlite3.connect("data/git_diff.db")
    cur = con.cursor()

    # Create the raw table if it doesn't exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS raw (
        rowid INTEGER PRIMARY KEY,
        commit_hash TEXT,
        author TEXT,
        date TEXT,
        message TEXT,
        repo TEXT,
        additions INTEGER, 
        deletions INTEGER,
        files_changed INTEGER,
        patch TEXT
    )
    """)

    # Load the dataset from Kaggle
    df = pd.read_csv('data/full.csv')
    length = len(df)

    # Loop through each commit and get the diff for it
    for index, row in df[current_row:].iterrows():
        # Log the current row
        log.info('Processing row {} of {}'.format(index, length))
        print('Processing row {} of {}'.format(index, length))

        # Safety check to make sure we don't process the same row twice
        # This should never happen, but just in case
        if current_row > index:
            log.info('Skipping row {} as it has already been processed'.format(index))
            print('Skipping row {} as it has already been processed'.format(index))
            continue

        commit = row['commit']
        repo = row['repo']
        author = row['author']
        date = row['date']
        message = row['message']

        # Get the diff
        try:
            authorization = f'token {GITHUB_API_TOKEN}'
            headers = {
                "Accept": "application/vnd.github.v3+json",
                "Authorization" : authorization,
            }
            r = requests.get('https://api.github.com/repos/{}/commits/{}'.format(repo, commit), headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            log.error('Error getting diff for commit {}: {}'.format(commit, err))
            print('Error getting diff for commit {}: {}'.format(commit, err))
            exit(1)

        additions = 0
        deletions = 0
        files_changed = 0
        patch = ''
        for file in r.json()['files']:
            additions = additions + file['additions']
            deletions = deletions + file['deletions']
            files_changed = files_changed + file['changes']
            if 'patch' in file:
                patch = patch + file['patch']

        # Insert the row into the database
        cur.execute("INSERT OR REPLACE INTO raw VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
            index,
            commit, 
            author, 
            date, 
            message, 
            repo, 
            additions, 
            deletions, 
            files_changed, 
            patch
            )
        )

        # Save the current row to a pickle file
        with open('data/current_row.pickle', 'wb') as f:
            pickle.dump(index, f)

        # Commit the changes to the database
        con.commit()

        # Sleep for 1 second to avoid rate limiting
        time.sleep(1)

        # If we've reached the end of the dataset, write database to csv file
        if index == length - 1:
            log.info('Writing database to csv file')
            print('Writing database to csv file')
            df = pd.read_sql_query("SELECT * FROM raw", con)
            df.to_csv('data/git_diff.csv', index=False)

    # Close the database connection
    con.close()