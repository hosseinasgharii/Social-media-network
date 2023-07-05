from django import forms
from accounts.models import MyUser


class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['email', 'username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserEditProfileForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "username"}
        )
    )
    firstname = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "firstname"}
            )
    )
    lastname = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "lastname"}
            )
    )
    bio = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "bio"},
            )
    )
    gender_choices = (
        (1, 'Male'),
        (2, 'Female'),
    )
    gender = forms.ChoiceField(
        choices=gender_choices,
        widget=forms.Select(
            attrs={"placeholder": "gender"}
            )
    )
    phonenumber = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "phonenumber"}
            )
    )
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "date_of_birth"}
            )
    )

    class Meta:
        model = MyUser
        fields = [
            'username', 'firstname', 'lastname',
            'bio', 'gender',
            'phonenumber', 'date_of_birth'
            ]
