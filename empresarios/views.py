from django.shortcuts import render, redirect
from .models import Empresa
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required
def cadastrar_empresa(request):
    if request.method == 'GET':
        return render(request, 'cadastrar_empresa.html', {'tempo_existencia': Empresa.tempo_existencia_choices, 'area_choices': Empresa.area_choices})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        site = request.POST.get('site')
        tempo_existencia = request.POST.get('tempo_existencia')
        descricao = request.POST.get('descricao')
        date = request.POST.get('date')
        number = request.POST.get('number')
        estagio = request.POST.get('estagio')
        area = request.POST.get('area')
        publico_alvo = request.POST.get('publico_alvo')
        valor = request.POST.get('valor')
        pitch = request.FILES.get('pitch')
        logo = request.FILES.get('logo')

        empresa = Empresa(
            user = request.user,
            nome=nome,
            cnpj=cnpj,
            site=site,
            tempo_existencia=tempo_existencia,
            descricao=descricao,
            data_final_captacao=date,
            percentual_equity=number,
            estagio=estagio,
            area=area,
            publico_alvo=publico_alvo,
            valor=valor,
            pitch=pitch,
            logo=logo
        )

        empresa.save()

        messages.success(request, 'Empresa cadastrada com sucesso!')
        return redirect('/empresarios/cadastrar_empresa')