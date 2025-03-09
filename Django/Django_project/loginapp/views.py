from django.shortcuts import render, redirect
from django.http import HttpResponse

# Simulated user storage (this resets when the server restarts)
user_credentials = {"admin": "admin123"}

def signup(request):
    """Handles user signup"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username in user_credentials:
            return HttpResponse("Username already exists. Please choose another one.")
        
        # Store the user
        user_credentials[username] = password
        return redirect("login")  # Redirect to login page after signup
    
    return render(request, "signup.html")

def login(request):
    """Handles user login"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username in user_credentials and user_credentials[username] == password:
            request.session["user"] = username  # Store user session
            return redirect("userpage")  # Redirect to user dashboard
        
        return HttpResponse("Invalid username or password. Try again.")

    return render(request, "login.html")

def userpage(request):
    """User dashboard page"""
    if "user" not in request.session:
        return redirect("login")  # Redirect to login if not authenticated
    
    username = request.session["user"]
    return render(request, "userpage.html", {"user": username})

def logout(request):
    """Handles user logout"""
    request.session.flush()  # Clears session
    return redirect("login")  # Redirect to login page