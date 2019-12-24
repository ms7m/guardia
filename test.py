from modules.authentication import SettingsConfiguration
from modules.database.createDatabase import MongoDB
from modules.database.newUser import CreateUser
from modules.database.verifyUser import VerifyUser
from modules.cache.connect import RedisConnection
class Configuration(object):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


if __name__ == "__main__":
    cur_redis = RedisConnection(SettingsConfiguration)
    inas = {
        "Bob": [
            "Megan"
        ]
    }
    res = cur_redis.cache_result("twea", inas)
    print(res)

    
