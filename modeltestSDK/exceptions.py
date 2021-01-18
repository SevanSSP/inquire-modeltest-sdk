'''
Parse errors from the api
'''


class ClientException(Exception):
    def __init__(self, exception, response):
        prefix = "\n____________________________ CUSTOM ERROR ____________________________\n"

        if exception.response is not None and exception.response.status_code == 403:
            raise ConnectionRefusedError(
                f"{prefix}Access denied. You're ip has not been validated by Azure. Contact admin to get access")

        if response is not None:
            prefix = f"{prefix}Server returned error {response.status_code} for {response.url}:\n"
            if response.status_code == 422:
                message = f"Error when creating object\n"
                items = list(response.json().values())
                for item in items:
                    for it in item:
                        message = message + "Location: " + it["loc"][0] + ", " + it["loc"][1] + " | Message: " +\
                                  it["msg"] + "\n"
                raise ConnectionRefusedError( f"{prefix}{message}")

            elif response.status_code == 500:
                raise ConnectionAbortedError(
                    f"{prefix}The server could not handle the call to {response.url}\n"
                    f"See server logs for more information"
                )

            else:
                self.message = f"{prefix}{response.text}"
                raise ConnectionError(f"{prefix}{response.text}")

        if (response is None) and (exception.response is None):
            raise ConnectionError(
                    f"{prefix}Connection failed when retrieving data. Make sure server is running and url is correct")

        raise Exception

    def __repr__(self):
        print(self.message)


def parse_response(response):
    pass
