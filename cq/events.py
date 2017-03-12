import uuid
from .genuuid import genuuid
from datetime import datetime
from pyrsistent import field
from pyrsistent import PRecord
from pyrsistent import InvariantException


def isoformat(format, dt):
    return dt.isoformat()


def get_datetime(val=None):
    if not val:
        return datetime.utcnow()
    return val


def get_id():
    return genuuid()


class EventBody(PRecord):
    """
    Base class for `Event.data` field definition.
    Note: I would suggest `Event` name instead.
    """
    pass


class Event(PRecord):
    """
    Base event class that specifies must have event fields.
    Note: I would suggest `EventEnvelope` name instead.
    """
    # pyrsistent style event class, like the simplicity of the syntax
    # UUID & date validation could be added easily.
    # Serialization is pretty much out of the box here as well.
    id = field(mandatory=True, type=str, initial=get_id)
    aggregate_id = field(mandatory=True, type=str)
    name = field(mandatory=True, type=str)
    ts = field(
        mandatory=True,
        type=datetime,
        # use `get_datetime` is ts is not provided on init
        initial=get_datetime,
        # use `get_datetime` if `ts=None` on init
        factory=get_datetime,
        serializer=isoformat
    )

    # type below should be PRecord or None.
    # `dict` is left for now, to allieviate fixing alll the failing tests
    data = field(type=(EventBody, dict, type(None)))
