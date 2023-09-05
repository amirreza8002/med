from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email", "age")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")


class CustomSignUpForm(SignupForm):
    pass


# class UserInfoUpdateForm(forms.ModelForm):
#     class Meta:
#         model = get_user_model()
#         fields = ("name", "email", "age")
