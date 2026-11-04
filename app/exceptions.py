
class InvalidPincodeError(Exception):
    """Not 6 digits"""
    def __init__(self, pincode: str):
        self.pincode = pincode

class PincodeNotServiceableError(Exception):
    """Pincode not serviceable"""
    def __init__(self, pincode: str):
        self.pincode = pincode

class ServiceUnavailableError(Exception):
    """Service is unavailable"""
    def __init__(self, service_id: int):
        self.service_id = service_id
        self.active = False
