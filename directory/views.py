from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Student
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomRegisterForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.http import require_POST



def home(request):
    if request.method == 'POST' and 'login_submit' in request.POST:
        # Handle login form submit
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home after login
    elif request.method == 'POST' and 'logout_submit' in request.POST:
        # Handle logout submit
        logout(request)
        return redirect('home')

    if request.user.is_authenticated:
        # Show student list + add/update/delete links on home page

        query = request.GET.get('q', '').strip()
        students = Student.objects.all()
        if query:
            students = students.filter(name__icontains=query)  # example filter

        return render(request, 'directory/home.html', {
            'students': students,
            'user': request.user,
        })
    else:
        # Show login form on home page
        form = AuthenticationForm()
        return render(request, 'directory/home.html', {
            'login_form': form,
        })
def student_list(request):
    query = request.GET.get('q', '').strip()
    semester = request.GET.get('semester', '').strip()
    faculty = request.GET.get('department', '').strip()
    section = request.GET.get('section', '').strip()  # optional section filter

    students = Student.objects.all()
    searched = False

    # If any search or filter input is provided
    if query or semester or faculty or section:
        searched = True

        if query:
            students = students.filter(
                Q(name__icontains=query) | Q(roll_number__icontains=query)
            )

        if semester:
            students = students.filter(semester__icontains=semester)

        if faculty:
            students = students.filter(faculty__icontains=faculty)

        if section:
            students = students.filter(section__icontains=section)

    return render(request, 'students/student_list.html', {
        'students': students,
        'searched': searched,
        'query': query,
        'semester': semester,
        'faculty': faculty,
        'section': section,
    })

def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()

            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomRegisterForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def add_student(request):
    form = StudentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'directory/student_form.html', {'form': form})

@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def update_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    form = StudentForm(request.POST or None, instance=student)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'directory/student_form.html', {'form': form})

@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'directory/confirm_delete.html', {'student': student})
@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home, which shows login form for unauthenticated users

