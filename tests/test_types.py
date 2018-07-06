class Test_BlameInfo:

    def test_resolve_created_by(self):
        from blame.types import BlameInfo
        from blame.models import Blame
        USERNAME = 'jdoe@somecompay.com'
        type_ = BlameInfo()
        type_.created_by = Blame(username=USERNAME)
        assert type_.resolve_created_by(None) == USERNAME

    def test_resolve_updated_by(self):
        from blame.types import BlameInfo
        from blame.models import Blame
        USERNAME = 'jdoe@somecompay.com'
        type_ = BlameInfo()
        type_.updated_by = Blame(username=USERNAME)
        assert type_.resolve_updated_by(None) == USERNAME
