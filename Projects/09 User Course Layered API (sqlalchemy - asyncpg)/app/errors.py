from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from loguru import logger


class InvalidCredentials(HTTPException):
    def __init__(self):
        status_code = status.HTTP_401_UNAUTHORIZED
        detail = "Could not validate credentials"
        headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(status_code, detail, headers)


class InvalidToken(HTTPException):
    def __init__(self):
        status_code = status.HTTP_401_UNAUTHORIZED
        detail = "Invalid token"
        headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(status_code, detail, headers)


class ForbiddenException(HTTPException):
    def __init__(self):
        status_code = status.HTTP_403_FORBIDDEN
        detail = "You are not allowd to do this action"
        super().__init__(status_code, detail)


class AccountNotActice(HTTPException):
    def __init__(self):
        status_code = status.HTTP_403_FORBIDDEN
        detail = "Your account is not active"
        super().__init__(status_code, detail)


class PasswordsNotMatched(HTTPException):
    def __init__(self):
        status_code = status.HTTP_400_BAD_REQUEST
        detail = "Passwords do not match"
        super().__init__(status_code, detail)


class UserAlreadyRegistered(HTTPException):
    def __init__(self):
        status_code = status.HTTP_400_BAD_REQUEST
        detail = "Email is already registered"
        super().__init__(status_code, detail)


class UserNotFound(HTTPException):
    def __init__(self):
        status_code = status.HTTP_404_NOT_FOUND
        detail = "User not found"
        super().__init__(status_code, detail)


class SectionNotFound(HTTPException):
    def __init__(self):
        status_code = status.HTTP_404_NOT_FOUND
        detail = "Section not found"
        super().__init__(status_code, detail)


class CourseNotFound(HTTPException):
    def __init__(self):
        status_code = status.HTTP_404_NOT_FOUND
        detail = "Course not found"
        super().__init__(status_code, detail)


class ContentBlockNotFound(HTTPException):
    def __init__(self):
        status_code = status.HTTP_404_NOT_FOUND
        detail = "Content Block not found"
        super().__init__(status_code, detail)


async def custom_500_handler(request: Request, exc: Exception):
    logger.error(f"Server Error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Oops! Something went wrong. Please try again later."},
    )


def register_exceptions(app: FastAPI):
    app.add_exception_handler(Exception, custom_500_handler)
