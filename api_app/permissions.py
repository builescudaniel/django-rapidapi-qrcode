from rest_framework.permissions import BasePermission
import os

class IsAuthenticatedOrFromRapidAPI(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True  # Allow if user is authenticated

        # Check if the request has been authenticated by our custom RapidAPI authentication
        rapidapi_secret = request.headers.get('X-RapidAPI-Proxy-Secret')
        if rapidapi_secret and rapidapi_secret == os.getenv('RAPID_API_KEY'):
            return True  # Allow if from RapidAPI with correct key

        return False
