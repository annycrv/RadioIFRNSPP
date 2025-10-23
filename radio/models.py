from django.db import models

class Home(models.Model):
    titulo_home = models.CharField(max_length=100)
    subtitulo_home = models.CharField(max_length=200)
    bg_home = models.ImageField(upload_to="radio/banner_home/", blank=True)
    quemsomos_home = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Home"

class Programacao(models.Model):
    DIAS_SEMANA = [
        ('segunda', 'Segunda'),
        ('terca', 'Terça'),
        ('quarta', 'Quarta'),
        ('quinta', 'Quinta'),
        ('sexta', 'Sexta'),
    ]
    bg_programacao = models.ImageField(upload_to="radio/img_programacao/", blank=True)
    titulo_programacao = models.CharField(max_length=100)
    horario_programacao = models.TimeField()
    dia_semana = models.CharField(max_length=10, choices=DIAS_SEMANA, blank=True)

    class Meta:
        verbose_name_plural = "Programações"

    def __str__ (self):
        return self.titulo_programacao

class Programa(models.Model):
    banner_programa = models.ImageField(upload_to="radio/img_programa/", blank=True)
    nome_programa = models.CharField(max_length=100)
    descricao_programa = models.CharField(max_length=100)
    artista_programa = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Programas"

    def __str__ (self):
        return self.titulo

class Podcast(models.Model):
    banner_podcast = models.ImageField(upload_to="radio/img_podcast/", blank=True)
    nome_podcast = models.CharField(max_length=100)
    descricao_podcast = models.CharField(max_length=100)
    host_podcast = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Podcasts"

    def __str__ (self):
        return self.titulo

class Sobre(models.Model):
    titulo_sobre = models.CharField(max_length=100)
    subtitulo_sobre = models.CharField(max_length=150)
    conteudo_sobre = models.CharField(max_length=150)
    banner_sobre = models.ImageField(upload_to="banner_sobre/")

    class Meta:
        verbose_name_plural = "Sobre"

    def __str__ (self):
        return self.titulo