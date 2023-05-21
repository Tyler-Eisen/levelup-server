# ADD THESE Imports
from django.urls import path
from levelupapi.views import register_user, check_user

# ADD THESE LINES TO urlpatterns
urlpatterns = [
    path('register', register_user),
    path('checkuser', check_user),
]
