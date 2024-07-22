from dotenv import load_dotenv
import os

load_dotenv()

MY_IPS = os.getenv("MY_IPS")
HOST = os.getenv("DB_HOST")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
NAME = os.getenv("DB_NAME")
S3_BUCKET = os.getenv("S3_BUCKET")
CLOUDFRONT_URL = os.getenv("CLOUDFRONT_URL")
