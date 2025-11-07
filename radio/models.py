from django.db import models

class Home(models.Model):
    titulo_home = models.CharField(max_length=100)
    subtitulo_home = models.CharField(max_length=200)
    bg_home = models.ImageField(upload_to="radio/banner_home/", blank=True)
    quemsomos_home = models.CharField(max_length=1000)
    nome = models.CharField("Seu nome",max_length=50, blank=True)
    comentario = models.TextField("Quais programas você gostaria de encontrar na nossa rádio?", max_length=1000, blank=True)

    class Meta:
        verbose_name_plural = "Home"

class Podcast(models.Model):
    banner_podcast = models.ImageField(upload_to="radio/img_podcast/", blank=True)
    nome_podcast = models.CharField(max_length=100)
    descricao_podcast = models.CharField(max_length=1000)
    host_podcast = models.CharField(max_length=1000)

    class Meta:
        verbose_name_plural = "Podcasts"

    def __str__ (self):
        return self.nome_podcast

class Quadro(models.Model):
    banner_quadro = models.ImageField("Banner do quadro",upload_to="radio/img_programa/", blank=True)
    nome_quadro = models.CharField("Nome do quadro",max_length=100)
    descricao_quadro = models.CharField("Descrição do quadro",max_length=1000)
    artista_quadro = models.CharField("Artista do quadro",max_length=1000)

    class Meta:
        verbose_name_plural = "Quadros"

    def __str__ (self):
        return self.nome_quadro

class Programacao(models.Model):
    DIAS_SEMANA = [
        ('segunda', 'Segunda'),
        ('terca', 'Terça'),
        ('quarta', 'Quarta'),
        ('quinta', 'Quinta'),
        ('sexta', 'Sexta'),
    ]
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, null=True, blank=True)
    quadro = models.ForeignKey(Quadro,on_delete=models.CASCADE, null=True, blank=True)
    titulo_programacao = models.CharField(max_length=100)
    horario_programacao = models.TimeField()
    dia_semana = models.CharField(max_length=10, choices=DIAS_SEMANA, blank=True)

    class Meta:
        verbose_name_plural = "Programações"

    def __str__ (self):
        return self.titulo_programacao

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
    TURNO = [
        ('manha', 'Manhã'),
        ('tarde', 'Tarde'),
    ]

    nome = models.CharField("Seu nome",max_length=1000)
    musica = models.CharField("O que você gostaria de ouvir hoje?",max_length=1000)
    artista = models.CharField("Qual o nome do(a) artista ou banda dessa música?",max_length=1000)
    horario_desejado = models.TimeField("Qual o horário desejado?")
    mensagem = models.TextField("Observações (opcional)",blank=True, null=True, max_length=1000)
    turno = models.CharField("Turno", max_length=10, choices=TURNO, blank=True, null=True)
    # horario_pedidos = models.TimeField()
    class Meta:
        verbose_name_plural = "Pedidos"

    def __str__ (self):
        return self.musica
    
    