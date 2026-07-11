from typing import Any, Optional
from fastapi import status

class EduPilotException(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[Any] = None
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)

class StudentNotFoundException(EduPilotException):
    def __init__(self, student_id: str):
        super().__init__(
            code="STUDENT_NOT_FOUND",
            message=f"Student with ID '{student_id}' was not found.",
            status_code=status.HTTP_404_NOT_FOUND
        )

class ModelNotFoundException(EduPilotException):
    def __init__(self, message: str = "The predictive ANN model or preprocessor could not be loaded."):
        super().__init__(
            code="MODEL_NOT_FOUND",
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )

class InvalidAcademicDataException(EduPilotException):
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            code="INVALID_ACADEMIC_DATA",
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )

class DocumentProcessingException(EduPilotException):
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            code="DOCUMENT_PROCESSING_FAILED",
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )

class AIProviderException(EduPilotException):
    def __init__(self, provider: str, message: str):
        super().__init__(
            code=f"{provider.upper()}_PROVIDER_ERROR",
            message=f"Error communicating with AI Provider ({provider}): {message}",
            status_code=status.HTTP_502_BAD_GATEWAY
        )

class HumanReviewException(EduPilotException):
    def __init__(self, message: str):
        super().__init__(
            code="HUMAN_REVIEW_FAILED",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST
        )

class ReportGenerationException(EduPilotException):
    def __init__(self, message: str):
        super().__init__(
            code="REPORT_GENERATION_FAILED",
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
