from minio import Minio
from minio.error import MinioException

from app.settings.base import minio_settings


bucket_name = minio_settings.s3_bucket_name


class S3Exception(MinioException):
    """Base exception"""


storage = Minio(
    minio_settings.s3_endpoint,
    access_key=minio_settings.s3_access_key,
    secret_key=minio_settings.s3_secret_key,
    region=minio_settings.s3_region,
    secure=minio_settings.s3_secure,
)
