from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine, ForeignKey, func, Enum
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from status import Status

Base = declarative_base()
engine = create_engine('postgresql://postgres:08072006@localhost:5434/postgres')


class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="Идентификатор водителя")
    name = Column(String(60), nullable=False)
    car = Column(String(30), nullable=False)

    def __repr__(self):
        return "{" + f'"id":"{self.id}", "name":"{self.name}", "car":"{self.car}"' + "}"


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="Идентификатор клиента")
    name = Column(String(60), nullable=False)
    is_vip = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return "{" + f'"id":"{self.id}", "name":"{self.name}", "is_vip":"{self.is_vip}"' + "}"


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="Идентификатор заказа")
    address_from = Column(String(100), nullable=False)
    address_to = Column(String(100), nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    driver_id = Column(Integer, ForeignKey('drivers.id'), nullable=False)
    date_created = Column(DateTime(timezone=True), nullable=False, default=func.now())
    status = Column(Enum(Status, validate_strings=True), nullable=False,
                    default=Status.not_accepted.value)  # not_accepted, in_progress, cancelled, done
    client = relationship("Client")
    driver = relationship("Driver")

    def __repr__(self):
        return "{" + f'"id":"{self.id}","address_from":"{self.address_from}","address_to":"{self.address_to}",' + \
               f'"client_id":"{self.client_id}","driver_id":"{self.driver_id}",' + \
               f'"date_created":"{self.date_created}","status":"{self.status.value}"' + "}"


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.commit()
    session.close()
