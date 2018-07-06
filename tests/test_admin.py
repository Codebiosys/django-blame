import pytest


@pytest.fixture
def site():
    from django.contrib.admin.sites import AdminSite
    site_ = AdminSite()
    return site_


@pytest.fixture
def admin(site):
    from blame.admin import BlameAdmin
    from blame.models import Blame
    admin_ = BlameAdmin(Blame, site)
    return admin_


class MockRequest(object):
    pass


request = MockRequest()


class Test_BlameAdmin:

    def test_str(self, admin):
        assert str(admin) == 'blame.BlameAdmin'

    def test_list_display(self, admin):
        """ It should list record columns """
        fields = list(admin.get_list_display(request))
        assert fields == ['uuid', 'username', 'created_at']
