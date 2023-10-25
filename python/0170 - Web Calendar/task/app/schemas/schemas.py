from marshmallow import Schema, fields

REQUIRED_DATE_FORMAT = 'YYYY-MM-DD!'
REQUIRED_DATE_MESSAGE = f'The event date with the correct format is required! The correct format is {REQUIRED_DATE_FORMAT}'
REQUIRED_EVENT_MESSAGE = 'The event name is required!'


class EventSchema(Schema):
    """Event Schema class"""

    event = fields.Str(
        required=True,
        error_messages={
            'required': REQUIRED_EVENT_MESSAGE
        }
    )

    date = fields.Date(
        required=True,
        error_messages={
            'required': REQUIRED_DATE_MESSAGE,
            'invalid': REQUIRED_DATE_MESSAGE
        }
    )
