class CustomException(Exception):
    """Base class for custom exceptions"""
    def __init__(self,header:dict, status_code: int, error_code:str,detail:str):
        self.header = header,
        self.status_code = status_code
        self.error_code = error_code
        self.detail = detail
        super().__init__(self.detail)   

