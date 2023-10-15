# Import necessary modules from Django's Rest Framework and the built-in 'os' module
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import os

# Define a custom authentication class that inherits from BaseAuthentication
class RapidAPIAuthentication(BaseAuthentication):
    
    # Define the authentication method
    def authenticate(self, request):
        
        # Try to retrieve the 'X-RapidAPI-Proxy-Secret' header from the request
        rapidapi_secret = request.headers.get('X-RapidAPI-Proxy-Secret')

        # If the retrieved header value matches our stored RAPID_API_KEY environment variable, the request is authenticated
        # We're returning (None, None) because while the request is authenticated, we're not associating it with any user
        if rapidapi_secret == str(os.getenv('RAPID_API_KEY')):
            return (None, None)  # Authentication is successful but no user is associated

        # If the header is present but doesn't match our stored value, raise an authentication error
        if rapidapi_secret is not None:
            raise AuthenticationFailed('Invalid RapidAPI secret key.')

        # If the header isn't even present, it means no authentication attempt was made. So, just return None.
        # By returning None, the system knows that this authentication method didn't apply, and it will move on to the next authentication method (if any exists)
        return None
