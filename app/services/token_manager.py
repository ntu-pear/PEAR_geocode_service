from fastapi import Depends
import time

class TokenManager:
    _instance = None  # Class variable to hold the singleton instance
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)  # Create the singleton instance
            cls._instance.token = ""
            cls._instance.expiry = ""
        return cls._instance
    
    def is_token_valid(self):
        if not self.token or self.token == "":
            return False

        if not self.expiry or self.expiry == "":
            return False
        try:
            expiry_timestamp = int(self.expiry)
        except ValueError:
            return False 
        # If token is expired (current time + 5 minutes >= expiry), return False
        if time.time() + (5 * 60) >= expiry_timestamp:
            return False

        return True

    def update_token(self, token, expiry):
        self.token = token
        self.expiry = expiry


def get_token_manager() -> TokenManager:
    token_manager = TokenManager() 
    return token_manager