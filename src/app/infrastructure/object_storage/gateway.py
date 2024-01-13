import io

import aioboto3
from types_aiobotocore_s3.service_resource import Bucket, S3ServiceResource
from types_aiobotocore_s3.client import S3Client

from src.app.infrastructure.base import AIOBotoGateway


class ObjectStorageGatewayImpl(AIOBotoGateway):
    def __init__(
            self,
            session: aioboto3.Session,
            bucket_name: str,
            endpoint_url: str | None = None,
    ) -> None:
        super().__init__(session=session)
        self.bucket_name = bucket_name
        self.bucket: Bucket | None = None

        self._endpoint_url = endpoint_url

    @property
    def s3_resource_context(self) -> S3ServiceResource:
        return self.session.resource(service_name="s3", endpoint_url=self._endpoint_url)  # type: ignore

    @property
    def s3_client_context(self) -> S3Client:
        return self.session.client(service_name="s3")  # type: ignore

    async def upload_file(self, file_path: str, name: str) -> None:
        async with self.s3_resource_context as s3_resource:
            self.bucket = await s3_resource.Bucket(self.bucket_name)
            await self.bucket.upload_file(Filename=file_path, Key=name)

    async def upload_file_object(self, file_object: io.BytesIO, name: str) -> None:
        async with self.s3_resource_context as s3_resource:
            self.bucket = await s3_resource.Bucket(self.bucket_name)
            await self.bucket.upload_fileobj(Fileobj=file_object, Key=name)

    async def delete_object(self, name: str) -> None:
        async with self.s3_resource_context as s3_resource:
            self.bucket = await s3_resource.Bucket(self.bucket_name)
            await self.bucket.objects.filter(Prefix=name).delete()

    async def delete_all_objects(self) -> None:
        async with self.s3_resource_context as s3_resource:
            self.bucket = await s3_resource.Bucket(self.bucket_name)
            await self.bucket.objects.all().delete()

    async def get_file_presigned_url(self, name: str, expires_in: int = 3_600) -> str:
        async with self.s3_client_context as s3_client:
            return await s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": name},
                ExpiresIn=expires_in,
            )

    async def get_file_object(self, name: str) -> io.BytesIO:
        async with self.s3_resource_context as s3_resource:
            bytes_io = io.BytesIO()
            self.bucket = await s3_resource.Bucket(self.bucket_name)
            await self.bucket.download_fileobj(Key=name, Fileobj=bytes_io)
            bytes_io.seek(0)
            return bytes_io
