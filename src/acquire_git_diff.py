from github import Github
import pandas as pd
import os
import logging
import time
import pickle
import sqlite3

token = os.environ.get("GITHUB_API_TOKEN")
g = Github(token)

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

# Create the tables if they don't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS commits (
    rowid INTEGER PRIMARY KEY,
    commit_hash TEXT,
    author TEXT,
    date TEXT,
    message TEXT,
    repo TEXT
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS diff (
    additions INTEGER, 
    deletions INTEGER,
    filename INTEGER,
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
    repo = g.get_repo(repo)
    commit = repo.get_commit(commit)

    for file in commit.files:
        additions = file.additions
        deletions = file.deletions
        filename = file.filename
        patch = file.patch

        # store this data in a new table in your database
        cur.execute("""
        INSERT INTO diff (additions, deletions, filename, patch)
        VALUES (?, ?, ?, ?)
        """, (additions, deletions, filename, patch))

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