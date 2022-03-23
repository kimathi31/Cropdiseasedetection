from django import forms
class ImageUploadForm(forms.Form):
   image = forms.ImageField(label=False)

class Loginform(forms.Form):
   username = forms.CharField(max_length=25,label='Enter Username')
   password = forms.CharField(max_length=25,label='Password',widget=forms.PasswordInput)