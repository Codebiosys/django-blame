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

### Running tests

It is highly encouraged you run the tests using the included docker stack.


1. Clone the application:

    ```
    > git clone https://github.com/CodeBiosys/django-blame
    > cd django-blame
    ```

1. Provision a new Docker machine called `django-blame`:

    ```
    > docker-machine create -d virtualbox django-blame
    > eval $(docker-machine env django-blame)
    > docker-machine ls
		NAME                ACTIVE   DRIVER       STATE     URL                         SWARM   DOCKER        ERRORS
		django-blame        *        virtualbox   Running   tcp://192.168.99.100:2376           v18.06.1-ce
    ```

    **Note the asterisk in the "ACTIVE" column.**


1. Build the application stack and start the services:

    ```
    > docker-compose build
		> docker-compose up -d
    ```

1. Run the tests

		```
		docker-compose run --rm app py.test
		```
