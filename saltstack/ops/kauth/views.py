from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse

from kauth.settings import TITLES


def login(request):
    errno = 0
    if request.method == 'POST':
        next = request.POST.get('next', '/')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            request.session['TITLES'] = TITLES
            return redirect(next)
        else:
            errno = 1
    else:
        next = request.GET.get('next', '/')

    return render(request, 'kauth/login.html', {'errno': errno, 'next': next})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('kauth:login'))


@login_required
def updatePassword(request):
    errno = 1
    newPassword = request.GET.get('newPassword', '')
    confirmPassword = request.GET.get('confirmPassword', '')
    if newPassword != '' and newPassword == confirmPassword:
        user = request.user
        user.set_password(newPassword)
        user.save()
        update_session_auth_hash(request, user)
        errno = 0

    return JsonResponse({'errno': errno, 'error': '', 'data': ''})
