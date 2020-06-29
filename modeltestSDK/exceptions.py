
class AuthenticationError(BaseException):
    def __init__(self, response):
        msg = response['msg']

    def __repr__(self):
        print(self.msg)


