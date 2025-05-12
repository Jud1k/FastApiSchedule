from fastapi import status, HTTPException


class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass


PasswordsDoNotMatch = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Passwords do not match",
)

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exists",
)

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found",
)

UserIdNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Missing user id",
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Incorrect email or password",
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="The token has expired",
)

InvalidTokenFormatException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Incorrect token format",
)


TokenNoFound = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The token missing from header",
)

NoJwtException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="The token is not valid",
)

NoUserIdException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User id is not found",
)

ForbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not enough rights",
)
