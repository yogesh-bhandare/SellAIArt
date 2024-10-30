from decouple import config

# AWS S3 settings
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default=None)
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default=None)
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", default="sellaiart")
AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME", default=None)
AWS_S3_ENDPOINT_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"


# Default storage settings
DEFAULT_FILE_STORAGE = "home.storages.backends.MediaStorage"
STATICFILES_STORAGE = "home.storages.backends.StaticFileStorage"

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME
        },
    },
    "staticfiles": {
        "BACKEND": "home.storages.backends.StaticFileStorage",
    },
    "mediafiles": {
        "BACKEND": "home.storages.backends.MediaStorage",
    },
}
