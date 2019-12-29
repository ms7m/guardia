
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

from dulwich.repo import Repo
import os


# Splashscreen information
def createSplashScreenLogo():
    current_Splash = open("splashscreen", "r")
    print(current_Splash.read())

def is_development_mode_active():
    try:
        if os.getenv("DEBUG_Guardia") == "active":
            print("Debug Mode Is Active.")
        else:
            print('Debug Mode is not Active.')
    except Exception as error:
        print("Unable to get OS Environment Variable.")

def displayLatest_development():
    try:
        current_repo = Repo(".")
        git_head = current_repo.head()
        git_last_commit = current_repo[git_head]
    except Exception as error:
        print('unable to get git information.')
        return
    
    try:
        print(f"Last Commit: {git_last_commit.id.decode()}")
        print(f"Commit Author: {git_last_commit.author.decode()}")
        print(f"Commit Message: {git_last_commit.message.decode()}")
    except Exception as error:
        print('Unable to get git information.')


def api():
    mongo = MongoDB(SettingsConfiguration)
    redis = RedisConnection(SettingsConfiguration)
    vrf_user = VerifyUser(mongo, redis)
    crt_user = CreateUser(mongo, vrf_user)
    pull_user = PullUser(mongo, redis)


    os.system('clear')
    createSplashScreenLogo()
    print("-" * 24)
    displayLatest_development()
    is_development_mode_active()
    
    api = falcon.API()

    api.add_route("/newUser", UserCreation(crt_user))
    api.add_route("/serviceAdd/{user_id}", NewServiceAddition(crt_user))
    api.add_route("/pullUser/{user_id}", PullUserInformation(pull_user))
    api.add_route("/pullFromService", PullUserInforamtionFromService(pull_user, vrf_user))
    return api

if __name__ == "__main__":
    mongo = MongoDB(SettingsConfiguration)
    redis = RedisConnection(SettingsConfiguration)
    vrf_user = VerifyUser(mongo, redis)
    crt_user = CreateUser(mongo, vrf_user)
    pull_user = PullUser(mongo, redis)


    os.system('clear')
    createSplashScreenLogo()
    print("-" * 24)
    displayLatest_development()
    is_development_mode_active()
    
    api = falcon.API()

    api.add_route("/newUser", UserCreation(crt_user))
    api.add_route("/serviceAdd/{user_id}", NewServiceAddition(crt_user))
    api.add_route("/pullUser/{user_id}", PullUserInformation(pull_user))
    api.add_route("/pullFromService", PullUserInforamtionFromService(pull_user, vrf_user))
    serve(api, port=3002)


