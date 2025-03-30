from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WasteGenerator, WasteCollector, WasteType, Organization, WasteGeneratorGroup, UserRole, UserProfile, Permission, ModulePermission
from .forms import (
    WasteGeneratorForm,
    WasteCollectorForm,
    WasteTypeForm,
    OrganizationSettingsForm,
    UserForm,
    UserEditForm,
    RoleForm,
    PermissionForm,
    RolePermissionForm
)
from django.db.models import Count
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.

# Waste Generator Views
@login_required
def waste_generator_list(request):
    generators = WasteGenerator.objects.filter(organization__owner=request.user)
    return render(request, 'core/waste_generator/list.html', {'generators': generators})

@login_required
def waste_generator_add(request):
    if request.method == 'POST':
        form = WasteGeneratorForm(request.POST)
        if form.is_valid():
            generator = form.save(commit=False)
            generator.organization = request.user.owned_organizations.first()
            generator.save()
            messages.success(request, 'Waste Generator added successfully.')
            return redirect('waste_generator_list')
    else:
        form = WasteGeneratorForm()
    return render(request, 'core/waste_generator/form.html', {'form': form, 'title': 'Add Waste Generator'})

@login_required
def waste_generator_edit(request, pk):
    generator = get_object_or_404(WasteGenerator, pk=pk, organization__owner=request.user)
    if request.method == 'POST':
        form = WasteGeneratorForm(request.POST, instance=generator)
        if form.is_valid():
            form.save()
            messages.success(request, 'Waste Generator updated successfully.')
            return redirect('waste_generator_list')
    else:
        form = WasteGeneratorForm(instance=generator)
    return render(request, 'core/waste_generator/form.html', {'form': form, 'title': 'Edit Waste Generator'})

@login_required
def waste_generator_delete(request, pk):
    generator = get_object_or_404(WasteGenerator, pk=pk, organization__owner=request.user)
    if request.method == 'POST':
        generator.delete()
        messages.success(request, 'Waste Generator deleted successfully.')
        return redirect('waste_generator_list')
    return render(request, 'core/waste_generator/delete.html', {'generator': generator})

@login_required
def waste_generator_dashboard(request):
    # Get current month's start date
    today = timezone.now()
    month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Get all waste generators for the current user's organization
    generators = WasteGenerator.objects.filter(organization__owner=request.user)
    
    # Calculate statistics
    context = {
        'generators': generators,  # Add the generators queryset to the context
        'total_generators': generators.count(),
        'active_generators': generators.filter(is_active=True).count(),
        'generator_groups': WasteGeneratorGroup.objects.count(),
        'new_this_month': generators.filter(created_at__gte=month_start).count(),
        'recent_generators': generators.select_related('group').order_by('-created_at')[:5],
    }
    
    # Get group distribution data
    group_stats = generators.values('group__name').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context['group_labels'] = [stat['group__name'] or 'Unassigned' for stat in group_stats]
    context['group_data'] = [stat['count'] for stat in group_stats]
    
    return render(request, 'dashboard/waste_generator_dashboard.html', context)

@login_required
def waste_generator_groups(request):
    groups = WasteGeneratorGroup.objects.all().order_by('name')
    return render(request, 'core/waste_generator/groups.html', {'groups': groups})

@login_required
def waste_generator_reports(request):
    return render(request, 'core/waste_generator/reports.html')

@login_required
def waste_generator_import(request):
    if request.method == 'POST':
        # Handle file import logic here
        messages.success(request, 'Generators imported successfully.')
        return redirect('waste_generator_list')
    return render(request, 'core/waste_generator/import.html')

@login_required
def waste_generator_export(request):
    # Add export logic here
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="waste_generators.csv"'
    return response

# Waste Collector Views
@login_required
def waste_collector_list(request):
    collectors = WasteCollector.objects.filter(organization__owner=request.user)
    return render(request, 'core/waste_collector/list.html', {'collectors': collectors})

@login_required
def waste_collector_add(request):
    if request.method == 'POST':
        form = WasteCollectorForm(request.POST)
        if form.is_valid():
            collector = form.save(commit=False)
            collector.organization = request.user.owned_organizations.first()
            collector.save()
            messages.success(request, 'Waste Collector added successfully.')
            return redirect('waste_collector_list')
    else:
        form = WasteCollectorForm()
    return render(request, 'core/waste_collector/form.html', {'form': form, 'title': 'Add Waste Collector'})

@login_required
def waste_collector_edit(request, pk):
    collector = get_object_or_404(WasteCollector, pk=pk, organization__owner=request.user)
    if request.method == 'POST':
        form = WasteCollectorForm(request.POST, instance=collector)
        if form.is_valid():
            form.save()
            messages.success(request, 'Waste Collector updated successfully.')
            return redirect('waste_collector_list')
    else:
        form = WasteCollectorForm(instance=collector)
    return render(request, 'core/waste_collector/form.html', {'form': form, 'title': 'Edit Waste Collector'})

@login_required
def waste_collector_delete(request, pk):
    collector = get_object_or_404(WasteCollector, pk=pk, organization__owner=request.user)
    if request.method == 'POST':
        collector.delete()
        messages.success(request, 'Waste Collector deleted successfully.')
        return redirect('waste_collector_list')
    return render(request, 'core/waste_collector/delete.html', {'collector': collector})

# Waste Type Views
@login_required
def waste_type_list(request):
    types = WasteType.objects.all()
    return render(request, 'core/waste_type/list.html', {'types': types})

@login_required
def waste_type_add(request):
    if request.method == 'POST':
        form = WasteTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Waste Type added successfully.')
            return redirect('waste_type_list')
    else:
        form = WasteTypeForm()
    return render(request, 'core/waste_type/form.html', {'form': form, 'title': 'Add Waste Type'})

@login_required
def waste_type_edit(request, pk):
    waste_type = get_object_or_404(WasteType, pk=pk)
    if request.method == 'POST':
        form = WasteTypeForm(request.POST, instance=waste_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Waste Type updated successfully.')
            return redirect('waste_type_list')
    else:
        form = WasteTypeForm(instance=waste_type)
    return render(request, 'core/waste_type/form.html', {'form': form, 'title': 'Edit Waste Type'})

@login_required
def waste_type_delete(request, pk):
    waste_type = get_object_or_404(WasteType, pk=pk)
    if request.method == 'POST':
        waste_type.delete()
        messages.success(request, 'Waste Type deleted successfully.')
        return redirect('waste_type_list')
    return render(request, 'core/waste_type/delete.html', {'waste_type': waste_type})

# Organization Settings View
@login_required
def organization_settings(request):
    organization = Organization.objects.filter(owner=request.user).first()
    
    if not organization:
        # Create a default organization if none exists
        organization = Organization.objects.create(
            name=f"{request.user.username}'s Organization",
            address="",
            contact_person=request.user.username,
            contact_email=request.user.email,
            contact_phone="",
            owner=request.user
        )
        messages.info(request, "A default organization has been created for you.")
    
    if request.method == 'POST':
        form = OrganizationSettingsForm(request.POST, instance=organization)
        if form.is_valid():
            form.save()
            messages.success(request, 'Organization settings updated successfully.')
            return redirect('organization_settings')
    else:
        form = OrganizationSettingsForm(instance=organization)
    return render(request, 'core/organization/settings.html', {'form': form})

@login_required
def admin_dashboard(request):
    # Get the organization context
    organization = None
    if hasattr(request.user, 'owned_organizations'):
        organization = request.user.owned_organizations.first()
    elif hasattr(request.user, 'profile'):
        organization = request.user.profile.organization

    if not organization:
        messages.error(request, "No organization found.")
        return redirect('admin_dashboard')

    context = {
        'organization': organization,
        'total_waste_generators': WasteGenerator.objects.filter(organization=organization).count(),
        'total_waste_collectors': WasteCollector.objects.filter(organization=organization).count(),
        'total_users': UserProfile.objects.filter(organization=organization).count(),
        'total_roles': UserRole.objects.filter(organization=organization).count()
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)

# User Management Views
@login_required
def user_dashboard(request):
    # Get the organization context
    organization = None
    if hasattr(request.user, 'owned_organizations'):
        organization = request.user.owned_organizations.first()
    elif hasattr(request.user, 'profile'):
        organization = request.user.profile.organization

    if not organization:
        messages.error(request, "No organization found.")
        return redirect('admin_dashboard')

    # Get all users associated with the organization
    user_profiles = UserProfile.objects.filter(organization=organization).select_related('user', 'role')
    
    context = {
        'user_profiles': user_profiles,
        'total_users': user_profiles.count(),
        'active_users': user_profiles.filter(is_active=True).count(),
        'total_roles': UserRole.objects.filter(organization=organization).count(),
        'organization': organization
    }
    
    return render(request, 'core/user/dashboard.html', context)

@login_required
def user_add(request):
    try:
        organization = request.user.profile.organization
        if not organization:
            messages.error(request, "No organization assigned. Cannot add users.")
            return redirect('user_dashboard')

        if request.method == 'POST':
            form = UserForm(request.POST, request.FILES, organization=organization)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = form.cleaned_data['email']  # Using email as username
                user.save()
                
                # Create user profile
                UserProfile.objects.create(
                    user=user,
                    organization=organization,
                    role=form.cleaned_data['role'],
                    phone_number=form.cleaned_data['phone_number'],
                    profile_pic=form.cleaned_data['profile_pic'],
                    is_active=form.cleaned_data['is_active']
                )
                messages.success(request, 'User created successfully.')
                return redirect('user_dashboard')
        else:
            form = UserForm(organization=organization)
        
        return render(request, 'core/user/form.html', {'form': form, 'title': 'Add User'})
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found. Please contact your administrator.")
        return redirect('admin_dashboard')

@login_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            profile = user.profile
            profile.role = form.cleaned_data.get('role')
            profile.phone_number = form.cleaned_data.get('phone_number')
            if form.cleaned_data.get('profile_pic'):
                profile.profile_pic = form.cleaned_data.get('profile_pic')
            profile.save()
            messages.success(request, 'User updated successfully.')
            return redirect('user_dashboard')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'core/user/form.html', {'form': form, 'title': 'Edit User'})

@login_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('user_dashboard')
    return render(request, 'core/user/delete.html', {'user': user})

@login_required
def manage_role_permissions(request):
    try:
        organization = request.user.profile.organization
        if not organization:
            messages.error(request, "No organization assigned. Cannot manage permissions.")
            return redirect('user_dashboard')

        if request.method == 'POST':
            form = RolePermissionForm(request.POST, organization=organization)
            if form.is_valid():
                form.save()
                messages.success(request, 'Role permissions updated successfully.')
                return redirect('role_list')
        else:
            form = RolePermissionForm(organization=organization)
        
        roles = UserRole.objects.filter(organization=organization)
        return render(request, 'core/user/permissions.html', {
            'form': form,
            'roles': roles,
            'permissions': ModulePermission.MODULE_CHOICES
        })
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found. Please contact your administrator.")
        return redirect('admin_dashboard')

@login_required
def role_list(request):
    try:
        organization = request.user.profile.organization
        if organization:
            roles = UserRole.objects.filter(organization=organization)
        else:
            roles = UserRole.objects.none()
            messages.warning(request, "No organization assigned. Please contact your administrator.")
        
        return render(request, 'core/user/role_list.html', {'roles': roles})
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found. Please contact your administrator.")
        return redirect('admin_dashboard')

@login_required
def role_add(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Role added successfully.')
            return redirect('role_list')
    else:
        form = RoleForm()
    return render(request, 'core/user/role_form.html', {'form': form, 'title': 'Add Role'})

@login_required
def role_edit(request, pk):
    role = get_object_or_404(UserRole, pk=pk)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, 'Role updated successfully.')
            return redirect('role_list')
    else:
        form = RoleForm(instance=role)
    return render(request, 'core/user/role_form.html', {'form': form, 'title': 'Edit Role'})

@login_required
def role_delete(request, pk):
    role = get_object_or_404(UserRole, pk=pk)
    if request.method == 'POST':
        role.delete()
        messages.success(request, 'Role deleted successfully.')
        return redirect('role_list')
    return render(request, 'core/user/role_delete.html', {'role': role})

@login_required
def manage_permissions(request):
    permissions = Permission.objects.all()
    if request.method == 'POST':
        form = PermissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Permission added successfully.')
            return redirect('manage_permissions')
    else:
        form = PermissionForm()
    return render(request, 'core/user/permissions.html', {
        'permissions': permissions,
        'form': form
    })
