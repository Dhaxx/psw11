from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem')
            return redirect('/usuarios/cadastro')
        elif len(senha) < 6:
            messages.error(request, 'A senha deve ter no mínimo 6 caracteres')
            return redirect('/usuarios/cadastro')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuário já cadastrado')
            return redirect('/usuarios/cadastro')
        
        user = User.objects.create_user(username=username, password=senha)

        return redirect('/usuarios/login')
        
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

    user = auth.authenticate(username=username, password=senha)

    if user:
        auth.login(request, user)
        return redirect('/empresarios/cadastrar_empresa')
    
    messages.error(request, 'Usuário ou senha inválidos')
    return redirect('/usuarios/login')