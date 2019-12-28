import falcon
from modules.database.pullUser import PullUser
from modules.database.verifyUser import VerifyUser
from loguru import logger


class PullUserInformation:
    def __init__(self, PullUserObject):
        if isinstance(PullUserObject, PullUser) == False:
            raise Exception("Improper Value Passed.")

        self._pullUser = PullUserObject

    
    def on_get(self, req, resp, user_id):
        try:
            attempt_query = self._pullUser.pull_user(
                user_id
            )

            if attempt_query == None:
                resp.media = {
                    "status": "failure",
                    "message": "Unable to get user information. Please check logs."
                }
                return

            resp.media = attempt_query
        except Exception as error:
            logger.error(f"PullUserInformation Complete Failure: {error}")
            resp.media = {
                "status": "failure",
                "message": "Compelete Failure."
            }

class PullUserInforamtionFromService:
    def __init__(self, PullUserObject, VerifyUserObject):
        if isinstance(VerifyUserObject, VerifyUser) == False:
            raise Exception("Improper Value Passed")
        
        self._verifyUser = VerifyUserObject

        if isinstance(PullUserObject, PullUser) == False:
            raise Exception("Improper Value Passed.")

        self._pullUser = PullUserObject

    def on_get(self, req, resp):
        user_params = [
            "serviceName",
            "serviceUniqueId"
        ]

            
        try:
            result_status, result_code, result_message = self._pullUser.pull_user_from_service(
                self._verifyUser,
                req.get_param(
                    "serviceUniqueId"
                )
            )
            resp.media = {
                "status": result_status,
                "id": str(result_message)
            }
        except Exception as error:
            logger.error(f"PullUserInforamtionFromService Complete failure. {error}")
            resp.media = {
                "status": "failure",
                "message": "Serverside error."
            }
