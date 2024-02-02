import base64
import uuid

from dotenv import load_dotenv

load_dotenv()

import boto3
import os
from botocore.exceptions import ClientError


class FileFolder:

    @classmethod
    def school(cls, name):
        return f"{name}/profile"

    @classmethod
    def student_profile(cls, school_name, email):
        return f"{school_name}/students/{email}/profile"

    @classmethod
    def admin_profile(cls, email):
        return f"admins/{email}"

    @classmethod
    def student_file(cls, school_name, email):
        file_name = f"file-{str(uuid.uuid4())[:8]}"
        return f"{school_name}/students/{email}/{file_name}", file_name

    @classmethod
    def project_file(cls, school_name, project_name):
        file_name = f"project-{str(uuid.uuid4())[:8]}"
        return f"{school_name}/projects/{project_name}/{file_name}", file_name

    @classmethod
    def learning_group_file(cls, school_name, learning_group_name):
        file_name = f"learning_group-{str(uuid.uuid4())[:8]}"
        return f"{school_name}/learning_group/{learning_group_name}/{file_name}", file_name


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
    def upload_file(cls, file, file_path):

        try:
            # Check if the prefix 'data:image/jpeg;base64,' exists in the string
            if file.startswith("data:image/jpeg;base64,"):
                image_type = file.split(';')[0].split(':')[1]
                base64_encoded_data = file.split(',', 1)[1]
            else:
                image_type = 'image/jpeg'
                base64_encoded_data = file

            decoded_image_data = base64.b64decode(base64_encoded_data)
            cls.s3.put_object(
                Bucket=cls.bucket_name,
                Key=file_path,
                Body=decoded_image_data,
                ContentType=str(image_type)  # Specify the content type as needed
            )

            # Generate a pre-signed URL for the uploaded image
            image_url = cls.get_file_url(str(file_path))
            return image_url
        except Exception as e:
            print(f"Failed to upload image: {e}")
            return None

    @classmethod
    def get_file_url(cls, file_name):
        try:

            response = cls.s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': cls.bucket_name,
                    'Key': file_name,
                },
                ExpiresIn=3600
            )
            return response
        except ClientError as e:
            print(f"Failed to generate URL: {e}")
            return None

    @classmethod
    def delete_file(cls, file_name):
        try:
            cls.s3.delete_object(Bucket=cls.bucket_name, Key=file_name)
            return True
        except ClientError as e:
            print(f"Deletion failed: {e}")
            return False

    @classmethod
    def update_file(cls, file, file_name):
        # Deleting the old file and uploading the updated one
        if cls.delete_file(file_name):
            return cls.upload_file(file, file_name)
        else:
            return False
