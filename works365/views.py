from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib import auth
from .models import UserProfile, ProfissionalProfile, Servico, Categoria

def home(request):
    return render(request, 'pages/home.html')

def register_profissional(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        categorias = request.POST.get('categorias')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        profissional = User.objects.filter(username=username).first()

        if profissional:
            messages.error(request, 'Nome de usuário já está em uso. Por favor, escolha outro!')
            return redirect('register_profissional')  # Redireciona de volta para o formulário de registro

        # Verifica se o email já está em uso
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            messages.error(request, 'Este email já está registrado. Por favor, use outro!')
            return redirect('register_profissional')  # Redireciona de volta para o formulário de registro
        
         # Verifica se as senhas coincidem
        if senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem. Por favor, digite novamente!')
            return redirect('register_profissional')
        
        profissional = User.objects.create_user(username=username, email=email, password=senha)
        profissional.save()
        
        profissional_profile = ProfissionalProfile(profissional=profissional, telefone=telefone, categorias=categorias)
        profissional_profile.save()
        
        messages.success(request, 'Cadastro de Profissional realizado com sucesso!')
        messages.success(request, 'Faça login para acessar sua conta.')
        return redirect('login')

    return render(request, 'pages/profissional.html')

def register_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # Verifica se o username já está em uso
        user = User.objects.filter(username=username).first()
        if user:
            messages.error(request, 'Nome de usuário já está em uso. Por favor, escolha outro!')
            return redirect('register_usuario')  # Redireciona de volta para o formulário de registro

        # Verifica se o email já está em uso
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            messages.error(request, 'Este email já está registrado. Por favor, use outro!')
            return redirect('register_usuario')  # Redireciona de volta para o formulário de registro
        
         # Verifica se as senhas coincidem
        if senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem. Por favor, digite novamente!')
            return redirect('register_usuario')
        
        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()

        user_profile = UserProfile(user=user, telefone=telefone)
        user_profile.save()

        messages.success(request, 'Cadastro de Usuário realizado com sucesso!')
        messages.success(request, 'Faça login para acessar sua conta.')
        return redirect('login')
        
    return render(request, 'pages/usuario.html')


def request_user_service(request):
    if request.method == 'POST':
        nome_servico = request.POST.get('nome_servico')
        endereco = request.POST.get('endereco')
        descricao = request.POST.get('descricao')
        categorias_input = request.POST.get('categorias')
        solicitante = request.POST.get('solicitante')

        categorias_nomes = [cat.strip() for cat in categorias_input.split(',') if cat.strip()]

        # Obter o perfil do usuário autenticado
        usuario_atual = UserProfile.objects.get(user=request.user)
        
        # Criar o serviço e associá-lo ao perfil do usuário autenticado
        servico = Servico.objects.create(
            nome_servico=nome_servico, 
            endereco=endereco, 
            solicitante=solicitante, 
            descricao=descricao,
            usuario=usuario_atual
        )
        
        for categoria_nome in categorias_nomes:
            # Verificar se a categoria já existe no banco de dados
            categoria, created = Categoria.objects.get_or_create(nome=categoria_nome)
            # Adicionar a categoria ao serviço
            servico.categorias.add(categoria)

        servico.save()

        return redirect('view_user_service')  
    
    categorias_disponiveis = Categoria.objects.values_list('nome', flat=True).distinct()
      
    return render(request, 'pages/solicitar_servico_usuario.html', {'categorias': categorias_disponiveis})


def view_profissional_service(request):
    servicos = Servico.objects.all()
    
    return render(request, 'pages/visualizar_servico_profissional.html', {'servicos': servicos })

def processar_oferta(request, servico_id):
    if request.method == 'POST':
        valor_oferta = request.POST.get('oferta')
        servico = get_object_or_404(Servico, id=servico_id)
        
        # Salvar a oferta no campo correspondente
        servico.oferta = valor_oferta
        servico.save()
        
        # Armazenar o valor na sessão
        request.session['valor_oferta'] = valor_oferta

        profissional_nome = request.user.username
        
        # Armazenar o nome do profissional na sessão
        request.session['profissional_nome'] = profissional_nome
        
        # Redireciona para onde deseja exibir a oferta
        return redirect('view_profissional_service')
    
    return render(request, 'visualizar_servico_profissional.html')


def view_user_service(request):
    categorias_disponiveis = list(Categoria.objects.values_list('nome', flat=True).distinct())

    # Obter o parâmetro de filtro de categoria da requisição GET
    categoria_filtro = request.GET.get('categoria_filtro')

    # Obter o perfil do usuário autenticado
    usuario_atual = UserProfile.objects.get(user=request.user)

    if categoria_filtro:
        # Filtrar os serviços pelo nome da categoria escolhida e pelo perfil do usuário autenticado
        servicos = Servico.objects.filter(categorias__nome=categoria_filtro, usuario=usuario_atual)
    else:
        # Se não houver filtro, retornar todos os serviços do perfil do usuário autenticado
        servicos = Servico.objects.filter(usuario=usuario_atual)

    return render(request, 'pages/visualizar_servico_usuario.html', {'servicos': servicos, 'categorias_disponiveis': categorias_disponiveis})

def quem_somos(request):
    return render(request, 'pages/quem_somos.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = authenticate(request, username=username, password=senha)

        if user:
            # Identifique o tipo de perfil
            if hasattr(user, 'userprofile'):
                login_django(request, user)
                # messages.success(request, 'Login realizado com sucesso!')        
                return redirect('request_user_service')  # Redirecione para o serviço de usuário
            elif hasattr(user, 'profissionalprofile'):
                login_django(request, user)
                # messages.success(request, 'Login realizado com sucesso!')           
                return redirect('view_profissional_service')  # Redirecione para o serviço profissional
            else:
                messages.error(request, 'Tipo de usuário não identificado.')
                return redirect('login')
        else:
            messages.error(request, 'Nome de usuário ou senha incorretos.')
            return redirect('login')
        
    else:
        return render(request, 'pages/login.html')
    

def logout(request):
    auth.logout(request)
    return redirect('login')
