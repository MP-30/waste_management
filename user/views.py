from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserProfileForm, InitialLoginForm  # Import InitialLoginForm
from .models import UserProfile
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import uuid
from django.contrib.auth import update_session_auth_hash
from django.utils.encoding import force_str
from django.contrib.auth.hashers import check_password
from core.models import Organization
from core.models import UserRole


def activate(request, uidb64, token):
    try:
        # Decode UID and convert it to a string safely
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = get_object_or_404(User, pk=int(uid))  # Get user by ID
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Invalid activation link.")
        return redirect("login")

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        request.session["activated_user_id"] = user.id

        messages.success(request, "Account activated successfully! Please log in.")
        return redirect("initial_login")  # Redirect to initial login form
    else:
        messages.error(request, "Invalid or expired activation link.")
        return redirect("login")
    
def initial_login(request):
    user_id = request.session.get("activated_user_id")  

    if not user_id:  # No activated user in session
        messages.error(request, "Session expired or invalid request. Please log in.")
        return redirect("login")

    # Get the user from the session
    user = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        form = InitialLoginForm(request.POST)
        if form.is_valid():
            temporary_password = form.cleaned_data["temporary_password"]
            new_password = form.cleaned_data.get("new_password1")

            print(f"Received temp password: {temporary_password}")

            if check_password(temporary_password, user.password):
                user.set_password(new_password)
                user.save()

                # Create default organization for the user
                organization = Organization.objects.create(
                    name=f"{user.username}'s Organization",
                    address="",
                    contact_person=user.username,
                    contact_email=user.email,
                    contact_phone="",
                    owner=user
                )

                # Clear session to avoid reuse
                del request.session["activated_user_id"]

                messages.success(request, "Your password has been updated successfully! Please log in.")
                return redirect("login")  
            else:
                print(f"Password mismatch for user: {user.username}")
                messages.error(request, "Invalid temporary password.")
    else:
        form = InitialLoginForm()

    return render(request, "user/initial_login.html", {"form": form})
    # return render(request, "user/login.html", {'form':form})

'''
            form.save()
            user.set_password(form.cleaned_data["new_password1"])  # Set new password
            user.save()
            update_session_auth_hash(request, user)  # Keep user logged in after password change
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("dashboard")  # Redirect to dashboard
    else:
        form = InitialLoginForm(instance=user_profile)

    return render(request, "user/initial_login.html", {"form": form})
'''
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # First check if user is an organization owner (admin)
            is_admin = Organization.objects.filter(owner=user).exists()
            if is_admin:
                # Create or get core profile for admin
                from core.models import UserProfile as CoreUserProfile
                organization = Organization.objects.filter(owner=user).first()
                CoreUserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'organization': organization,
                        'is_active': True
                    }
                )
                return redirect('admin_dashboard')
            
            # If not admin, check for role-based access
            try:
                from core.models import UserProfile as CoreUserProfile
                core_profile = CoreUserProfile.objects.get(user=user)
                if core_profile.role:
                    return redirect('user_dashboard')
                else:
                    return redirect('admin_dashboard')
            except CoreUserProfile.DoesNotExist:
                # Create core profile if it doesn't exist
                organization = Organization.objects.filter(owner=user).first()
                if organization:
                    CoreUserProfile.objects.create(
                        user=user,
                        organization=organization,
                        is_active=True
                    )
                return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "user/login.html")

def user_logout(request):
    messages.success(request, "Logged out successfully.")
    return render(request, "user/logout.html")


@login_required
def dashboard(request):
    # First check if user is an organization owner (admin)
    is_admin = Organization.objects.filter(owner=request.user).exists()
    if is_admin:
        # Create or get core profile for admin
        from core.models import UserProfile as CoreUserProfile
        organization = Organization.objects.filter(owner=request.user).first()
        CoreUserProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'organization': organization,
                'is_active': True
            }
        )
        return redirect('admin_dashboard')
    
    # If not admin, check for role-based access
    try:
        from core.models import UserProfile as CoreUserProfile
        core_profile = CoreUserProfile.objects.get(user=request.user)
        if core_profile.role:
            return redirect('user_dashboard')
        else:
            return redirect('admin_dashboard')
    except CoreUserProfile.DoesNotExist:
        # Create core profile if it doesn't exist
        organization = Organization.objects.filter(owner=request.user).first()
        if organization:
            CoreUserProfile.objects.create(
                user=request.user,
                organization=organization,
                is_active=True
            )
        return redirect('admin_dashboard')
