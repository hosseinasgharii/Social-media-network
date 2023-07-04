from django import forms
from accounts.models import MyUser


class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['email', 'username']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return confirm_password


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserEditProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = [
            'firstname', 'lastname',
            'bio', 'gender',
            'phonenumber', 'date_of_birth'
            ]
