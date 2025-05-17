from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from users.models import User
from users.utils import (
    hash_password,
    validate_first_last_name,
    validate_id_number,
    validate_credit_card_number,
    validate_valid_date,
    validate_cvc,
    contains_forbidden_chars,
    contains_forbidden_query
)

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        hashed_password = hash_password(password)

        try:
            user = User.objects.get(username=username, password_hash=hashed_password)
            request.session['user_id'] = user.id
            request.session['role'] = user.role
            print(f"✅ התחברת כ: {user.username}, תפקיד: {user.role}")

            if user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def login_injection_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if contains_forbidden_chars(username) or contains_forbidden_chars(password):
            return render(request, 'login.html')

        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                    SELECT id, role FROM users 
                    WHERE username = ? AND password_hash = ?
                """, (username, password))
                result = cursor.fetchone()
            except Exception as e:
                messages.error(request, f"Database error: {str(e)}")
                return render(request, 'login.html')

        if result:
            user_id, role = result
            request.session['user_id'] = user_id
            request.session['role'] = role
            if role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def query_injection_view(request):
    data = None
    if request.method == 'POST':
        raw_query = request.POST.get('query')

        if contains_forbidden_query(raw_query):
            data = ["Illegal SQL detected. Request blocked."]
        else:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(raw_query)
                    try:
                        data = cursor.fetchall()
                    except:
                        data = ["Query executed successfully (no results)."]
                except Exception as e:
                    data = [f"Error: {str(e)}"]

    return render(request, 'query_injection.html', {'data': data})

def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username)
            user.password_hash = hash_password(new_password)
            user.save()
            messages.success(request, "Password reset successful. You can now login.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "Username not found.")

    return render(request, 'reset_password.html')

def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect('login')

def admin_dashboard(request):
    if request.session.get('role') != 'admin':
        return redirect('login')

    users = None
    if request.method == 'POST':
        if 'show_data' in request.POST:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT first_name, last_name, id_number, credit_card_number, valid_date, cvc, username, is_admin
                    FROM users
                """)
                users = cursor.fetchall()
        elif 'hide_data' in request.POST:
            users = None

    return render(request, 'admin_dashboard.html', {'users': users})

def user_dashboard(request):
    return render(request, 'user_dashboard.html')
