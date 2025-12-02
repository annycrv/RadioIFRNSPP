from django.db import models
from usuarios.models import Usuario

class Home(models.Model):
    titulo_home = models.CharField(max_length=100)
    subtitulo_home = models.CharField(max_length=200)
    bg_home = models.ImageField(upload_to="radio/banner_home/", blank=True)
    quemsomos_home = models.CharField(max_length=1000)
    nome = models.CharField("Seu nome",max_length=50)
    comentario = models.TextField("Quais os programas você gostaria de encontrar na nossa rádio?", max_length=1000)

    class Meta:
        verbose_name_plural = "Home"

class Programa(models.Model):
    banner_programa = models.ImageField("Banner do programa",upload_to="radio/img_programa/", blank=True)
    nome_programa = models.CharField("Nome do programa",max_length=100)
    descricao_programa = models.CharField("Descrição do programa",max_length=1000)
    apresentador_programa = models.CharField("Apresentador do programa",max_length=1000)
    curtidas = models.ManyToManyField(Usuario, related_name="curtidas", blank=True)


    class Meta:
        verbose_name_plural = "programas"

    def __str__ (self):
        return self.nome_programa
    

class Episodio(models.Model):
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, related_name="episodios")
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    # audio = models.FileField(upload_to="radio/episodios/")
    data_publicacao = models.DateField(auto_now_add=True)
    apresentador = models.CharField(max_length=1000,null=True)


    class Meta:
        verbose_name_plural = "Episodios"

    def __str__(self):
        return f"{self.programa.nome_programa} - {self.titulo}"

class Programacao(models.Model):
    DIAS_SEMANA = [
        ('segunda', 'Seg'),
        ('terca', 'Ter'),
        ('quarta', 'Qua'),
        ('quinta', 'Qui'),
        ('sexta', 'Sex'),
    ]

    HORARIO = [
        ('08:30','08:30 - 08:50'),
        ('10:20','10:20 - 10:30'),
        ('14:30','14:30 - 14:50'),
        ('16:20','16:20 - 16:30'),
    ]

    programa = models.ForeignKey(Programa, on_delete=models.CASCADE)
    dia = models.CharField(max_length=10, choices=DIAS_SEMANA)
    horario = models.CharField(choices=HORARIO)
    
    class Meta:
        verbose_name_plural = "programação"

    def __str__ (self):
        return self.programa.nome_programa



class Sobre(models.Model):
    titulo_sobre = models.CharField(max_length=100)
    subtitulo_sobre = models.CharField(max_length=1000)
    conteudo_sobre = models.CharField(max_length=1000)
    banner_sobre = models.ImageField(upload_to="banner_sobre/")

    class Meta:
        verbose_name_plural = "Sobre"

    def __str__ (self):
        return self.titulo_sobre
    

class Pedido(models.Model):

    HORARIO = [
        ('08:30','08:30 - 08:50'),
        ('10:20','10:20 - 10:30'),
        ('14:30','14:30 - 14:50'),
        ('16:20','16:20 - 16:30'),
    ]

    nome = models.CharField("Seu nome",max_length=1000)
    musica = models.CharField("O que você gostaria de ouvir hoje?",max_length=1000)
    artista = models.CharField("Qual o nome do(a) artista ou banda dessa música?",max_length=1000)
    horario_desejado = models.CharField("Qual o horário desejado?", max_length=5, choices=HORARIO)
    mensagem = models.TextField("Observações (opcional)",blank=True, null=True, max_length=1000)

    class Meta:
        verbose_name_plural = "Pedidos"

    def __str__ (self):
        return self.musica

    