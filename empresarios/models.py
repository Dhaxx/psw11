from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from datetime import datetime

class Empresa(models.Model):
    tempo_existencia_choices = (
        ('-6', 'Menos de 6 meses'),
        ('+6', 'Mais de 6 meses'),
        ('+1', 'Mais de 1 ano'),
        ('+5', 'Mais de 5 anos'),
        )
    estagio_choices = (
        ('I', 'Tenho apenas uma Ideia'),
        ('MVP', 'Possuo um MVP'),
        ('MVPP', 'Possuo um MVP com clientes pagantes'),
        ('E', 'Empresa pronta para escalar'),
        )
    area_choices = (
        ('ED', 'Ed-tech'),
        ('FT', 'Fintech'),
        ('AT', 'Agrotech'),
    )
    
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=30)
    site = models.URLField()
    tempo_existencia = models.CharField(max_length=2, choices=tempo_existencia_choices, default='-6')
    descricao = models.TextField()
    data_final_captacao = models.DateField()
    percentual_equity = models.IntegerField()
    estagio = models.CharField(max_length=4, choices=estagio_choices, default='I')
    area = models.CharField(max_length=2, choices=area_choices, default='ED')
    publico_alvo = models.CharField(max_length=3)
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    pitch = models.FileField(upload_to='pitchs')
    logo = models.FileField(upload_to='logos')

    def __str__(self):
        return f'{self.user.username} | {self.nome}'
    
    @property
    def status(self):
        if self.data_final_captacao < datetime.now().date():
            return mark_safe('<span class="badge rounded-pill text-bg-danger">Captação Finalizada</span>')
        return mark_safe('<span class="badge rounded-pill text-bg-success">Em Captação</span>')
    
    @property
    def valuation(self):
        return (100 * self.valor) / self.percentual_equity
    
class Documento(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.DO_NOTHING)
    titulo = models.CharField(max_length=30)
    arquivo = models.FileField(upload_to='documentos')

    def __str__(self):
        return f'{self.empresa} | {self.titulo}'
    
class Metrica(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.DO_NOTHING)
    titulo = models.CharField(max_length=30)
    valor = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.empresa} | {self.titulo}'
