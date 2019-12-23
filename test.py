from modules.authentication import SettingsConfiguration
from modules.database.createDatabase import MongoDB
from modules.database.newUser import CreateUser
from modules.database.verifyUser import VerifyUser
class Configuration(object):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


if __name__ == "__main__":
    try:
        res = MongoDB(SettingsConfiguration)
        print('Connection Active?')
        print('Dumped Attrs.')
        #for attr in dir(res):
        #    print(attr)


        print('adding test user')

        config = Configuration()
        config.serviceName = "TestService"
        config.serviceId = "222"
        config.username = "bob"

        #cras = CreateUser(res)
        #result, result_message = cras.add_new_user(
        #    config
        #)
        #print(result)
        #print(result_message)

        config.provided_id_bool = True
        config.provided_id = "5e00f85930c0c3ad46f7b42e"

        res1, resCode, resMessage = VerifyUser(
            res
        ).verify_user(
            config
        )

        print(res1)
        print(resCode)
        print(resMessage)
    except Exception as error:
        print(f'error: {error}')