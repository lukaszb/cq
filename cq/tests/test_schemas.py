from .app import User
from .app import UserRegisteredSchema
from .app import UserEmailChangedSchema
import cq.aggregates
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