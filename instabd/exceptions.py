class IGApiBaseException(Exception):
    solution = ""

    def __init__(self, error):
        if isinstance(error, dict):
            error["solution"] = self.solution
        if isinstance(error, str):
            error += f"\nsolution: {self.solution}"
        super().__init__(error)


class IGApiBadRequestException(IGApiBaseException):
    solution = (
        "Invalid field. Refer to endpoint's reference for list of available "
        "fields and retry with valid field."
    )


class IGApiException(IGApiBaseException):
    solution = (
        "Verify object exists and that owner has granted your app appropriate "
        "permissions to access this object."
    )


class IGApiUnauthorizedException(IGApiBaseException):
    solution = "Generate a new access token."


class IGApiCodedException(IGApiBaseException):
    solution = (
        "Application request limit reached. Please wait and retry the call."
    )


class IGApiForbiddenException(IGApiBaseException):
    solution = (
        "Verify owner has granted your app appropriate permissions to perform "
        "this action."
    )
