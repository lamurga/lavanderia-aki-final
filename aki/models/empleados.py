
from sqlalchemy import Column, Integer, String

from aki.models.base import Base


class EmployeesModel(Base):

    __tablename__ = 'empleados'

    id = Column('empleados_id', Integer, primary_key=True)
    first_name = Column('nom_empleado', String)
    last_name = Column('ape_empleado', String)
    street = Column('dir_empleado', String)
    document = Column('dni_empleado', String)
    phone = Column('tel_empleado', String)
    district = Column('dis_empleado', String)

    def __repr__(self):
        return f"<Empleado {self.first_name}>"

