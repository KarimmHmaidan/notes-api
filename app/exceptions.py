class InvalidCredentialsException(Exception):
    """Exception raised for invalid credentials."""
    pass

class UserAlreadyExistsException(Exception):
    """Exception raised when a user with the given username or email already exists."""
    pass
class NoteNotFoundException(Exception):
    """Exception raised when a note with the given ID is not found."""
    pass