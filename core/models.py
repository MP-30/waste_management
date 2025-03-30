from django.db import models
from django.contrib.auth.models import User

class Organization(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_person = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_organizations')

    class Meta:
        db_table = 'tbl_organization'

    def __str__(self):
        return self.name

class WasteGeneratorGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_waste_generator_group'
        ordering = ['name']  # Sort groups alphabetically

    def __str__(self):
        return self.name

class WasteType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    hazardous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_waste_type'

    def __str__(self):
        return self.name

class WasteGenerator(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255, null=True, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)
    group = models.ForeignKey(WasteGeneratorGroup, on_delete=models.SET_NULL, null=True, blank=True)
    waste_specification = models.ForeignKey(WasteType, on_delete=models.SET_NULL, null=True, blank=True)
    contact_person = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_waste_generator'

    def __str__(self):
        return self.name

class WasteCollector(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_waste_collector'

    def __str__(self):
        return self.name

class WasteCollection(models.Model):
    waste_generator = models.ForeignKey(WasteGenerator, on_delete=models.CASCADE)
    waste_collector = models.ForeignKey(WasteCollector, on_delete=models.CASCADE)
    waste_type = models.ForeignKey(WasteType, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    collection_date = models.DateTimeField()
    status = models.CharField(max_length=50)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_waste_collection'

    def __str__(self):
        return f"{self.waste_generator} - {self.collection_date}"

class UserRole(models.Model):
    ROLE_CHOICES = [
        ('auditor', 'Auditor'),
        ('data_manager', 'Data Manager'),
        # Add other roles as needed
    ]
    
    name = models.CharField(max_length=100, choices=ROLE_CHOICES)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='roles', null=True)  # Making it nullable temporarily
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['name', 'organization']

    def __str__(self):
        return f"{self.get_name_display()} - {self.organization.name if self.organization else 'No Organization'}"

class ModulePermission(models.Model):
    MODULE_CHOICES = [
        ('manage_commodity', 'Manage Commodity'),
        ('manage_entities', 'Manage Entities'),
        ('manage_agreements', 'Manage Agreements'),
        ('audit', 'Audit'),
        ('schedule_audit', 'Schedule Audit'),
        ('reports', 'Reports'),
    ]

    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, related_name='module_permissions')
    module = models.CharField(max_length=50, choices=MODULE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['role', 'module']

    def __str__(self):
        return f"{self.role.name} - {self.get_module_display()}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='user_profiles', null=True)  # Making it nullable temporarily
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s Profile"

class Permission(models.Model):
    name = models.CharField(max_length=100)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class RolePermission(models.Model):
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('role', 'permission')

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"
