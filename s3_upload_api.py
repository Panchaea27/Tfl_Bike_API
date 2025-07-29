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
            #now filters to only include .json files
            to_upload_files = [f for f in os.listdir(directory)
                               if os.path.isfile(os.path.join(directory, f)) and f.endswith('.json')]  #  added .endswith('.json') filter

            if not to_upload_files:
                print('No .json files found in directory')  
                return

            for to_upload_file in to_upload_files:
                to_upload_path = os.path.join(directory, to_upload_file)
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
                    print(f'Successfully uploaded {to_upload_file} to {bucket}/{s3_file}')
                    os.remove(to_upload_path)
                except Exception as e:
                    print(f'Failed to upload {to_upload_file}: {e}')
        except Exception as e:
            print(f'Error accessing directory or reading files: {e}')
    else:
        print('connection failed')

upload_files('data')
