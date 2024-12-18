from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from organization_manager.db.models.base import MasterBase


class Organization(MasterBase):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)

    # Relationship to link an organization to their user mappings
    users = relationship("OrganizationUserMapping", back_populates="organization")


class OrganizationDatabase(MasterBase):
    __tablename__ = 'organization_databases'

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    database_name = Column(String, nullable=True)
    database_url = Column(String, nullable=False)
