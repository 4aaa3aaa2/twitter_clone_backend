from google.cloud import storage
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\\Users\\mingzhi.huang\\Downloads\\twitter-clone-4aaa3aaa2-1e904d71ca87.json"
client = storage.Client()
bucket_name = "twitter_clone_4aaa3aaa2"
bucket = client.bucket(bucket_name)

print("Bucket exists:", bucket.exists())
