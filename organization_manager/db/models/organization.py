from sqlalchemy import Column, Integer, String

from organization_manager.db.models.base import Base


class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    organization_name = Column(String, index=True, nullable=False)
