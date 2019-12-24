
class Authentication:
    username = "InternalDebugging"
    password = "None"

class RedisAuthentication:
  password = None

class SettingsConfiguration:
    mongoHost = "localhost"
    mongoPort = 22100
    authentication = Authentication

    redisHost = "localhost"
    redisPort = 6379
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