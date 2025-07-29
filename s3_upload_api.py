import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv
import os

load_dotenv()

def test_connection():
    try:
        sts = boto3.client(
                'sts',
                aws_access_key_id = os.getenv("access_key"),
                aws_secret_access_key = os.getenv("secret_key"),
                region_name=os.getenv("region")
                )
        response = sts.get_caller_identity()
        return True    
    except (NoCredentialsError, ClientError) as e:
            print(f"Connection failed: {e}")
            return False


def upload_files(directory:str):
    if test_connection():
        try:
            # now building a list of all files in directory
            to_upload_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]  # replaced single file selection with list of all files

            if not to_upload_files:
                print('No files found in directory')  #  handle case where directory is empty
                return

            for to_upload_file in to_upload_files:  # loop through all files instead of just one
                to_upload_path = os.path.join(directory, to_upload_file)  # use os.path.join for portability
                print(f'Uploading file: {to_upload_file}')

                try:
                    bucket = os.getenv('AWS_BUCKET_NAME')
                    s3_file = f'bike-point/{to_upload_file}'
                    s3_client = boto3.client(
                        's3',
                        aws_access_key_id = os.getenv("access_key"),
                        aws_secret_access_key = os.getenv("secret_key")
                    )
                    s3_client.upload_file(to_upload_path, bucket, s3_file)
                    print(f'Successfully uploaded {to_upload_file} to {bucket}/{s3_file}')  # more informative success log
                    os.remove(to_upload_path)  # use full path to delete file after upload
                except Exception as e:  # show actual exception to aid debugging
                    print(f'Failed to upload {to_upload_file}: {e}')
        except Exception as e:  # show actual exception to aid debugging
            print(f'Error accessing directory or reading files: {e}')
    else:
        print('connection failed')

upload_files('data')