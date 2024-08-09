from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from empresarios.models import Empresa, Documento
from .models import PropostaInvestimento
from django.contrib import messages

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
    
@login_required
def ver_empresa(request, empresa_id):
    empresa = Empresa.objects.get(id=empresa_id)
    documentos = Documento.objects.filter(empresa=empresa)

    proposta_investimentos = PropostaInvestimento.objects.filter(empresa=empresa, status='PA')
    percentual_vendido = 0
    for pi in proposta_investimentos:
        percentual_vendido += pi.percentual

    limiar = 80 * empresa.percentual_equity / 100
    concretizado = False

    if percentual_vendido >= limiar:
        concretizado = True

    percentual_disponivel = empresa.percentual_equity - percentual_vendido

    return render(request, 'ver_empresa.html', {'empresa': empresa, 'documentos': documentos, 'concretizado': concretizado, 'percentual_disponivel': percentual_disponivel})

@login_required
def realizar_proposta(request, id):
    valor = request.POST.get('valor')
    percentual = request.POST.get('percentual')
    empresa = Empresa.objects.get(id=id)

    propostas_aceitas = PropostaInvestimento.objects.filter(empresa=empresa, status='PA')
    total = 0

    for pa in propostas_aceitas:
        total += pa.valor

    if total + int(percentual) > empresa.percentual_equity:
        messages.warning(request, 'O percentual solicitado ultrapassa o percentual máximo.')
        return redirect(f'/investidores/ver_empresa/{id}')
    
    valuation = (100 * int(valor)) / int(percentual)

    if valuation < (int(empresa.valuation) / 2):
        messages.warning(request, f'Seu valuation proposto foi R${valuation} e deve ser no mínimo R${empresa.valuation/2}')
        return redirect(f'/investidores/ver_empresa/{id}')
    
    pi = PropostaInvestimento(valor=valor, percentual=percentual, empresa=empresa, investidor=request.user)
    pi.save()

    return redirect(f'/investidores/assinar_contrato/{pi.id}')

@login_required
def assinar_contrato(request, id):
    pi = PropostaInvestimento.objects.get(id=id)
    if pi.status != "AS":
        raise Http404()
    
    if request.method == "GET":
        return render(request, 'assinar_contrato.html', {'id': id})
    elif request.method == "POST":
        selfie = request.FILES.get('selfie')
        rg = request.FILES.get('rg')
        print(request.FILES)
        

        pi.selfie = selfie
        pi.rg = rg
        pi.status = 'PE'
        pi.save()

        messages.success(request, 'Contrato assinado com sucesso.')
        return redirect(f'/investidores/ver_empresa/{pi.empresa.id}')
