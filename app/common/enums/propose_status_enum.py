from sqlalchemy.dialects.postgresql import ENUM

propose_status_enum = ENUM('propose', 'reject', 'checking', name='propose_status', create_type=True)