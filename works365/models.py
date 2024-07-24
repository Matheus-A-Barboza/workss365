from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class ProfissionalProfile(models.Model):
    profissional = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    categorias = models.CharField(max_length=100)
    
    def __str__(self):
        return self.profissional.user.username + ' - Profissional Profile'
    
class Servico(models.Model):
    nome_servico = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    descricao = models.TextField()
    categorias = models.ManyToManyField(Categoria)
    solicitante = models.CharField(max_length=255)
    oferta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    usuario = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='servicos')

    def __str__(self):
        return self.nome_servico
    
