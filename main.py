
import falcon

from modules.database.verifyUser import VerifyUser
from modules.database.newUser import CreateUser
from modules.database.pullUser import PullUser
from modules.database.createDatabase import MongoDB
from modules.cache.connect import RedisConnection
from modules.authentication import SettingsConfiguration

from api.createUser import UserCreation, NewServiceAddition
from api.pullUserInfo import PullUserInformation, PullUserInforamtionFromService

from loguru import logger
from waitress import serve


if __name__ == "__main__":
    mongo = MongoDB(SettingsConfiguration)
    redis = RedisConnection(SettingsConfiguration)
    vrf_user = VerifyUser(mongo, redis)
    crt_user = CreateUser(mongo, vrf_user)
    pull_user = PullUser(mongo, redis)

    api = falcon.API()

    api.add_route("/newUser", UserCreation(crt_user))
    api.add_route("/serviceAdd/{user_id}", NewServiceAddition(crt_user))
    api.add_route("/pullUser/{user_id}", PullUserInformation(pull_user))
    api.add_route("/pullFromService", PullUserInforamtionFromService(pull_user, vrf_user))
    serve(api, port=3002)


