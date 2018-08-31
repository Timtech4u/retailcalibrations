from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from calibrate.models import Calibration, Profile
from calibrate.forms import CalibrationForm, UserForm, SuperUserForm, AdminStaffUserForm
from calibration.forms import EditProfileForm
#from django.contrib.auth.models import User 
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required


class CalibrationList(LoginRequiredMixin, ListView):
    model = Calibration

class CalibrationCreate(LoginRequiredMixin, CreateView):
    model = Calibration
    form_class = CalibrationForm
    success_url = reverse_lazy('calibrate:calibration_list')

class CalibrationUpdate(LoginRequiredMixin, UpdateView):
    model = Calibration
    form_class = CalibrationForm
    success_url = reverse_lazy('calibrate:calibration_list')

class CalibrationDelete(LoginRequiredMixin, DeleteView):
    model = Calibration
    success_url = reverse_lazy('calibrate:calibration_list')

@login_required
def profile(request):
    args = {'user': request.user}
    return render(request, 'registration/profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance = request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance = request.user)
        args = {'form':form}
        return render(request, 'registration/edit_profile.html', args)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data =request.POST, user = request.user)

        if form.is_valid():
            update_session_auth_hash(request, form.user)
            form.save()
            return redirect('login')
        else:
            return redirect('change_password')
    else:
        form = PasswordChangeForm(user = request.user)
        args = {'form':form}
        return render(request, 'registration/change_password.html', args)

    

@login_required
def staff_list(request):
    context = {}
    context['users'] = User.objects.all()
    context['title'] = 'Staffs'
    return render(request, 'staffs/index.html', context)

@login_required
def staff_details(request, id=None):
    context = {}
    context['user'] = get_object_or_404(User, id=id)
    return render(request, 'staffs/details.html', context)


@login_required
def staff_add(request):
    context = {}
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        context['user_form'] = user_form
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('calibrate:staff_list'))
        else:
            return render(request, 'staffs/add.html', context)
    else: 
        user_form = UserForm()
        context['user_form'] = user_form
        return render(request, 'staffs/add.html', context)

# super staff add
@login_required
def superStaff_add(request):
    context = {}
    if request.method == 'POST':
        user_form = SuperUserForm(request.POST)
        context['user_form'] = user_form
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('calibrate:staff_list'))
        else:
            return render(request, 'staffs/add.html', context)
    else: 
        user_form = SuperUserForm()
        context['user_form'] = user_form
        return render(request, 'staffs/add.html', context)


#admin staff add
@login_required
def adminstaff_add(request):
    context = {}
    if request.method == 'POST':
        user_form = AdminStaffUserForm(request.POST)
        context['user_form'] = user_form
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('calibrate:staff_list'))
        else:
            return render(request, 'staffs/add.html', context)
    else: 
        user_form = AdminStaffUserForm()
        context['user_form'] = user_form
        return render(request, 'staffs/add.html', context)


@login_required
def staff_edit(request, id=None):
    user = get_object_or_404(User, id=id)
    if request.method =='POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('calibrate:staff_list'))
        else:
            return render(request, 'staffs/edit.html', {'user_form':user_form})
    else:
        user_form = UserForm(instance=user)
        return render(request, 'staffs/edit.html', {'user_form':user_form})


@login_required
def staff_delete(request, id=None):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        return HttpResponseRedirect(reverse('calibrate:staff_list'))
    else:
        context = {}
        context['user']=user
        return render(request, 'staffs/delete.html', context)