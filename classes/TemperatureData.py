from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Column, DateTime, Float
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid as uuid_lib
import datetime as datetime_lib
from utils import env_variables
from dotenv import load_dotenv

Base = declarative_base()


class TemperatureData(Base):
    load_dotenv()
    __tablename__: str = env_variables.readEnvVariable("AZURE_TABLE_NAME")
    uuid = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid_lib.uuid4)
    datetime = Column(DateTime, nullable=False)
    consulted_at = Column(DateTime, nullable=False)
    temp = Column(Float, nullable=False)
    temp_min = Column(Float, nullable=False)
    temp_max = Column(Float, nullable=False)
    feels_like = Column(Float, nullable=False)

    def __init__(
        self,
        uuid_value: uuid_lib.UUID,
        datetime: datetime_lib.datetime,
        consulted_at: datetime_lib.datetime,
        temp: float,
        temp_min: float,
        temp_max: float,
        feels_like: float,
    ) -> None:
        super().__init__()
        self.uuid: uuid_lib.UUID = uuid_value
        self.datetime: datetime_lib.datetime = datetime
        self.consulted_at: datetime_lib.datetime = consulted_at
        self.temp: float = temp
        self.temp_min: float = temp_min
        self.temp_max: float = temp_max
        self.feels_like: float = feels_like
