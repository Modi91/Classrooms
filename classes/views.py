from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import Classroom, Student
from .forms import ClassroomForm, SignupForm, SigninForm, StudentForm

def classroom_list(request):
    classrooms = Classroom.objects.all()
    context = {
        "classrooms": classrooms,
    }
    return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    students = Student.objects.filter(classroom=classroom).order_by('name', '-exam_grade')
    context = {
        "classroom": classroom,
        "students": students,
    }
    return render(request, 'classroom_detail.html', context)


def classroom_create(request):
    if request.user.is_anonymous:
        return redirect('signin')
    form = ClassroomForm()
    if request.method == "POST":
        form = ClassroomForm(request.POST, request.FILES or None)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.teacher = request.user
            classroom.save()
            messages.success(request, "Successfully Created!")
            return redirect('classroom-list')
        print (form.errors)
    context = {
    "form": form,
    }
    return render(request, 'create_classroom.html', context)


def classroom_update(request, classroom_id):
    if request.user.is_anonymous:
        return redirect('signin')
    classroom = Classroom.objects.get(id=classroom_id)
    form = ClassroomForm(instance=classroom)
    if request.method == "POST":
        form = ClassroomForm(request.POST, request.FILES or None, instance=classroom)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Edited!")
            return redirect('classroom-list')
        print (form.errors)
    context = {
    "form": form,
    "classroom": classroom,
    }
    return render(request, 'update_classroom.html', context)


def classroom_delete(request, classroom_id):
    if not(request.user==student.classroom.teacher):
        messages.success(request, 'you are not autherized!')
        return redirect('classroom-list')
    Classroom.objects.get(id=classroom_id).delete()
    messages.success(request, "Successfully Deleted!")
    return redirect('classroom-list')


def add_student(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    if not(request.user==classroom.teacher):
        messages.success(request, 'you are not autherized!')
        return redirect('classroom-list')
    form = StudentForm()
    classroom = Classroom.objects.get(id=classroom_id)
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES or None)
        if form.is_valid():
            student = form.save(commit=False)
            student.classroom = classroom
            student.save()
            messages.success(request, "Student added Successfully!")
            return redirect('classroom-detail', classroom_id)
        print (form.errors)
    context = {
    "form": form,
    "classroom": classroom,
    }
    return render(request, 'add_student.html', context)

def student_update(request, student_id):
    student = Student.objects.get(id=student_id)
    if not(request.user==student.classroom.teacher):
        messages.success(request, 'you are not autherized!')
        return redirect('classroom-list')
    form = StudentForm(instance=student)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated!")
            return redirect('classroom-detail', classroom_id=student.classroom.id)
        print (form.errors)
    context = {
    "form": form,
    "student": student,
    }
    return render(request, 'student_update.html', context)

def student_delete(request, classroom_id, student_id):
    student = Student.objects.get(id=student_id)
    if not(request.user==student.classroom.teacher):
        messages.success(request, 'you are not autherized!')
        return redirect('classroom-list')

    class_id = student.classroom.id
    student.delete()
    
    messages.success(request, "Successfully Deleted!")
    return redirect('classroom-detail', classroom_id=class_id)

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect('classroom-list')
            messages.success(request, "Welcome!")
        messages.warning(request, form.errors)
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)


def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('classroom-list')
                messages.success(request, "Welcome back!")
            messages.success(request, "Incorrect Username or password!")
        messages.warning(request, form.errors)
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)


def signout(request):
    logout(request)
    return redirect("signin")