from django.contrib.auth.models import User


def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    email = details.get('email')
    username = details.get('username')

    if not email or not username:
        return None

    user = User.objects.create_user(
        username=username,
        email=email,
        first_name=details.get('first_name', ''),
        last_name=details.get('last_name', '')
    )
    return {
        'is_new': True,
        'user': user
    }

