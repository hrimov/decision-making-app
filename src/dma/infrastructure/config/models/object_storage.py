from dataclasses import dataclass


@dataclass
class ObjectStorageConfig:
    access_key: str
    secret_key: str
    bucket_name: str
