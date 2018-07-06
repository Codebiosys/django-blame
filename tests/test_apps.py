def test_app_is_installed():
    """ It should ensure that the Audit app is installed. """
    from django.conf import settings
    from blame.apps import BlameConfig as config

    assert config.name in settings.INSTALLED_APPS
