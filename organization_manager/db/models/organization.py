from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from organization_manager.db.models.base import MasterBase


class Organization(MasterBase):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    organization_name = Column(String, index=True, nullable=False)

    # Relationship to link an organization to their user mappings
    users = relationship("OrganizationUserMapping", back_populates="organization")
