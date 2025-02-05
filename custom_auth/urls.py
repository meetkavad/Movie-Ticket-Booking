from django.urls import path
from .views import signup, login, updateUser, deleteUser, VerifyEmail

urlpatterns = [
    path('signup/', signup,  name='signup'),
    path('login/', login,  name='login'),
    path('delete/', deleteUser, name="delete_user"),
    path('update/', updateUser,  name='update_user'),
    path('verifyuser/', VerifyEmail,  name='verify_user'),  
]