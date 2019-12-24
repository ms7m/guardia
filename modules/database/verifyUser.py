from modules.database.createDatabase import MongoDB
from datetime import datetime
from loguru import logger
from bson.objectid import ObjectId

class VerifyUser:
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
        logger.info('Initalized Verify User.')


    def verify_user(self, configuration):
        # TODO: Integrate with Trackrr Core Reference File
        
        try:
            if configuration.provided_id_bool == False:
                # We weren't provided an ID :(
                query_to_push = {
                    "firstLinkedServiceInformation.serviceUniqueId": configuration.serviceUniqueId
                }
            elif configuration.provided_id_bool == True:
                # Nice, we were provided a DB id
                query_to_push = {
                    "_id": ObjectId(configuration.provided_id)
                }

            else:
                raise Exception("Did not provide a provided_id bool.")
        except Exception as error:
            logger.debug(f"Dropped Attrs: {configuration.__dict__}")
            raise Exception(f"Error on checkcing for configProvided!. --> {error}")
        
        try:
            attempt_query = self.primary_database.find_one(
                query_to_push
            )

            # Honestly, while we already have the data
            # might as well add it to a cache for PullUser
            
            if attempt_query:
                try:
                    redis_action = self.redisConnection.cache_result(
                        str(attempt_query['_id']),
                        attempt_query
                    )
                    if redis_action == True:
                        return True, 0, attempt_query['_id']
                    else:
                        logger.error("Unable to add to redis.")
                        return True, 2, attempt_query

                except Exception as error:
                    logger.error(f'Unable to add to redis. --> {error}')
                    return True, 2, attempt_query
                
                return True, 0, attempt_query['_id']
            else:
                return False, 1, "Unable to verify. User isn't in database."
        except Exception as error:
            return False, 0, f"Unable to Verify User due to Server Error. {error}"