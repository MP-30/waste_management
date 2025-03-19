from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.hashers import check_password


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



class InitialLoginForm(forms.Form):  
    temporary_password = forms.CharField(
        label="Temporary Password",
        widget=forms.PasswordInput,
        max_length=128  # Increased length to match Django's password storage
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput,
        required=True  # Ensures new password is mandatory
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput,
        required=True
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # Pass the user instance to the form
        super().__init__(*args, **kwargs)

    def clean_temporary_password(self):
        """Validate the temporary password against the stored password"""
        temp_pw = self.cleaned_data.get("temporary_password")

        if self.user and not check_password(temp_pw, self.user.password):
            raise forms.ValidationError("Temporary password is incorrect.")
        
        return temp_pw

    def clean(self):
        """Ensure new passwords match"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password1 != password2:
            raise forms.ValidationError("New passwords must match.")
        
        return cleaned_data

    def save(self):
        """Set the new password for the user"""
        self.user.set_password(self.cleaned_data["new_password1"])
        self.user.save()
        return self.user