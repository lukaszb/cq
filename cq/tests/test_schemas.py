from .app import User
from .app import UserRegisteredSchema
from .app import UserEmailChangedSchema
import cq.aggregates
import cq.exceptions
import cq.schemas
import pytest


class AggregateWithoutMutators(cq.aggregates.Aggregate):
        pass


def test_aggregate_get_schema__none_mutators_registered():
    assert AggregateWithoutMutators.get_schema('dummy_mutator') is None
    

def test_user_aggregate_registered_schemas():
    assert User.schemas == {
        'Registered': UserRegisteredSchema,
        'EmailChanged': UserEmailChangedSchema,
    }


def test_user_aggreagate_get_schemas():
    assert User.get_schema('dummy_schema') is None


def test_validate_user_registered__valid_data():
    assert User.validate('Registered', {
        'email': 'john@doe.com',
        'password': 'secret',
        'role': 'janitor'
    })


def test_validate_user_registered__invalid_data():
    with pytest.raises(cq.exceptions.SchemaValidationError) as exc:
        User.validate('Registered', {
            'email': 'dummy',
        })

    msg = "Error validatng User.Registered event: {'email': ['Not a valid email address.']}"
    assert msg in str(exc.value)


def test_validate_user_registered__excess_keys():
    """
    Strictly report errors if unspecified keys are provided in event payload.
    """
    with pytest.raises(cq.exceptions.SchemaValidationError) as exc:
        assert User.validate('Registered', {
            'email': 'john@doe.com',
            'password': 'secret',
            'role': 'janitor',
            'unrelated': 'info'
        })

    msg = "Error validatng User.Registered event: {'unrelated': ['Unknown field']}"
    assert msg in str(exc.value)
