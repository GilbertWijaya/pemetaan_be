from app.extensions import db
from app.common.enums.wa_status_enum import wa_status_enum
from app.common.enums.propose_status_enum import propose_status_enum
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy import Numeric, Text
import uuid
from app.common.models.base import AuditMixin


class ResponseClean(db.Model, AuditMixin):
    __tablename__ = "responses_clean"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    place_id = db.Column(db.String(255), nullable=False)
    place_name = db.Column(db.String(255), nullable=False)
    format_address = db.Column(JSONB, nullable=False)
    geometry = db.Column(JSONB, nullable=False)
    formatted_phone_number = db.Column(JSONB, nullable=True)
    rating = db.Column(Numeric(precision=12, scale=2), nullable=False)
    user_rating_total = db.Column(db.Integer, nullable=False)
    is_wa_active = db.Column(wa_status_enum, default='checking', nullable=False)
    business_status = db.Column(db.String(255), nullable=False)
    categorical = db.Column(db.String(255), nullable=False)
    industry_type = db.Column(db.String(255), nullable=False)
    other_data = db.Column(JSONB, nullable=False)
    is_propose = db.Column(propose_status_enum, default='checking', nullable=False)
    description = db.Column(Text, nullable=False)

    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.id"),
        nullable=False
    )

    response_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("responses.id"),
        nullable=False
    )

    # 🔗 Relasi ke User
    user = db.relationship(
        "User",
        back_populates="responses_clean"
    )

    # 🔗 Relasi ke Response (FIXED)
    response = db.relationship(
        "Response",
        back_populates="responses_clean"  # ✅ harus cocok
    )

    def to_dict(self):
        return {
            "id": self.id,
            "place_id": self.place_id,
            "place_name": self.place_name,
            "format_address": self.format_address,
            "geometry": self.geometry,
            "formatted_phone_number": self.formatted_phone_number,
            "rating": self.rating,
            "user_rating_total": self.user_rating_total,
            "is_wa_active": self.is_wa_active,
            "business_status": self.business_status,
            "categorical": self.categorical,
            "industry_type": self.industry_type,
            "other_data": self.other_data,
            "is_propose": self.is_propose,
            "description": self.description,
            "user_id": self.user_id,
            "response_id": self.response_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "deleted_by": self.deleted_by,
        }
