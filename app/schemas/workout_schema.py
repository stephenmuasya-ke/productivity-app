from marshmallow import Schema, fields, validate


class WorkoutLogSchema(Schema):
    exercise_name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    duration_minutes = fields.Integer(required=True, validate=validate.Range(min=1))
    calories_burned = fields.Integer(required=False, allow_none=True, validate=validate.Range(min=0))
    workout_date = fields.Date(required=False, allow_none=True)
    notes = fields.String(required=False, allow_none=True, validate=validate.Length(max=2000))


class WorkoutLogUpdateSchema(Schema):
    exercise_name = fields.String(required=False, validate=validate.Length(min=1, max=120))
    duration_minutes = fields.Integer(required=False, validate=validate.Range(min=1))
    calories_burned = fields.Integer(required=False, allow_none=True, validate=validate.Range(min=0))
    workout_date = fields.Date(required=False, allow_none=True)
    notes = fields.String(required=False, allow_none=True, validate=validate.Length(max=2000))
