from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
# import datetime

Base = declarative_base()


class BusinessSymptom(Base):
    """Creates the data model of the Business-Symptoms data

    Args:
        Base (_type_): Returns the model schema to be used throughout the application.
    """
    __tablename__      = 'business_symptom'

    id                 = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    business_id        = Column(Integer, nullable=False)
    business_name      = Column(String, nullable=False)
    symptom_code       = Column(String, nullable=False)
    symptom_name       = Column(String, nullable=False)
    symptom_diagnostic = Column(String, nullable=False)
