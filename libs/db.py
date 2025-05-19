from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql.functions import func

from libs.conf import DB

connection_string = f"mysql+pymysql://{DB['user']}:{DB['password']}@{DB['host']}/{DB['database']}"
engine = create_engine(
    connection_string,
    pool_size=30,
    max_overflow=60,
)
session = sessionmaker(bind=engine)
db_session = scoped_session(session)

class Base:

    @classmethod
    def default_joined_query(cls):
        return cls.query.options(*cls.loading_opts())

    @classmethod
    def loading_opts(cls):
        return ()

    @classmethod
    def get(cls, **kwargs):
        assert len(kwargs) == 1
        attr_name, attr_value = list(kwargs.items())[0]
        return next((row for row in cls.get_all() if getattr(row, attr_name) == attr_value), None)

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.id).all()


Base = declarative_base(cls=Base)
Base.query = db_session.query_property()


class TblWeatherHistory(Base):
    __tablename__ = "tbl_weather_history"

    id = Column(Integer, primary_key=True)
    city = Column(String(128), nullable=False)
    temperature = Column(Float(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.NOW())
