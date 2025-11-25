'''
from google.cloud import storage
from flask import current_app
from typing import IO


class CloudStorageService:
    def __init__(self):
        # Create a Google Cloud Storage client
        # It uses GOOGLE_APPLICATION_CREDENTIALS env var for authentication
        self.client: storage.Client = storage.Client()
        self.bucket_name: str = current_app.config["GCS_BUCKET"]

    def upload(self, file_name: str, file_stream: IO[bytes], content_type: str) -> str:
        """
        Upload a file to Google Cloud Storage and return its public URL.

        :param file_name: Name of the file in the bucket
        :param file_stream: Stream of the file (e.g., Flask FileStorage)
        :param content_type: MIME type (e.g., 'image/jpeg')
        :return: Public URL of the uploaded file
        """
        # Get the bucket
        bucket = self.client.bucket(self.bucket_name)

        # Create a blob (represents the file in the bucket)
        blob = bucket.blob(file_name)

        # Upload from stream
        blob.upload_from_file(file_stream, content_type=content_type)

        # Make file publicly accessible (optional)
        blob.make_public()

        # Return the public URL
        return f"https://storage.googleapis.com/{self.bucket_name}/{file_name}"

'''
from google.cloud import storage
from flask import current_app
import os
from typing import IO, Optional


class CloudStorageService:
    def __init__(self, bucket_name: Optional[str] = None, make_public: bool = False):
        """
        Hybrid version:
        - Reads bucket name from Flask config if available, otherwise from env var.
        - Allows optional control over public/private file access.

        :param bucket_name: Explicit bucket name (overrides config/env if provided)
        :param make_public: Whether to make uploaded files publicly accessible
        """
        self.client: storage.Client = storage.Client()

        # Prefer explicit bucket_name, then Flask config, then environment variable
        if bucket_name:
            self.bucket_name = bucket_name
        else:
            try:
                self.bucket_name = current_app.config["GCS_BUCKET"]
            except RuntimeError:
                # current_app not available (outside Flask context)
                self.bucket_name = os.getenv("GCS_BUCKET")

        self.make_public = make_public

    def upload(self, file_name: str, file_stream: IO[bytes], content_type: str) -> str:
        """
        Upload a file to Google Cloud Storage.

        :param file_name: Name of the file in the bucket
        :param file_stream: File-like object (e.g., Flask FileStorage.stream)
        :param content_type: MIME type of the file
        :return: Public or signed URL of the uploaded file
        """
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(file_name)

        blob.upload_from_file(file_stream, content_type=content_type)

        if self.make_public:
            blob.make_public()
            return blob.public_url
        else:
            # Return a signed URL valid for 1 hour (example)
            return blob.generate_signed_url(expiration=3600)