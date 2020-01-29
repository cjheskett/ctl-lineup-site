from django import forms

class NameForm(forms.Form):
    new_pw = forms.CharField(widget=forms.PasswordInput, label='New password', max_length=100)
    new_pw_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm password', max_length=100)