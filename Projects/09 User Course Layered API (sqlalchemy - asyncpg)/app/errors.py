from fastapi import HTTPException, status


class InvalidCredentials(HTTPException):
    def __init__(self):
        status_code = status.HTTP_401_UNAUTHORIZED
        detail = "Could not validate credentials"
        headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(status_code, detail, headers)


class TokenExpired(HTTPException):
    def __init__(self):
        status_code = status.HTTP_401_UNAUTHORIZED
        detail = "Token has expired"
        headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(status_code, detail, headers)
