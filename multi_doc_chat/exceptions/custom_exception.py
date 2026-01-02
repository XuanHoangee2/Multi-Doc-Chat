import sys
import traceback
from typing import Optional, cast

class DocumentPortalException(Exception):
    def __init__(self, error_message, error_detail: Optional[object] = None):
        # normalize message
        if isinstance(error_message, BaseException):
            norm_msg = str(error_message)
        else:
            norm_msg = str(error_message)
        
        # resolve exc_info
        exc_type = exc_value = exc_tb = None
        if error_detail is None:
            exc_type, exc_value, exc_tb = sys.exc_info()
        else:
            if hasattr(error_detail, "exc_info"):
                exc_info_obj = cast(sys, error_detail)
                exc_type, exc_value, exc_tb = exc_info_obj.exc_info()
            elif isinstance(error_detail, BaseException):
                exc_type, exc_value, exc_tb = type(error_detail), error_detail, error_detail.__traceback__
            else:
                exc_type, exc_value, exc_tb = sys.exc_info()

        last_tb = exc_tb
        while last_tb and last_tb.tb_next:
            last_tb = last_tb.tb_next
        
        self.filename = last_tb.tb_frame.f_code.co_filename if last_tb else "<unknown>"
        self.lineno = last_tb.tb_lineno if last_tb else -1
        self.error_message = norm_msg

        # fully pretty traceback
        if exc_type and exc_tb:
            self.traceback = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
        else:
            self.traceback = "No traceback available"

        super().__init__(self.__str__())
    
    def __str__(self):
        base = f"Error in [{self.filename}] at line [{self.lineno}] | Message: {self.error_message}"
        if self.traceback:
            return f"{base}\nTraceback:\n{self.traceback}"
        return base
    
    def __repr__(self): 
        return f"DocumentPortalException(file={self.filename!r}, line={self.lineno}, message={self.error_message!r})"

def test_document_portal_exception():
    print("=== Test 1: raise inside try/except ===")
    try:
        1 / 0
    except Exception as e:
        ex = DocumentPortalException("Division error occurred", e)
        print(ex)
        print(repr(ex))
    
    print("\n=== Test 2: pass exception object directly ===")
    e2 = ValueError("Invalid value")
    ex2 = DocumentPortalException("Value error test", e2)
    print(ex2)
    print(repr(ex2))
    
    print("\n=== Test 3: no error_detail, capture current exc_info ===")
    try:
        int("abc")  # will raise ValueError
    except:
        ex3 = DocumentPortalException("Conversion failed")
        print(ex3)
        print(repr(ex3))
    
    print("\n=== Test 4: non-exception detail ===")
    ex4 = DocumentPortalException("Custom error message", error_detail="random string")
    print(ex4)
    print(repr(ex4))


# Run tests
test_document_portal_exception()
