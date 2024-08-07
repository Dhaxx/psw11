from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar_empresa/', views.cadastrar_empresa, name='cadastrar_empresa'),
    path('listar_empresas/', views.listar_empresas, name='listar_empresas'),
    path('empresa/<str:nome_empresa>', views.empresa, name='empresa'),
    path('add_doc/<str:nome_empresa>', views.add_doc, name='add_doc'),
    path('excluir_doc/<int:doc_id>', views.excluir_doc, name='excluir_doc'),
    path('add_metrica/<int:empresa_id>', views.add_metrica, name='add_metrica'),
]