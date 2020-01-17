from app.helpers.utility import res


class Messages:
    AUTHENTICATION_FAILED = 'Authentication failed, please try again'
    AUTHORISATION_FAILED = 'You do not have the required permission'
    NOT_ENOUGH_INFO = 'Information you provided is not accurate'
    NOT_EXIST = 'Record not found'
    OBJECT_EXIST = 'Object exists'
    SUCCESS = 'Operation Success'
    OPERATION_FAILED = 'Operation Failed'


class Roles:
    MEMBER = 'member'
    ADMIN = 'admin'


class Responses:
    @staticmethod
    def NOT_EXIST():
        return res('', Messages.NOT_EXIST, 404)

    @staticmethod
    def SUCCESS():
        return res(Messages.SUCCESS)

    @staticmethod
    def OBJECT_EXIST():
        return res('', Messages.OBJECT_EXIST, 409)

    @staticmethod
    def OPERATION_FAILED():
        return res('', Messages.OPERATION_FAILED, 400)

    @staticmethod
    def AUTHENTICATION_FAILED():
        return res('', Messages.AUTHENTICATION_FAILED, 400)
    @staticmethod
    def AUTHORISATION_FAILED():
        return res('', Messages.AUTHORISATION_FAILED, 400)
