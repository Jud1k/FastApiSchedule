from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, record_name="Record", record_id=None, headers=None):
        """Custom HTTPException for 404 Not Found errors.

        Provides consistent formatting for "resource not found" scenarios
        with flexible messaging based on provided parameters."""
        message = f"{record_name} not found" if record_id is None else f"{record_name} with ID {record_id} not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message, headers=headers)


class ConflictException(HTTPException):
    def __init__(self, record_name="Record", headers=None):
        """Custom HTTPException for 409 Conflict errors."""
        message = f"{record_name} already exist"
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=message, headers=headers)


IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Incorrect email or password",
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="The token has expired",
)

TokenNoFound = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The token missing from header",
)

MissingCoockies = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The token missing from coockies",
)

NoJwtException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="The token is not valid",
)

ForbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not enough rights",
)
