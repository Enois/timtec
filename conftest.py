import pytest
from django.conf import settings


def pytest_addoption(parser):
    parser.addoption("--collectstatic", action="store_true",
                     help="run slow collectstatic test")


def create_user(username):
    """A Django common user"""
    email = username + '@example.com'
    password = 'password'

    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username, email, password)
        user.accepted_terms = True
        if username == 'admintest':
            user.is_staff = True
            user.is_superuser = True
        user.save()
    return user


@pytest.fixture()
def admin_user(db):
    """A Django test admin user"""
    user = create_user('admintest')
    return user


@pytest.fixture()
def admin_client(db):
    """A Django admin user"""
    from django.test.client import Client

    user = create_user('admintest')

    client = Client()
    client.login(username=user.username, password='password')
    return client


@pytest.fixture()
def user(db):
    return create_user('common')


def pytest_configure():
    # workaround to avoid django pipeline issue
    # refers to https://github.com/cyberdelia/django-pipeline/issues/277
    settings.STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'
