import io
import os
import tempfile
from typing import AsyncGenerator, Generator

import aioboto3
import pytest
import pytest_asyncio
from testcontainers.minio import MinioContainer  # type: ignore[import-untyped]

from dma.infrastructure.object_storage.gateway import ObjectStorageGatewayImpl


BUCKET_NAME: str = "bucket-name"


@pytest.fixture(scope="session")
def minio_container() -> Generator[MinioContainer, None, None]:
    minio_container = MinioContainer(
        access_key="access_key",
        secret_key="secret_key",
    )
    if os.name == "nt":  # Note: from testcontainers/testcontainers-python#108
        minio_container.get_container_host_ip = lambda: "localhost"
    try:
        minio_container.start()
        minio_container.get_container_host_ip()
        minio_client = minio_container.get_client()
        minio_client.make_bucket(BUCKET_NAME)
        yield minio_container
    finally:
        minio_container.stop()


# noinspection PyUnusedLocal
@pytest_asyncio.fixture()
async def aioboto_session(
        minio_container: MinioContainer,
) -> AsyncGenerator[aioboto3.Session, None]:
    yield aioboto3.Session(
        aws_access_key_id="access_key",
        aws_secret_access_key="secret_key",
        aws_session_token=None,
    )


@pytest_asyncio.fixture()
async def object_storage_gateway(
        minio_container: MinioContainer,
        aioboto_session: aioboto3.Session,
) -> AsyncGenerator[ObjectStorageGatewayImpl, None]:
    host_ip = minio_container.get_container_host_ip()
    port = minio_container.get_exposed_port(minio_container.port_to_expose)
    gateway = ObjectStorageGatewayImpl(
        session=aioboto_session,
        bucket_name=BUCKET_NAME,
        endpoint_url=f"http://{host_ip}:{port}",
    )
    yield gateway
    # objects cleanup
    minio_client = minio_container.get_client()
    objs = minio_client.list_objects(bucket_name=BUCKET_NAME)
    minio_client.remove_objects(bucket_name=BUCKET_NAME, delete_object_list=objs)


@pytest.fixture()
def file_object_to_upload() -> io.BytesIO:
    return io.BytesIO(b"Some binary data")


# noinspection PyProtectedMember
@pytest.fixture()
def file_to_upload() -> Generator[tempfile._TemporaryFileWrapper, None, None]:
    with tempfile.NamedTemporaryFile(delete=False, mode="wb") as file:
        file.write(b"Some binary data")
        file.close()
        yield file
