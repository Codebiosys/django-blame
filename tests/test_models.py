import pytest


@pytest.mark.django_db
def test__str__():
    """ Test the blame's string representation. """
    from blame.factories import BlameFactory
    blame = BlameFactory()
    assert str(blame) == '%s' % blame.username


@pytest.mark.manual_blame_middleware
class Test_get_current_username:

    def test_success(self, monkeypatch):
        """ It should inspect the current request to extract the current user """
        from unittest.mock import Mock
        import blame.models
        USERNAME = 'dave'
        request = Mock(user=Mock(username=USERNAME))
        monkeypatch.setattr(blame.models, 'get_current_request', lambda: request)
        assert blame.models._get_current_username() == USERNAME

    def test_fail(self, monkeypatch):
        """ It should throw a description exception when user is unavailable """
        import blame.models
        monkeypatch.setattr(blame.models, 'get_current_request', lambda: None)
        with pytest.raises(Exception) as excinfo:
            blame.models._get_current_username()
        assert 'User not present' in str(excinfo.value)


@pytest.mark.django_db
def test_auto_blame_for_blanks(monkeypatch):
    """ It should populate empty blame fields """
    from unittest.mock import Mock
    import blame.models

    USERNAME = 'dave'
    monkeypatch.setattr(blame.models, '_get_current_username', lambda: USERNAME)

    dummy = Mock(
        _state=Mock(adding=True),
        created_by=None,
        updated_by=None
    )

    from blame.models import auto_blame
    auto_blame(blame.models.BlameInfo, dummy)

    assert dummy.created_by.username == USERNAME
    assert dummy.updated_by.username == USERNAME


@pytest.mark.django_db
def test_allow_override_on_add(monkeypatch):
    """ It should allow factoryboy to autopopulate when creating records """
    from unittest.mock import Mock
    import blame.models
    LOGGED_USERNAME = 'dave'
    FACTORY_USERNAME = 'factoryboy'
    monkeypatch.setattr(blame.models, '_get_current_username', lambda: LOGGED_USERNAME)

    dummy = Mock(
        _state=Mock(adding=True),
        created_by=blame.models.Blame(username=FACTORY_USERNAME),
        updated_by=blame.models.Blame(username=FACTORY_USERNAME),
    )

    from blame.models import auto_blame
    auto_blame(blame.models.BlameInfo, dummy)

    assert dummy.created_by.username == FACTORY_USERNAME
    assert dummy.updated_by.username == FACTORY_USERNAME


@pytest.mark.django_db
def test_update_updated_by(monkeypatch):
    """ It should update the updated_by field when updates are saved """
    from unittest.mock import Mock
    import blame.models
    LOGGED_USERNAME = 'dave'
    FACTORY_USERNAME = 'factoryboy'
    monkeypatch.setattr(blame.models, '_get_current_username', lambda: LOGGED_USERNAME)

    dummy = Mock(
        _state=Mock(adding=False),
        created_by=blame.models.Blame(username=FACTORY_USERNAME),
        updated_by=blame.models.Blame(username=FACTORY_USERNAME),
    )

    from blame.models import auto_blame
    auto_blame(blame.models.BlameInfo, dummy)

    assert dummy.created_by.username == FACTORY_USERNAME
    assert dummy.updated_by.username == LOGGED_USERNAME


@pytest.mark.django_db
def test_auto_blame_for_exceptions(monkeypatch):
    """ It should populate empty blame fields when Django can't find them """
    import blame.models
    from .models import DummyModel

    USERNAME = 'dave'
    monkeypatch.setattr(
        blame.models, '_get_current_username', lambda: USERNAME)

    dummy = DummyModel()
    from blame.models import auto_blame
    auto_blame(blame.models.BlameInfo, dummy)

    assert dummy.created_by.username == USERNAME
    assert dummy.updated_by.username == USERNAME
