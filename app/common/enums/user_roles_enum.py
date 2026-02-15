from sqlalchemy.dialects.postgresql import ENUM

user_roles_enum = ENUM('admin', 'user', name='user_roles', create_type=True)