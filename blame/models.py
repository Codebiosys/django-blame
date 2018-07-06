import uuid

from django.db import models
from django.core import exceptions
from django.dispatch import receiver


from .middleware import get_current_request


class Blame(models.Model):
    """ User tracking table.

    User accounts are stored in a separate service and this table will only
    log the fact that a specific user has activity in the system.

    Note that this class does not inherit primary key information from
    any mixin in order to stay application-agnostic
    """

    id = models.BigAutoField(primary_key=True)

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    username = models.CharField(
        editable=False,
        max_length=100,
        help_text=(
            'The user\'s primary login handle from the authentication '
            'service.')
        )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        help_text='The first time the user had any activity in the system'
        )

    def __str__(self):
        return f'{self.username}'


class BlameInfo(models.Model):
    """ Mixin class to add blame information to models """

    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        help_text='Date & time the record was first inserted into the database'
        )

    created_by = models.ForeignKey(
        'blame.Blame',
        related_name='+',  # No back-ref!
        on_delete=models.PROTECT,
        editable=False,
        help_text='Who to blame for creating the record',
        )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
        help_text='Date & time the record was last modified'
        )

    updated_by = models.ForeignKey(
        'blame.Blame',
        related_name='+',  # No back-ref!
        on_delete=models.PROTECT,
        editable=False,
        help_text='Who to blame for changes',
        )

    # This field will be required in the database, but can be left blank
    # https://docs.djangoproject.com/en/2.0/ref/models/fields/#null
    reason_for_change = models.CharField(
        max_length=256,
        blank=True,
        help_text='What was changed in the record?'
        )


def _get_current_username():
    """ Accesses thread-local storage to acquire the current username

    The username must be stored in a user object in the request via a
    Django-REST-like framework
    """
    try:
        return get_current_request().user.username
    except Exception:
        raise Exception(
            'User not present in request when trying to access for blame')


def _is_relation_empty(instance, name):
    """ Checks if an instance has a saved relation without throwing an exception """
    try:
        return getattr(instance, name) is None
    except exceptions.ObjectDoesNotExist:
        return True


def _get_or_create_blame_user():
    """ Creates a blame user from the currently logged in user """
    username = _get_current_username()
    blame, _ = Blame.objects.get_or_create(username=username)
    return blame


@receiver(models.signals.pre_save)
def auto_blame(sender, instance, **kwargs):
    """ Updates blame user columns with currently logged in user

    This method expects a "user" property to be set in the request via
    a Django-REST-like framework that contains a "username" value.
    """

    # Ensure only BlameInfo models are handled
    # Django model signals do not work with abstract classes
    if not issubclass(sender, BlameInfo):
        return

    if instance._state.adding:
        if _is_relation_empty(instance, 'created_by'):
            instance.created_by = _get_or_create_blame_user()
        if _is_relation_empty(instance, 'updated_by'):
            instance.updated_by = instance.created_by
    else:
        instance.updated_by = _get_or_create_blame_user()
