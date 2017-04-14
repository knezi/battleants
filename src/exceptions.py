class OutOfRangeError(Exception):
    """Exception raised when accessing non-existing position in a BoxContainer

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
