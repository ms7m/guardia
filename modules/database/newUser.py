
from modules.database.createDatabase import MongoDB
from datetime import datetime
from loguru import logger 


class CreateUser:
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

    def add_new_user(self, configuration):
        # TODO: Integrate it with Trackrr Core Reference File

        current_configuration = configuration
        current_time = datetime.now()
        current_time_to_iso = current_time.isoformat()
        # This assumes that it's already been checked. 
        try:
            attempt_addition = self.primary_database.insert_one(
                {
                    "firstLinkedServiceInformation": {
                        "serviceName": current_configuration.serviceName,
                        "serviceUniqueId": current_configuration.serviceId
                    },
                    "linkedServicesInformation": [
                        {
                            "serviceName": current_configuration.serviceName,
                            "serviceUniqueId": current_configuration.serviceId
                        }
                    ],
                    "userInfo": {
                        "userProvidedUsername": current_configuration.username,
                        "dateCreation": current_time_to_iso
                    }
                }
            )
            return True, attempt_addition.inserted_id
        except Exception as error:
            logger.debug(
                f"""
                Unable to add new user.

                currentConfiguration: {type(current_configuration)}
                currentConfigurationAttrs: {dir(current_configuration)}
                exception: {error}
                """
            )
            return False, "Unable to add new user. Please check logs."