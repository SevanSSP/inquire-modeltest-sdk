
class AuthenticationError(BaseException):
    def __init__(self, response):
        msg = response['msg']

    def __repr__(self):
        print(self.msg)


def parse_response(response):
    print("\n Server side error:")
    if response['detail'] is not None:
        for error in response['detail']:
            print(error)
    print("\n")
