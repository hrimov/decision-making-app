import io
import tempfile
from urllib.parse import urlparse

import pytest
import pytest_asyncio

from src.app.infrastructure.object_storage.gateway import ObjectStorageGatewayImpl


@pytest.mark.order("first")
async def test_upload_file_object(
        object_storage_gateway: ObjectStorageGatewayImpl,
        file_object_to_upload: io.BytesIO,
):
    await object_storage_gateway.upload_file_object(
        file_object=file_object_to_upload,
        name="some_binary_file.format",
    )


@pytest.mark.order("second")
async def test_upload_file(
        object_storage_gateway: ObjectStorageGatewayImpl,
        file_to_upload: tempfile._TemporaryFileWrapper,
):
    await object_storage_gateway.upload_file(
        file_path=file_to_upload.name,
        name="some_binary_file.format",
    )


@pytest.mark.order(3)
async def test_get_file_object(
        object_storage_gateway: ObjectStorageGatewayImpl,
        file_object_to_upload: io.BytesIO,
):
    await object_storage_gateway.upload_file_object(
        file_object=file_object_to_upload,
        name="some_binary_file.format",
    )
    file_obj = await object_storage_gateway.get_file_object(
        "some_binary_file.format",
    )
    assert file_obj.getbuffer().nbytes > 0
    assert file_obj.getbuffer().nbytes == file_object_to_upload.getbuffer().nbytes


@pytest.mark.order(4)
async def test_get_file(
        object_storage_gateway: ObjectStorageGatewayImpl,
        file_to_upload: tempfile._TemporaryFileWrapper,
):
    await object_storage_gateway.upload_file(
        file_path=file_to_upload.name,
        name="some_binary_file.format",
    )
    file_presigned_url = await object_storage_gateway.get_file_presigned_url(
        "some_binary_file.format",
    )
    try:
        parsed_url = urlparse(file_presigned_url)
        is_valid_url = all([parsed_url.scheme, parsed_url.netloc])
    except ValueError:
        is_valid_url = False
    assert is_valid_url
