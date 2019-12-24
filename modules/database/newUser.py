
from modules.database.createDatabase import MongoDB
from datetime import datetime
from loguru import logger 
from modules.database.verifyUser import VerifyUser
from bson.objectid import ObjectId
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


    def __init__(self, mongoDbObject, VerifyUserObject):
        self.verifyObj = VerifyUserObject

        if isinstance(mongoDbObject, MongoDB) == True:
            self._mongoDb = mongoDbObject
            attempt_loadPrimaries = self._loadPrimaryDatabase()
            if attempt_loadPrimaries == True:
                self._primaryVerifiation = True
            else:
                raise Exception('Unable to load primary database.')
        else:
            raise ValueError(f'Improper Object. Expected MongoDB. {mongoDbObject}')
        logger.info('Initalized New User.')

    def add_new_service(self, configuration, user_id, serviceName, serviceUniqueId):
        try:
            configuration.provided_id = user_id
            vrf_bool, vrf_code, vrf_msg = self.verifyObj.verify_user(
                configuration
            )

            if vrf_bool == True:
                if str(vrf_msg) == user_id:
                    return 10, "User already has Service ID Saved."
                else:
                    return "failure", "This service is already linked to a different account."
            elif vrf_bool == False:
                action = self.primary_database.find_and_modify(
                    query={"_id": ObjectId(user_id)},
                    update = {
                        "$push": {
                            "linkedServicesInformation": {
                                "serviceName": serviceName,
                                "serviceUniqueId": serviceUniqueId
                            }
                        }
                    }
                )

                if action:
                    return True
                else:
                    return False
        except Exception as error:
            logger.error(f"unable to add new service to user! {error}")
            return False

    def add_new_user(self, configuration):
        # TODO: Integrate it with Trackrr Core Reference File

        try:
            vrf_bool, vrf_code, vrf_msg = self.verifyObj.verify_user(
                configuration
            )

            if vrf_bool == True:
                return 10, {
                    "message": "User Already Exists.",
                    "userId": str(vrf_msg)
                }
        except Exception as error:
            logger.critical(f"Unable to VERIFY! {error}")
            return 2, "Serverside error."


        current_configuration = configuration
        current_time = datetime.now()
        current_time_to_iso = current_time.isoformat()
        # This assumes that it's already been checked. 
        try:
            attempt_addition = self.primary_database.insert_one(
                {
                    "firstLinkedServiceInformation": {
                        "serviceName": current_configuration.serviceName,
                        "serviceUniqueId": current_configuration.serviceUniqueId
                    },
                    "linkedServicesInformation": [
                        {
                            "serviceName": current_configuration.serviceName,
                            "serviceUniqueId": current_configuration.serviceUniqueId
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