from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import UserProfileForm
from .models import UserProfile
from django.conf import settings

# Signup with Email Verification
def user_signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("signup")

        user = User.objects.create_user(username=username, email=email, password=password, is_active=False)

        # Generate email verification token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verification_link = request.build_absolute_uri(reverse('verify_email', kwargs={'uidb64': uid, 'token': token}))

        # Send email
        subject = "Email Verification - Waste Management"
        message = render_to_string("user/email_verification.html", {"username": user.username, "verification_link": verification_link})
        # send_mail(subject, message, "your_email@gmail.com", [email], fail_silently=False)
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)


        messages.success(request, "Check your email to verify your account!")
        return redirect("login")

    return render(request, "user/signup.html")


# Email Verification View
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            # Create a corresponding UserProfile instance
            UserProfile.objects.create(user=user)  # Associate the user with a profile

            messages.success(request, "Email verified! You can now complete your profile.")
            return redirect("complete_profile")
        else:
            messages.error(request, "Invalid verification link.")
            return redirect("signup")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Invalid verification link.")
        return redirect("signup")

from django.contrib.auth.decorators import login_required

def complete_profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user.userprofile)  # Pass the user's profile to the form
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("dashboard")
    else:
        try:
            form = UserProfileForm(instance=request.user.userprofile)  # Get the user's profile
        except UserProfile.DoesNotExist:
            # Handle case where a profile doesn't exist (shouldn't happen after verification)
            UserProfile.objects.create(user=request.user)
            form = UserProfileForm(instance=request.user.userprofile)

    return render(request, "user/complete_profile.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")  # Redirect to the dashboard after login
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, "user/login.html")

from django.contrib.auth.decorators import login_required



@login_required
def dashboard(request):
    # Your dashboard logic here. i will add in future
    return render(request, "user/dashboard.html")


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return render(request, "login.html")
