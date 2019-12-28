
class Authentication:
    username = "InternalDebugging"
    password = "None"

class RedisAuthentication:
  password = None

class SettingsConfiguration:
    mongoHost = "localhost"
    mongoPort = 55551
    authentication = Authentication

    redisHost = "localhost"
    redisPort = 55552
    redisAuthentication = RedisAuthentication

"""
 db.createUser(
  {
    user: "InternalDebugging",
    pwd: "None",
    roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
  }
)
"""