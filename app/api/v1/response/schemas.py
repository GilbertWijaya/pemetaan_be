from marshmallow import Schema, fields

class ResponseCreateSchema(Schema):
    prompt = fields.String(required=True)
    response_data = fields.Dict(required=True)
    parent_id = fields.String(required=False)
