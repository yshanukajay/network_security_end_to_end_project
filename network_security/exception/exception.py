import sys
from network_security.logging.logger import logging

class CustomException(Exception):
    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)
        _, _, exc_tb = error_details.exc_info()

        self.line_number = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename
        self.error_message = error_message

    def __str__(self):
        return f"Error in {self.file_name} at line {self.line_number}: {self.error_message}"

if __name__ == "__main__":
    try:
        logging.info("Testing custom exception")
        a = 1/0
    except Exception as e:
        logging.error("Custom exception raised")
        raise CustomException(e, sys)
        
