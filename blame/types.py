""" Optional convenience graphene utilities
"""

try:

    import graphene

except ImportError:  # pragma: nocover

    pass

else:

    class BlameInfo(object):
        """ Mixin to alias blame fields to their string value """

        created_by = graphene.String()
        updated_by = graphene.String()

        def resolve_created_by(self, info, **kwargs):
            return self.created_by.username

        def resolve_updated_by(self, info, **kwargs):
            return self.updated_by.username
