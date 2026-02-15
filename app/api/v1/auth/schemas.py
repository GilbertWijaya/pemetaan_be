from marshmallow import Schema, fields, validate

class AuthRegisterSchema(Schema):
    fullname = fields.String(required=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    role = fields.String(required=True)

class AuthLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
