from modules.database.createDatabase import MongoDB
from modules.authentication import SettingsConfiguration as Configuration
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

    def __init__(self, mongoDbObject, redisConnection):
        self.redisConnection = redisConnection
        if isinstance(mongoDbObject, MongoDB) == True:
            self._mongoDb = mongoDbObject
            attempt_loadPrimaries = self._loadPrimaryDatabase()
            if attempt_loadPrimaries == True:
                self._primaryVerifiation = True
            else:
                raise Exception('Unable to load primary database.')
        else:
            raise ValueError(f'Improper Object. Expected MongoDB. {mongoDbObject}')
        logger.info('Initalized Pull User.')

    def _redisPullUser(self, redis_cache_id):
        try:
            redis_query, redis_result = self.redisConnection._checkKey(
                redis_cache_id
            )
            if redis_query == True:
                return True, redis_result
            
            return False, None
        except Exception as error:
            logger.info(f"unable to get redis result due to {error}")
            return False, None

    def _mongoPullUser(self, object_id):
        # Fallback.
        
        mongo_result = self._mongoDb.find_one(
            {
                "_id": ObjectId(object_id)
            }
        )

        if mongo_result:
            return True, mongo_result
        else:
            logger.critical("Unable to find mongo result even with provided ID!")
            logger.debug("Error ID: {object_id}")
            return False, None



    def pull_user_from_service(self, verifyObject, providedServiceId):
        # Psuedo Link to verifyUser.verify_user with Configuration
        provided_configuration = Configuration()

        # Configure
        provided_configuration.provided_id_bool = False
        provided_configuration.serviceUniqueId = providedServiceId
        
        return verifyObject.verify_user(provided_configuration)

    def pull_user(self, redis_cache_id):
        
        redis_query, redis_result = self._redisPullUser(
            redis_cache_id
        )

        if redis_query == True:
            return redis_result
        
        else:
            mongo_query, mongo_result = self._mongoPullUser(
                redis_cache_id
            )

            if mongo_query == True:
                return mongo_result
            else:
                logger.critical(f"Completely Unable to Find Specified ID! {redis_cache_id}")
                return None
