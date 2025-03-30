from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import WasteGenerator, WasteCollector, WasteType, Organization, WasteGeneratorGroup, UserRole, UserProfile, Permission, RolePermission, ModulePermission

class WasteGeneratorForm(forms.ModelForm):
    class Meta:
        model = WasteGenerator
        fields = [
            'name', 
            'address_line1', 
            'address_line2', 
            'city', 
            'state', 
            'zipcode',
            'group',
            'waste_specification',
            'contact_person',
            'contact_email',
            'contact_phone',
            'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'required': True,
                'placeholder': 'Enter waste generator name'
            }),
            'address_line1': forms.TextInput(attrs={
                'class': 'input',
                'required': True,
                'placeholder': 'Address 1'
            }),
            'address_line2': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Address 2'
            }),
            'city': forms.TextInput(attrs={
                'class': 'input',
                'required': True,
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'input',
                'required': True,
                'placeholder': 'State'
            }),
            'zipcode': forms.TextInput(attrs={
                'class': 'input',
                'required': True,
                'placeholder': 'Zipcode'
            }),
            'group': forms.Select(attrs={
                'class': 'input',
                'required': True
            }),
            'waste_specification': forms.Select(attrs={
                'class': 'input',
                'required': True
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'input',
                'required': True,
                'placeholder': 'Enter contact name'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'input',
                'required': True,
                'placeholder': 'Enter contact email'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'input',
                'required': True,
                'type': 'tel',
                'placeholder': 'Enter contact phone'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'checkbox'
            }),
        }

class WasteCollectorForm(forms.ModelForm):
    class Meta:
        model = WasteCollector
        fields = ['name', 'license_number', 'contact_person', 'contact_email', 'contact_phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'license_number': forms.TextInput(attrs={'class': 'input'}),
            'contact_person': forms.TextInput(attrs={'class': 'input'}),
            'contact_email': forms.EmailInput(attrs={'class': 'input'}),
            'contact_phone': forms.TextInput(attrs={'class': 'input'}),
        }

class WasteTypeForm(forms.ModelForm):
    class Meta:
        model = WasteType
        fields = ['name', 'description', 'hazardous']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'class': 'textarea'}),
            'hazardous': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }

class OrganizationSettingsForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'address', 'contact_person', 'contact_email', 'contact_phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'address': forms.Textarea(attrs={'class': 'textarea'}),
            'contact_person': forms.TextInput(attrs={'class': 'input'}),
            'contact_email': forms.EmailInput(attrs={'class': 'input'}),
            'contact_phone': forms.TextInput(attrs={'class': 'input'}),
        }

class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    role = forms.ModelChoiceField(queryset=None, required=True)
    profile_pic = forms.ImageField(required=False)
    is_active = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'role', 'profile_pic', 'is_active')

    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        if organization:
            self.fields['role'].queryset = UserRole.objects.filter(organization=organization)

class UserEditForm(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=UserRole.objects.all(), required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            try:
                profile = self.instance.profile
                self.fields['role'].initial = profile.role
                self.fields['phone_number'].initial = profile.phone_number
            except UserProfile.DoesNotExist:
                pass

class RoleForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = UserRole
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['permissions'].initial = self.instance.permissions.all()

    def save(self, commit=True):
        role = super().save(commit=False)
        if commit:
            role.save()
            if 'permissions' in self.cleaned_data:
                role.permissions.set(self.cleaned_data['permissions'])
        return role

class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ('name', 'codename', 'description')

class RolePermissionForm(forms.Form):
    role = forms.ModelChoiceField(queryset=None, required=True)
    permissions = forms.MultipleChoiceField(
        choices=ModulePermission.MODULE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        if organization:
            self.fields['role'].queryset = UserRole.objects.filter(organization=organization)

    def save(self):
        role = self.cleaned_data['role']
        permissions = self.cleaned_data['permissions']
        
        # Clear existing permissions
        role.module_permissions.all().delete()
        
        # Add new permissions
        for permission in permissions:
            ModulePermission.objects.create(role=role, module=permission) 