from app.extensions import db
from app.common.enums.user_roles_enum import user_roles_enum
from sqlalchemy.dialects.postgresql import UUID
from app.common.models.base import AuditMixin
import uuid

class User(db.Model, AuditMixin):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fullname = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(user_roles_enum, nullable=False, default='admin')
    responses = db.relationship("Response", back_populates="user", lazy="select")
    responses_clean = db.relationship("ResponseClean", back_populates="user", lazy="select")

    def to_dict(self):
        return {
            "id": str(self.id),  # konversi UUID ke string
            "fullname": self.fullname,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "deleted_by": self.deleted_by,
        }

