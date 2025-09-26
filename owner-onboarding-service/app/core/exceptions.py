class CustomException(Exception):
    """Base class for custom exceptions"""
    def __init__(self, status_code: int, error_code:str,detail:str):
        self.status_code = status_code
        self.error_code = error_code
        self.detail = detail
        super().__init__(self.detail)

