from django.db import models
class Contato(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    mensagem = models.TextField()

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    senha = models.CharField(max_length=255)

    def __str__(self):
        return self.nome