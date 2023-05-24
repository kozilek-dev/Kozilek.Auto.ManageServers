import logging
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobType, StorageStreamDownloader
from dotenv import load_dotenv
from os import getenv
from typing import Optional

load_dotenv()


class Storage:
    __instance: Optional[ContainerClient] = None
    __connection_string: str = getenv('ST_CONNSTRING')
    __default_container: str = getenv('ST_CONTAINER_NAME')

    def __init__(self):
        self.__ensure_instance()
        self.__ensure_container()

    def __ensure_instance(self) -> ContainerClient:
        if self.__instance is None:
            blob_service_client = BlobServiceClient.from_connection_string(self.__connection_string)
            self.__instance = blob_service_client.get_container_client(self.__default_container)

        return self.__instance

    def __ensure_container(self) -> None:
        if not self.__instance.exists():
            self.__instance.create_container({'category': 'backups'}, 'container')

    def upload(self, filename, data) -> Optional[bool]:
        """
        Devolve um valor booleano indicando se o upload foi realizado

        args:
            filename: Nome do arquivo
            data: Dados do arquivo

        return:
            bool: True se o upload foi realizado, False caso contrário
        """
        try:
            logging.info('Realizando upload do arquivo %s', filename)
            response = self.__instance.upload_blob(filename, data, BlobType.BLOCKBLOB, metadata={'servidor': filename}, overwrite=True)
            return response is not None
        except Exception as e:
            logging.error('Erro capturado %s', str(e))
            return None

    def download(self, uri: str) -> Optional[bytes]:
        """
        Retorna o caminho do arquivo baixado

        args:
            uri: URI do arquivo

        return:
            str: Caminho do arquivo baixado
        """
        try:
            logging.info('Baixando arquivo %s', uri)
            buffer_size = 10 * (1024 ** 10)
            return self.__instance.download_blob(uri, length=buffer_size, offset=0).readall()
        except Exception as e:
            logging.error('Erro capturado %s', str(e))
            return None
