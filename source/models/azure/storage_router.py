import shutil
from datetime import datetime, timedelta
import base64
from pathlib import Path

from azure.storage.blob import BlobServiceClient
from azure.storage.blob import generate_blob_sas, AccountSasPermissions
import os, uuid
import backoff

from config.backoffConf import backoff_cnf
from config.circuitConf import circuit_conf
from circuitbreaker import circuit
from utils.handlers import backoff_handlers, circuit_handlers
from config.loggingConf import LogConfig

from source.models.auth.auth_controller import logger, get_user
from config.appConf import Settings
from fastapi import APIRouter, HTTPException, Depends, Request

storageRouter = APIRouter(
    tags=["Azure Storage functionality"
          ])


@storageRouter.post("/image")
@backoff.on_exception(backoff.expo,
                      HTTPException,
                      max_tries=backoff_cnf.MAX_RETRIES,
                      on_backoff=backoff_handlers.backoff_hdlr,
                      logger=logger
                      )
# TODO FIX UNAUTHORIZED (?)
async def upload_image(image_base64: str, request: Request, user=Depends(get_user)):
    account_name = Settings.AZURE_CLOUD_STORAGE_NAME
    account_key = Settings.AZURE_CLOUD_STORAGE_KEY
    print(request.headers)
    print(request.body())
    print(request.client)

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(Settings.AZURE_CLOUD_STORAGE_CONNECTION_STRING)
    # Create a unique name for the container
    container_name = user['uid'].lower()

    if blob_service_client.get_container_client(container_name):
        container_client = blob_service_client.get_container_client(container_name)
    else:
        # Create the container
        container_client = blob_service_client.create_container(container_name)

    # Create a local directory to hold blob data
    local_path = os.path.dirname(Path(__file__).parent) + '/files'
    os.mkdir(local_path)

    # Create a file in the local data directory to upload and download
    local_file_name = str(uuid.uuid4()) + ".jpg"
    upload_file_path = os.path.join(local_path, local_file_name)
    logger.debug(upload_file_path)

    with open(upload_file_path, "wb") as fh:
        fh.write(base64.decodebytes(str.encode(image_base64)))

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    # Upload the created file
    with open(upload_file_path, "rb") as data:
        blob_client.upload_blob(data)

    shutil.rmtree(local_path, ignore_errors=True)

    blob_name = local_file_name
    logger.debug(blob_name)

    url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}"
    sas_token = generate_blob_sas(
        account_name=account_name,
        account_key=account_key,
        container_name=container_name,
        blob_name=blob_name,
        permission=AccountSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )

    url_with_sas = f"{url}?{sas_token}"
    logger.debug(url_with_sas)

    return {"detail": url_with_sas}


@storageRouter.get("/image")
@backoff.on_exception(backoff.expo,
                      HTTPException,
                      max_tries=backoff_cnf.MAX_RETRIES,
                      on_backoff=backoff_handlers.backoff_hdlr,
                      logger=logger
                      )
async def list_images(user=Depends(get_user)):
    account_name = Settings.AZURE_CLOUD_STORAGE_NAME
    account_key = Settings.AZURE_CLOUD_STORAGE_KEY

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(Settings.AZURE_CLOUD_STORAGE_CONNECTION_STRING)
    # Create a unique name for the container
    container_name = user['uid'].lower()

    if blob_service_client.get_container_client(container_name):
        container_client = blob_service_client.get_container_client(container_name)
    else:
        # Create the container
        container_client = blob_service_client.create_container(container_name)

    url_list = []
    blob_list = container_client.list_blobs()
    for blob_name in blob_list:
        url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name.name}"
        sas_token = generate_blob_sas(
            account_name=account_name,
            account_key=account_key,
            container_name=container_name,
            blob_name=blob_name.name,
            permission=AccountSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )

        url_with_sas = f"{url}?{sas_token}"
        logger.debug(url_with_sas)
        url_list.append(url_with_sas)

    return {"detail": url_list}
