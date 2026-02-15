from app.extensions import db
from app.common.enums.response_status_enum import response_status_enum
from sqlalchemy.dialects.postgresql import JSONB, UUID
import uuid
from app.common.models.base import AuditMixin

class Response(db.Model, AuditMixin):
    __tablename__ = "responses"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt = db.Column(db.String(255), nullable=False)
    response = db.Column(JSONB, nullable=False)
    response_status = db.Column(response_status_enum, nullable=False, default="all")

    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.id"),
        nullable=False
    )

    parent_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("responses.id"),
        nullable=True
    )

    # 🔗 Relasi ke User
    user = db.relationship(
        "User",
        back_populates="responses"
    )

    # 🔗 Relasi ke ResponseClean (FIXED)
    responses_clean = db.relationship(
        "ResponseClean",
        back_populates="response",  # ✅ harus cocok
        lazy="select"
    )

    # 🔁 Self relation
    parent = db.relationship(
        "Response",
        remote_side=[id],
        backref="children"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "prompt": self.prompt,
            "response": self.response,
            "user_id": self.user_id,
            "parent_id": self.parent_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "deleted_by": self.deleted_by
        }