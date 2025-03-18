from django import forms
from .models import UserProfile
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["phone_number", "city", "pincode"] 
        labels = {
            "phone_number": "Phone Number",
            "city": "City",
            "pincode": "Pincode",
        }
        widgets = {
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "pincode": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  
            self.fields["phone_number"].disabled = True  


class InitialLoginForm(UserProfileForm):  
    first_name = forms.CharField(label="First Name", max_length=30, required=False)
    last_name = forms.CharField(label="Last Name", max_length=30, required=False)
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput, required=False)

    class Meta(UserProfileForm.Meta):
        fields = ["first_name", "last_name"] + UserProfileForm.Meta.fields  

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")

        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords must match")
        return password2

    def save(self, user, commit=True):
        """ Save user profile and optionally update password """
        user.first_name = self.cleaned_data.get("first_name") or user.first_name
        user.last_name = self.cleaned_data.get("last_name") or user.last_name

        if self.cleaned_data.get("new_password1"):
            user.set_password(self.cleaned_data["new_password1"]) 

        if commit:
            user.save()

        
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.phone_number = self.cleaned_data.get("phone_number") or profile.phone_number
        profile.city = self.cleaned_data.get("city") or profile.city
        profile.pincode = self.cleaned_data.get("pincode") or profile.pincode

        if commit:
            profile.save()

        return user
