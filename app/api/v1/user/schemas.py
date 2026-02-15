from marshmallow import Schema, fields, validate

class UserUpdateSchema(Schema):
    fullname = fields.String(required=True)
    username = fields.String(required=True)
