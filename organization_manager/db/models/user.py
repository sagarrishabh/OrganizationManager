from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from organization_manager.db.models.base import MasterBase


class User(MasterBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationship to link a user to their organization mappings
    organizations = relationship("OrganizationUserMapping", back_populates="user")


class OrganizationUserMapping(MasterBase):
    __tablename__ = 'organization_user_mapping'

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relationship to link back to the User
    user = relationship("User", back_populates="organizations")

    # Add an organization relationship if there's an Organization model
    organization = relationship("Organization", back_populates="users")

    # Define a composite unique constraint on organization_id and user_id
    __table_args__ = (
        UniqueConstraint('organization_id', 'user_id', name='uniqe_organization_user'),
    )