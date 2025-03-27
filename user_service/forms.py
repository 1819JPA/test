from allauth.account.forms import SignupForm
from allauth.account.forms import LoginForm


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.username = self.cleaned_data.get("username")  # username 저장
        user.save()
        return user
    
class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         self.fields['login'].label = ""
         self.fields['password'].label = ""