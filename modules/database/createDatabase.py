

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from loguru import logger


class MongoDB:
    def _generateMongo(self):
        try:
            self._mongoConnection = MongoClient(
                host=self._mongoHost,
                port=self._mongoPort
                #username=self._mongoAuthentication.username,
                #password=self._mongoAuthentication.password,
                #authSource="admin",
                #authMechanism='SCRAM-SHA-256'
            )
        except Exception as error:
            logger.error(f"Unable to create Mongo object. {error}")
            logger.debug(f"Dropped Attrs: {dir(self)}")
            raise Exception("Unable to create Mongo Object.")
        
        if self._mongoConnection:
            try:
                # Set the Maximum Connection Threshold to 1ms
                self._mongoConnection.serverSelectionTimeoutMS = 1
                self._mongoConnection.server_info()

                # Set back to default.
                self._mongoConnection.serverSelectionTimeoutMS = 30000
            except ServerSelectionTimeoutError:
                raise Exception(f"Unable to connect to {self._mongoHost}.")
        else:
            logger.debug(f"Dropped Attrs: {dir(self)}")
            logger.critical("No Mongo Was Found!")
            raise Exception("No Mongo found.")
    
    def _parseMongoDatabases(self):
        try:
            result = {
                "userActiveLogin": self._mongoConnection.db.activeLoggedIn,
                "userData": self._mongoConnection.db.userData
            }
            return result
        except Exception as error:
            logger.error(f"Unable to return a parsed list of DB. {error}")
            raise Exception("unable to return parsed list.")


    def __init__(self, settingsConfiguration):
        self._settingsConfiguration = settingsConfiguration
        self._mongoHost = self._settingsConfiguration.mongoHost
        self._mongoPort = self._settingsConfiguration.mongoPort
        self._mongoAuthentication = self._settingsConfiguration.authentication
        self._generateMongo()
        self.resulting = self._parseMongoDatabases()
        logger.info('Initalized Mongo.')
