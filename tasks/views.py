from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Task
from .forms import StudentSignUpForm, TaskForm

# ==========================================
# 1. AUTHENTICATION VIEWS (Signup, Login, Logout)
# ==========================================

def signup_view(request):
    """
    New student account creation ke liye function-based view.
    GET request: Form display karega.
    POST request: Account create karega aur auto-login karake task list pe bhejega.
    """
    if request.user.is_authenticated:
        return redirect('task_list')

    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            # User ko database mein save kar rahe hain
            user = form.save()
            # New user ko auto login kara rahe hain
            login(request, user)
            messages.success(request, f"Welcome {user.username}! Aapka account successfully ban gaya hai.")
            return redirect('task_list')
        else:
            messages.error(request, "Registration fail ho gaya. Kripya details check karein.")
    else:
        form = StudentSignUpForm()

    return render(request, 'tasks/signup.html', {'form': form})


def login_view(request):
    """
    Student Login view (Django ka built-in AuthenticationForm use ho raha hai).
    """
    if request.user.is_authenticated:
        return redirect('task_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        # Custom styling input box ke liye
        form.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        form.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('task_list')
            else:
                messages.error(request, "Invalid username ya password.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()
        form.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        form.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})

    return render(request, 'tasks/login.html', {'form': form})


def logout_view(request):
    """
    User ko session se logout karega aur login page par bhej dega.
    """
    logout(request)
    messages.info(request, "Aap successfully logout ho gaye hain.")
    return redirect('login')


# ==========================================
# 2. TASK MANAGEMENT VIEWS (CRUD Operations)
# ==========================================

@login_required
def task_list(request):
    """
    Logged-in user ke saare tasks list karne aur filter karne ka view.
    Search, Priority Filter aur Status Filter support karta hai.
    """
    # Base Queryset: Sirf current logged-in user ke tasks fetch honge
    user_tasks = Task.objects.filter(user=request.user)

    # URL Parameters se filters read kar rahe hain
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    search_query = request.GET.get('search', '')

    # Status Filter apply karna
    if status_filter in ['Pending', 'Completed']:
        user_tasks = user_tasks.filter(status=status_filter)

    # Priority Filter apply karna
    if priority_filter in ['High', 'Medium', 'Low']:
        user_tasks = user_tasks.filter(priority=priority_filter)

    # Search query apply karna (title ya description mein search hoga)
    if search_query:
        user_tasks = user_tasks.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Summary Statistics calculate karna dashboard counter ke liye
    all_user_tasks = Task.objects.filter(user=request.user)
    total_count = all_user_tasks.count()
    pending_count = all_user_tasks.filter(status='Pending').count()
    completed_count = all_user_tasks.filter(status='Completed').count()

    context = {
        'tasks': user_tasks,
        'total_count': total_count,
        'pending_count': pending_count,
        'completed_count': completed_count,
        'current_status': status_filter,
        'current_priority': priority_filter,
        'search_query': search_query,
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_create(request):
    """
    Naya task add karne ka view.
    """
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # commit=False se object memory mein rehta hai, DB mein abhi save nahi hota
            task = form.save(commit=False)
            # Current logged-in user assign kar rahe hain
            task.user = request.user
            # Ab database mein final save karenge
            task.save()
            messages.success(request, "Naya task successfully add ho gaya!")
            return redirect('task_list')
        else:
            messages.error(request, "Form mein kuch galatiyan hain. Kripya dubara check karein.")
    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'page_title': 'Add New Task',
        'button_text': 'Create Task'
    })


@login_required
def task_update(request, task_id):
    """
    Existing task ko update/edit karne ka view.
    get_object_or_404 se check hota hai ki task exist karta hai aur user ka apna task hai.
    """
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task successfully update ho gaya!")
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'page_title': 'Edit Task',
        'button_text': 'Update Task',
        'is_edit': True
    })


@login_required
def task_delete(request, task_id):
    """
    Task ko delete karne ka view with confirmation prompt.
    """
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        task.delete()
        messages.success(request, "Task successfully delete kar diya gaya.")
        return redirect('task_list')

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@login_required
def task_toggle_status(request, task_id):
    """
    Quick Action View: Task ko Pending se Completed ya Completed se Pending toggle karta hai.
    """
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if task.status == 'Pending':
        task.status = 'Completed'
        messages.success(request, f"'{task.title}' complete ho gaya!")
    else:
        task.status = 'Pending'
        messages.info(request, f"'{task.title}' wapas pending status mein set ho gaya.")

    task.save()
    return redirect('task_list')
