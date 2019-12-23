from modules.database.createDatabase import MongoDB
from datetime import datetime
from loguru import logger
from bson.objectid import ObjectId

class PullUser:
    def _loadPrimaryDatabase(self):
        try:
            self.primary_database = self._mongoDb.resulting['userData']
            return True
        except Exception as error:
            logger.debug(f'Dumped Attrs: {dir(self._mongoDb)}')
            try:
                logger.debug(f"Resulting: {self._mongoDb.resulting}")
            except Exception as dumped_error:
                logger.error('Complete Failure. Both Exceptions occured.')
                logger.error(f'Error on PrimaryGet: {error}')
                logger.error(f"Error on Dump: {dumped_error}")
            raise Exception('Unable to load primary Database.')

    def __init__(self, mongoDbObject):
        if isinstance(mongoDbObject, MongoDB) == True:
            self._mongoDb = mongoDbObject
            attempt_loadPrimaries = self._loadPrimaryDatabase()
            if attempt_loadPrimaries == True:
                self._primaryVerifiation = True
            else:
                raise Exception('Unable to load primary database.')
        else:
            raise ValueError(f'Improper Object. Expected MongoDB. {mongoDbObject}')
    
    def pull_user(self, redis_cache_id):
        if isinstance(user_id, ObjectId) == True:
            pass
                
        