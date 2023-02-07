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
from rich import print
from dotenv import dotenv_values

# Set up logging
epoch = int(time.time())
logging.basicConfig(
    filename='logs/{}_acquire_git_diff.log'.format(epoch),
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)

"""
The dataset from Kaggle is available here: https://www.kaggle.com/datasets/dhruvildave/github-commit-messages-dataset

The dataset is a CSV file with the following columns:
- commit: The commit hash
- author: The author of the commit
- date: The date of the commit
- message: The commit message
- repo: The repository name
"""
df = pd.read_csv('data/full.csv')
length = len(df)

"""
Now, let's loop through each commit and get the diff for it.

The GitHub API format is as follows:

    https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}
"""
for index, row in df.iterrows():
    # Check if current_row.pickle exists
    # If it does, start from there
    try:
        with open('data/current_row.pickle', 'rb') as f:
            current_row = pickle.load(f)
            if current_row > index:
                continue
    except FileNotFoundError:
        current_row = 0

    # Print the progress
    message = """
    Processing {}/{} rows
    commit {} for repo {}
    """.format(index + 1, length, row['commit'], row['repo'])

    print(message)
    log.info(message)

    # Set up the necessary variables for the API call
    url = 'https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}'.format(
        owner=row['repo'].split('/')[0],
        repo=row['repo'].split('/')[1],
        commit_sha=row['commit']
    )
    auth_token = dotenv_values()['GITHUB_TOKEN']
    headers = {
        "Authorization": "token {}".format(auth_token),
        "Accept": "application/vnd.github.v3+json",
    }

    # Make the API call
    response = requests.get(
        url, 
        headers=headers
    )
    if response.status_code != 200:
        print('Error: {}'.format(response.status_code))
        break

    # Set the diff values
    df.at[index, 'additions'] = 0
    df.at[index, 'deletions'] = 0
    df.at[index, 'files_changed'] = 0
    df.at[index, 'patch'] = ''

    # Loop through each file and add the diff values
    for file in response.json()['files']:
        df.at[index, 'additions'] = df.at[index, 'additions'] + file['additions']
        df.at[index, 'deletions'] = df.at[index, 'deletions'] + file['deletions']
        df.at[index, 'files_changed'] = df.at[index, 'files_changed'] + file['changes']

        # The 'patch' field won't exist for binary files
        if 'patch' in file:
            df.at[index, 'patch'] = df.at[index, 'patch'] + file['patch']

    # Increment and then pickle the current_row variable
    current_row = index
    with open('data/current_row.pickle', 'wb') as f:
        pickle.dump(current_row, f)

df.to_csv('data/full_with_diff.csv', index=False)

def main():
    pass

def extract_raw_to_db():
    pass

def load_db():
    pass

def save_db():
    pass