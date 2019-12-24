# Create User Endpoint

import falcon
from modules.database.newUser import CreateUser
from loguru import logger



class Configuration:
    def __init__(self, req_object):
        self._req_object = req_object
        self.serviceName = self._req_object.get_param("firstServiceLinked")
        self.serviceUniqueId = self._req_object.get_param("firstServiceLinkedID")
        self.username = f"{self._req_object.get_param('username')}".strip()

class UserCreation:
    def __init__(self, createUserObject):
        if isinstance(createUserObject, CreateUser) == False:
            raise Exception("Improper Value Returned.")

        self._createUser = createUserObject


    def on_post(self, req, resp):
        # TODO: Intergrate with Core Trackrr Reference

        try:
            current_object = Configuration(req)

            current_object.provided_id_bool = False

            attempt, attempt_result = self._createUser.add_new_user(
                current_object
            )

            if attempt == 10:
                attempt_result['status'] = "failure"
                resp.media = attempt_result
                return 

            if attempt == True:
                resp.media = {
                    "status": attempt,
                    "resultingId": str(attempt_result)
                }
                return

            else:
                resp.media = {
                    "status": attempt_result,
                    "message": str(attempt_result)
                }
        except Exception as error:
            logger.error(error)
            resp.media = {
                "status": "complete failure",
                "message": "Outer scope error. Please check logs."
            }

class NewServiceAddition:
    def __init__(self, createUserObject):
        if isinstance(createUserObject, CreateUser) == False:
            raise Exception("Improper Value Returned.")

        self._createUser = createUserObject

    def on_post(self, req, resp, user_id):
        current_object = Configuration(req)
        current_object.provided_id_bool = True

        attempt_code, attempt_message = self._createUser.add_new_service(
            current_object,
            user_id,
            req.get_param("service"),
            req.get_param("serviceUniqueId")
        )

        resp.media = {
            "status": attempt_code,
            "message": attempt_message
        }
                

