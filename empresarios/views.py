from django.shortcuts import render, redirect, HttpResponse
from .models import Empresa, Documento, Metrica
from investidores.models import PropostaInvestimento
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
    
@login_required   
def listar_empresas(request):
    if request.method == 'GET':
        empresas = Empresa.objects.filter(user=request.user)
        return render(request, 'listar_empresas.html', {'empresas': empresas})
    
@login_required
def empresa(request, nome_empresa):
    empresa = Empresa.objects.get(nome=nome_empresa)
    if empresa.user != request.user:
        messages.error(request, 'Você não tem permissão para acessar esta empresa!')
        return redirect('/usuarios/login')

    if request.method == 'GET':
        documentos = Documento.objects.filter(empresa=empresa)
        proposta_investimentos = PropostaInvestimento.objects.filter(empresa=empresa)
        percentual_vendido = 0
        for pi in proposta_investimentos:
            if pi.status == 'PA':
                percentual_vendido += pi.percentual
        
        total_captado = sum(proposta_investimentos.filter(status='PA').values_list('valor', flat=True))
        valuation_atual = (100 * float(total_captado)) / float(percentual_vendido) if percentual_vendido != 0 else 0

        proposta_investimentos_enviada = proposta_investimentos.filter(status='PE')
        return render(request, 'empresa.html', {'empresa': empresa, 'documentos': documentos, 'proposta_investimentos_enviada': proposta_investimentos_enviada, 'total_captado': total_captado, 'valuation_atual': valuation_atual})

@login_required
def add_doc(request, nome_empresa):
    empresa = Empresa.objects.get(nome=nome_empresa)
    titulo = request.POST.get('titulo')
    arquivo = request.FILES.get('arquivo')
    extensao = arquivo.name.split('.')[-1]

    if extensao != 'pdf':
        messages.error(request, 'O arquivo deve ser um PDF!')
        return redirect(f'/empresarios/empresa/{empresa.nome}')
    
    if not arquivo:
        messages.error(request, 'O arquivo é obrigatório!')
        return redirect(f'/empresarios/empresa/{empresa.nome}')
    
    doc = Documento(empresa=empresa, titulo=titulo, arquivo=arquivo)
    doc.save()

    messages.success(request, 'Documento adicionado com sucesso!')
    return redirect(f'/empresarios/empresa/{empresa.nome}')

@login_required
def excluir_doc(request, doc_id):
    doc = Documento.objects.get(id=doc_id)

    if doc.empresa.user != request.user:
        messages.error(request, 'Você não tem permissão para excluir este documento!')
        return redirect(f'/empresarios/empresa/{doc.empresa.nome}')

    empresa = doc.empresa
    doc.delete()
    messages.success(request, 'Documento excluído com sucesso!')
    return redirect(f'/empresarios/empresa/{empresa.nome}')

@login_required
def add_metrica(request, empresa_id):
    empresa = Empresa.objects.get(id=empresa_id)
    titulo = request.POST.get('titulo')
    valor = request.POST.get('valor')

    if empresa.user != request.user:
        messages.error(request, 'Você não tem permissão para adicionar métricas a esta empresa!')
        return redirect(f'/empresarios/empresa/{empresa.nome}')
    
    metrica = Metrica(empresa=empresa, titulo=titulo, valor=valor)
    metrica.save()

    messages.success(request, 'Métrica adicionada com sucesso!')
    return redirect(f'/empresarios/empresa/{empresa.nome}')

@login_required
def gerenciar_proposta(request, id):
    acao = request.GET.get('acao')
    pi = PropostaInvestimento.objects.get(id=id)

    if acao == 'aceitar':
        messages.success(request, 'Proposta aceita')
        pi.status = 'PA'
    elif acao == 'recusar':
        messages.success(request, 'Proposta recusada')
        pi.status = 'PR'

    pi.save()
    return redirect(f'/empresarios/empresa/{pi.empresa.id}')