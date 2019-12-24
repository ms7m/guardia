
from redis import Redis
import json
from loguru import logger
import arrow


class RedisConnection(object):
    
    def _generateRedis(self):
        try:
            self._redisConnection = Redis(
                host=self._redisHost,
                port=self._redisPort,
                db=0,
            )
            self._redisConnection.ping()
        except Exception as error:
            logger.critical(f"Unable to create redis object. {error}")
            logger.debug(f"Dropped Attrs: {dir(self)}")
            logger.debug(f'dict_dropped: {self.__dict__}')
            raise Exception("Unable to create redis object")

    def __init__(self, settingsConfiguration):
        self._settingsConfiguration = settingsConfiguration
        self._redisHost = self._settingsConfiguration.redisHost
        self._redisPort = self._settingsConfiguration.redisPort
        self._redisAuthentication = self._settingsConfiguration.redisAuthentication
        self._generateRedis()
        logger.info('Initalized Redis.')



    def _checkKey(self, dbKey):
        try:
            query_test = self._redisConnection.get(dbKey)
            if query_test:
                return True, json.loads(query_test.decode())
            else:
                return False, None
        except Exception as error:
            return False, f"Doesn't exist. --> {error}"


    def cache_result(self, dbKey, dbValue, alreadyChecked=False):
        
        if alreadyChecked == False:
            query_result, query_message = self._checkKey(dbKey)
        else:
            query_result = False
        
        if query_result == False:
            try:
                # Clean Up DB Value. 
                dbValue['_id'] = str(dbValue['_id'])

                action_input = json.dumps(dbValue)
                self._redisConnection.set(
                    dbKey,
                    action_input
                )

                self._redisConnection.expireat(
                    dbKey,
                    arrow.now().shift(hours=3).datetime
                )
                logger.info(f"cached ({dbKey}).")
                return True
            except Exception as error:
                logger.error(f'Unable to add to redis: {error}')
                logger.debug(f"DBKey ---> {dbKey}")
                return False
        else:
            # TODO: Raise the minimum cache refresh time.
            logger.info("already cached.")
            return True

    
    def update_result(self, dbKey, dbValue):
        query_result, query_message = self._checkKey(dbKey)

        if query_result == True:
            self._redisConnection.delete(
                dbKey
            )
            self.cache_result(dbKey, dbValue, alreadyChecked=True)
        else:
            logger.info("We haven't cached this yet, why was this called?")
            logger.debug(f"Message: {query_message}")
            self.cache_result(dbKey, dbValue)
    