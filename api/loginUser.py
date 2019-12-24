import falcon
from modules.database.verifyUser import VerifyUser
from loguru import logger

class VerifyUser:
    def __init__(self, verifyUserObject):
        if isinstance(verifyUserObject, VerifyUser) == False:
            raise Exception("Improper Value Returned")

        self._verifyUser = verifyUserObject

    def on_get(self, req, resp):
        verify_params = [
            "u"
        ]