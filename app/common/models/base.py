from app.extensions import db
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

class AuditMixin:
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    deleted_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    created_by = db.Column(UUID, nullable=True)
    updated_by = db.Column(UUID, nullable=True)
    deleted_by = db.Column(UUID, nullable=True)
