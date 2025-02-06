from django.urls import path
from .views import signup, login, updateUser, deleteUser, VerifyEmail, forgotPassword, resetPassword

urlpatterns = [
    path('signup/', signup,  name='signup'),
    path('login/', login,  name='login'),
    path('delete/', deleteUser, name="delete_user"),
    path('update/', updateUser,  name='update_user'),
    path('verifyuser/', VerifyEmail,  name='verify_user'), 
    path('forgotpassword/', forgotPassword,  name='forgot_password'), 
    path('resetpassword/', resetPassword,  name='reset_password'), 

]