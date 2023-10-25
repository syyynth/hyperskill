from marshmallow import Schema, fields, validate


class TeamSchema(Schema):
    short = fields.Str(required=True, validate=[validate.Length(equal=3), str.isupper])
    name = fields.Str(required=True)
