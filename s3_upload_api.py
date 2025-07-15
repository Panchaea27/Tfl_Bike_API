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
            to_upload_file = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f))][0]
            to_upload_path = f'{directory}/{to_upload_file}'
            print(f'File identified: {to_upload_file}')
            try:
                bucket = os.getenv('AWS_BUCKET_NAME')
                s3_file = f'bike-point/{to_upload_file}'
                print(s3_file)
                s3_client = boto3.client(
                's3',
                aws_access_key_id = os.getenv("access_key"),
                aws_secret_access_key = os.getenv("secret_key")
                )
                print(s3_client)
                s3_client.upload_file(to_upload_path,bucket,s3_file)
                os.remove(f'{directory}/{to_upload_file}')
            except:
                 print('fail')
        except:
             print('file not found')
    else:
         print('connection failed')

upload_files('data')
