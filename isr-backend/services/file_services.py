import logging
import boto3
from botocore.exceptions import ClientError
import os

ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")

s3_client = boto3.client(
        "s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY
    )

def upload_file(file, bucket, file_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    try:
        s3_client.upload_fileobj(
        file,
        bucket,
        file_name,
        ExtraArgs={'Metadata': {'ContentType': 'image/png'}}
    )

    except ClientError as e:
        logging.error(e)
        return False
    return True


def fetch_file(object_key):
    try:
        response_content_disposition = 'inline'
        response = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={"Bucket": "spm-proj-bucket", "Key": object_key, 
                    "ResponseContentDisposition": response_content_disposition,
                    "ResponseContentType": "image/png"},
            ExpiresIn=60000,
        )
        return response
    
    except Exception as e:
        logging.error(e)
        return False
    

def key_exists(key):
    try:
        s3_client.head_object(Bucket= "spm-proj-bucket", Key=key)
        print(f"Key: '{key}' found!")
        return True
    except Exception as e:
        if e.response["Error"]["Code"] == "404":
            print(f"Key: '{key}' does not exist!")
        else:
            print("Something else went wrong")
        return False