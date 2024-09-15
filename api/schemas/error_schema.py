from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """Represents the structure of an error message."""
    message: str
