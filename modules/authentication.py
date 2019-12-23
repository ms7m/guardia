
class Authentication:
    username = "InternalDebugging"
    password = "None"


class SettingsConfiguration:
    mongoHost = "localhost",
    mongoPort = 22100
    authentication = Authentication

"""
 db.createUser(
  {
    user: "InternalDebugging",
    pwd: "None",
    roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
  }
)
"""