from .models import UserProfile, ProfissionalProfile

def your_context_processor(request):
    user_profile = None
    profissional_profile = None

    if request.user.is_authenticated:
        # Supondo que você tenha um modelo UserProfile e um modelo ProfissionalProfile
        try:
            user_profile = request.user.userprofile  # Obtenha o perfil do usuário
        except UserProfile.DoesNotExist:
            user_profile = None

        try:
            profissional_profile = request.user.profissionalprofile  # Obtenha o perfil do profissional
        except ProfissionalProfile.DoesNotExist:
            profissional_profile = None

    return {
        'user_profile': user_profile,
        'profissional_profile': profissional_profile,
    }
