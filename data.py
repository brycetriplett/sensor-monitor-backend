from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from contextlib import contextmanager


engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)


@contextmanager
def session():
    yield (session := Session())
    session.commit()


class Device(Base := declarative_base()):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    oid = Column(String)
    response = Column(String)

    sessions = relationship('Monitor', back_populates='device')

    def __repr__(self):
        return (
            "<Device("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"oid='{self.oid}', "
            f"response='{self.response}'"
            ")>"
        )


class Monitor(Base):
    __tablename__ = 'sessions'

    ip = Column(String, primary_key=True)
    name = Column(String)
    community = Column(String)
    refresh = Column(Integer)
    active = Column(Boolean)
    device_id = Column(Integer, ForeignKey('devices.id'))

    device = relationship('Device', back_populates='sessions')
    sleep = relationship('Sleep', back_populates='session')

    def __repr__(self):
        return (
            "<Monitor("
            f"ip='{self.ip}', "
            f"name='{self.name}', "
            f"community='{self.community}', "
            f"refresh={str(self.refresh)}, "
            f"active={str(self.active)}, "
            f"device_id='{self.device_id}', "
            f"device={self.device}"
            ")>"
        )


class Sleep(Base):
    __tablename__ = 'sleep'

    ip = Column(String, ForeignKey('sessions.ip'), primary_key=True)
    time = Column(DateTime)
    duration = Column(Integer)

    session = relationship('Monitor', back_populates='sleep')

    def __repr__(self):
        return (
            "<Sleep("
            f"ip='{self.ip}', "
            f"time='{self.time}', "
            f"duration={str(self.duration)}, "
            f"session={self.session}"
            ")>"
        )


Base.metadata.create_all(engine)
    







