from sqlalchemy.dialects.postgresql import ENUM

response_status_enum = ENUM('all', 'detail', name='response_status', create_type=True)