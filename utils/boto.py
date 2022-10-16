from decouple import config
import boto3


def boto_client():

    # set the Amazon S3 Client
    client = boto3.client('s3',
        aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
        )

    return client

def put_aws_object(bucket,key,file):

    client = boto_client()

    # we do not have ACL = public-read here because
    # this folder is locked down in AWS
    bucket = client.put_object(
        Bucket = bucket,
        Body = file,
        Key = key
    )

    # ContentType = file.content_type,

def delete_aws_object(bucket,key):

    client = boto_client()

    # delete the S3 object
    client.delete_object(
        Bucket = bucket,
        Key = key
    )
