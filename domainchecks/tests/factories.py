import random
import string

from django.contrib.auth import get_user_model
from django.utils.timezone import now

from .. import models


def create_user(**kwargs):
    """Create sample user."""
    username = ''.join(random.choice(string.ascii_letters) for x in range(30))
    values = {
        'username': username,
        'email': '{}@example.com'.format(username),
        'password': 'test',
    }
    values.update(kwargs)
    User = get_user_model()
    user = User.objects.create(**values)
    user.set_password(values['password'])
    user.save(update_fields=('password', ))
    return user


def create_domain_check(**kwargs):
    """Create a sample domain check."""
    values = {
        'protocol': 'http',
        'domain': 'example.com',
        'path': '/',
        'method': 'get',
        'is_active': True,
    }
    values.update(kwargs)
    return models.DomainCheck.objects.create(**values)


def create_check_result(**kwargs):
    """Create a sample check result."""
    values = {
        'checked_on': now(),
        'status_code': 200,
        'response_time': 0.5,
        'response_body': 'Ok'
    }
    values.update(kwargs)
    if 'domain_check' not in values:
        values['domain_check'] = create_domain_check()
    return models.CheckResult.objects.create(**values)
