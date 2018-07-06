""" Optional factories for testing data

Declarations in this module are intended only for development purposes
"""

try:

    import factory

except ImportError:  # pragma: nocover

    pass

else:

    class BlameFactory(factory.django.DjangoModelFactory):

        class Meta:
            model = 'blame.Blame'

        username = factory.Faker('ascii_email')
        created_at = factory.Faker('date_time_this_year')

    class BlameInfoFactory(factory.django.DjangoModelFactory):
        """ Mixin class for generating fake data for blame columns """

        class Meta:
            abstract = True

        created_by = factory.SubFactory(BlameFactory)
        created_at = factory.Faker('date_time_this_year', before_now=True)
        updated_by = factory.SubFactory(BlameFactory)
        updated_at = factory.Faker('date_time_this_year', after_now=True)
