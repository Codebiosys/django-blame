# Django Blame

A simple Django utlitity to allow tracking created/updated metadata of Django
model records. When mixed in to your models, this tool will update created at/by
information for new records as well as updated at/by inoformation when the
record is updated using django signals.

## Requirements

* Django 1.11+
* Python 3.6+


## Quick start

1. Add to your INSTALLED_APPS setting like this:

    ```python
    INSTALLED_APPS = [
        ...

        'blame',
    ]
    ```

1. Enable middleware to track the current request user:

    ```python
    MIDDLEWARE = [
        ...

        'blame.middleware.RequestMiddleware',
    ]
    ```
    
    
1. In your models:

    ```python
    from blame.models import BlameInfo

    class MyModel(BlameInfo):
        ...
    ```


1. Run `python manage.py migrate` to create the necessary models.


### Optional features

#### GraphQL

This app comes equiped with an optional mixin to resolve `created_by`/`updated_by`
fields to just `graphene.String` typed values. To enable this feature, add the
following mixin to your graphql types:

```python
from graphene_django import DjangoObjectType
from blame.type import BlameInfo

class MyModelType(BlameInfo, DjangoObjectType):
    ...
```

