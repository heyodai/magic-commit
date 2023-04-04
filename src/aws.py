"""
This script either uploads or downloads data between the /data folder and an S3 bucket.
"""
import boto3
import os
# from dotenv import dotenv_values

def upload():
    """
    Upload contents of the /data folder to an S3 bucket.
    """
    # Set up the S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )

    # Upload the files
    for file in os.listdir('data'):
        s3.upload_file('data/{}'.format(file), 'magic-commit-aw', 'data/{}'.format(file))

def download():
    """
    Download contents of an S3 bucket to the /data folder.
    """
    # Set up the S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )

    # Download the files
    for file in os.listdir('data'):
        s3.download_file('magic-commit-aw', 'data/{}'.format(file), 'data/{}'.format(file))