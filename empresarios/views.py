from django.shortcuts import render, redirect
from .models import Empresa
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re

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
        data_final = request.POST.get('data_final')
        percentual_equity = request.POST.get('percentual_equity')
        estagio = request.POST.get('estagio')
        area = request.POST.get('area')
        publico_alvo = request.POST.get('publico_alvo')
        valor = request.POST.get('valor')
        pitch = request.POST.get('pitch')
        pitch = request.FILES.get('pitch')
        logo = request.FILES.get('logo')

        if not nome or not cnpj or not site or not tempo_existencia or not descricao or not data_final or not percentual_equity or not estagio or not area or not publico_alvo or not valor or not pitch or not logo:
            messages.error(request, 'Todos os campos são obrigatórios!')
            return render(request, 'cadastrar_empresa.html', {'tempo_existencia': Empresa.tempo_existencia_choices, 'area_choices': Empresa.area_choices})
        
        if not re.match(r'^\d{14}$', cnpj):
            messages.error(request, 'CNPJ inválido!')
            return redirect('/empresarios/cadastrar_empresa')
        
        try:
            valor = float(valor)
            if valor <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, 'Valor inválido!')
            return redirect('/empresarios/cadastrar_empresa')
        
        if pitch and pitch.size > 5 * 1024 * 1024 or logo and logo.size > 5 * 1024 * 1024:
            messages.error(request, 'Os Arquivos devem ter no máximo 5MB!')
            return redirect('/empresarios/cadastrar_empresa')
        
        if pitch.content_type != 'application/pdf':
            messages.error(request, 'O pitch deve ser um arquivo PDF!')
            return redirect('/empresarios/cadastrar_empresa')
        
        if logo.content_type not in ['image/jpeg', 'image/png', 'image/jpg', 'image/svg']:
            messages.error(request, 'O logo deve ser uma imagem JPEG, JPG, PNG ou SVG!')
            return redirect('/empresarios/cadastrar_empresa')

        empresa = Empresa(
            user = request.user,
            nome=nome,
            cnpj=cnpj,
            site=site,
            tempo_existencia=tempo_existencia,
            descricao=descricao,
            data_final_captacao=data_final,
            percentual_equity=percentual_equity,
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