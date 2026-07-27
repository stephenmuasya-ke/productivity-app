from marshmallow import Schema, fields, validate


class SignupSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3, max=80))
    password = fields.String(required=True, validate=validate.Length(min=6, max=128))


class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
