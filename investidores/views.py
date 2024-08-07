from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from empresarios.models import Empresa


# Create your views here.
@login_required
def sugestao(request):
    areas = Empresa.area_choices
    if request.method == 'GET':
        return render (request, 'sugestao.html', {'areas': areas})
    elif request.method == 'POST':
        tipo = request.POST.get('tipo')
        area = request.POST.getlist('area')
        valor = request.POST.get('valor')

        if tipo == 'C':
            empresas = Empresa.objects.filter(tempo_exisencia ='+5', estagio="E")
        elif tipo == 'D':
            empresas = Empresa.objects.exclude(tempo_existencia ='+5', estagio="E")
        
        empresas = empresas.filter(area__in=area)

        empresas_selecionadas = []
        for empresa in empresas:
            percentual = (float(valor) * 100) / float(empresa.valor)
            if percentual > 1:
                empresas_selecionadas.append(empresa)
        
        return render(request, 'sugestao.html', {'areas': areas, 'empresas': empresas_selecionadas})