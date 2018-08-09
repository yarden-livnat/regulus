class RegulusError(Exception):
    """Base class for Regulus exceptions"""
    pass


class RegulusMissingError(RegulusError):
    """Exception for missing information"""
    def __init__(self, message):
        self.message = message