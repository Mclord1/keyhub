import base64

from dotenv import load_dotenv

load_dotenv()

import boto3
import os
from botocore.exceptions import ClientError


class FileFolder:
    school = "school"
    teacher = f"{school}/teacher"
    student = f"{school}/student"
    parent = f"{school}/parent"
    learning_group = f"{school}/learning_group"
    project = f"{school}/project"
    message = f"{school}/message"


class FileHandler:
    aws_access_key = os.environ.get("AWS_ACCESS_KEY")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS")
    bucket_name = "keyhub-folder"
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )

    @classmethod
    def validate_image(cls, image):
        try:
            decoded_data = base64.b64decode(image)
            return True
        except Exception as e:
            raise e

    @classmethod
    def upload_file(cls, file, folder, file_name):

        try:
            # Check if the prefix 'data:image/jpeg;base64,' exists in the string
            if file.startswith("data:image/jpeg;base64,"):
                image_type = file.split(';')[0].split(':')[1]
                base64_encoded_data = file.split(',', 1)[1]
            else:
                image_type = 'image/jpeg'
                base64_encoded_data = file


            decoded_image_data = base64.b64decode(base64_encoded_data)
            _file_name = f"{folder}/{file_name}"
            cls.s3.put_object(
                Bucket=cls.bucket_name,
                Key=_file_name,
                Body=decoded_image_data,
                ContentType=str(image_type)  # Specify the content type as needed
            )

            # Generate a pre-signed URL for the uploaded image
            image_url = cls.get_file_url(folder, str(file_name))
            return image_url
        except Exception as e:
            print(f"Failed to upload image: {e}")
            return None

    @classmethod
    def get_file_url(cls, folder, file_name):
        try:
            _file_name = f"{folder}/{file_name}"

            response = cls.s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': cls.bucket_name,
                    'Key': _file_name,
                }
            )
            return response
        except ClientError as e:
            print(f"Failed to generate URL: {e}")
            return None

    @classmethod
    def delete_file(cls, folder, file_name):
        try:
            _file_name = f"{folder}/{file_name}"
            cls.s3.delete_object(Bucket=cls.bucket_name, Key=_file_name)
            return True
        except ClientError as e:
            print(f"Deletion failed: {e}")
            return False

    @classmethod
    def update_file(cls, file, folder, file_name):
        # Deleting the old file and uploading the updated one
        if cls.delete_file(folder, file_name):
            return cls.upload_file(file, folder, file_name)
        else:
            return False
