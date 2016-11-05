from ses import settings
from ses.events import Event
from ses.genuuid import genuuid
from ses.storages import Storage
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative.api import declarative_base
import json
import sqlalchemy


Base = declarative_base()


class EventModel(Base):
    __tablename__ = 'ses_event'

    id = sqlalchemy.Column(sqlalchemy.String(128), primary_key=True, default=genuuid)
    name = sqlalchemy.Column(sqlalchemy.String(255), index=True)
    entity_id = sqlalchemy.Column(sqlalchemy.String(255), index=True)
    data = sqlalchemy.Column(sqlalchemy.Text(), default='{}')
    ts = sqlalchemy.Column(sqlalchemy.DateTime(), index=True)


class SqlAlchemyStorage(Storage):

    def __init__(self, db_uri=None, echo=None):
        self.db_uri = db_uri
        self.echo = settings.ENGINE_ECHO

    def append(self, event):
        obj = to_model(event)
        session = self.get_session()
        session.add(obj)
        session.commit()
        return obj

    def get_events(self, entity_id):
        session = self.get_session()
        # TODO: should be ordered by version, not ts (otoh ts should also work)
        query = session.query(EventModel).order_by(EventModel.ts)
        return (from_model(e) for e in query)

    def book_unique(self, namespace, value, entity_id=None):
        raise NotImplementedError

    def get_unique(self, namespace, value):
        raise NotImplementedError

    def has_unique(self, namespace, value):
        raise NotImplementedError

    def get_session(self):
        Session = self.get_sessionmaker()
        return Session()

    def get_sessionmaker(self):
        if not hasattr(self, '_sessionmaker'):
            engine = self.get_engine()
            self._sessionmaker = sessionmaker(bind=engine)
        return self._sessionmaker

    def get_engine(self):
        db_uri = self.get_db_uri()
        if not hasattr(self, '_engine'):
            self._engine = sqlalchemy.create_engine(db_uri, echo=self.echo)
            Base.metadata.create_all(self._engine)
        return self._engine

    def get_db_uri(self):
        if self.db_uri:
            return self.db_uri
        if settings.DB_URI is None:
            raise RuntimeError("DB_URI environment variable must be set")
        else:
            return settings.DB_URI


def to_model(event):
    return EventModel(
        id=event.id,
        name=event.name,
        entity_id=event.entity_id,
        data=json.dumps(event.data),
    )


def from_model(instance):
    return Event(
        id=instance.id,
        name=instance.name,
        entity_id=instance.entity_id,
        data=json.loads(instance.data),
        ts=instance.ts,
    )
