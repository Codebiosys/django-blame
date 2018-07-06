from django.db import models

from blame.models import BlameInfo


class DummyModel(BlameInfo):
    """ Dummy model for testing app mixins and migrations """

    text = models.CharField(max_length=100)
