
## Sobre

A **Rádio IFRN** é uma plataforma web desenvolvida para promover informação, entretenimento e comunicação com a comunidade acadêmica do **IFRN – Campus São Paulo do Potengi**. O sistema reúne conteúdos relacionados à programação da rádio, incluindo programas, episódios, pedidos musicais e sugestões dos usuários. A plataforma busca aproximar a comunidade da rádio, proporcionando um ambiente digital acessível para acompanhar a programação, interagir com os conteúdos e participar ativamente das atividades da instituição.

## Tecnologias Utilizadas
[![SkillIcons](https://skillicons.dev/icons?i=js,py,html,css,django,bootstrap)](https://skillicons.dev)<br/>

## Integrantes
- Anny Carolline
- Williany Vitória

## Rodando
Siga as instruções abaixo para configurar o ambiente do projeto após clonar o repositório.

### 1. Criando e Ativando o Ambiente Virtual
```bash
python -m venv venv  
venv\Scripts\Activate.ps1
```

### 2. Instalando as Dependências
```bash
pip install -r requirements.txt  
```

### 3. Aplicando as Migrações
```bash
python manage.py migrate  
```

### 4. Criando um Superusuário
```bash
python manage.py createsuperuser  
```

Siga as instruções e defina um nome de usuário, e-mail e senha.

### 5. Executando o Servidor

```bash
python manage.py runserver  
```

### 6. Acessando a Rádio

Abra o navegador e acesse:

```
http://127.0.0.1:8000/
```

Faça login com o superusuário criado anteriormente.

Agora a **Rádio** está pronta para ser utilizada!
