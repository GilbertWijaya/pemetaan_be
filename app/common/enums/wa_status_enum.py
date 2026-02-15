from sqlalchemy.dialects.postgresql import ENUM

wa_status_enum = ENUM('active', 'non-active', 'checking', name='wa_status', create_type=True)