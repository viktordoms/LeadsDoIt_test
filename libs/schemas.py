
from flask import abort
from marshmallow import fields as f, Schema, ValidationError


class BasicSchema(Schema):
    """Very basic schema with custom methods"""

    def handle_error(self, exc: ValidationError, data, **kwargs):
        """Raise custom exception when (de)serialization fails."""
        from libs.errors import throw_validation_error

        abort(
            throw_validation_error(
                message="Some data is invalid",
                errors=[
                    f"{key}: {', '.join(msg) if type(msg) == list else msg}" for key, msg in exc.messages.items()
                ]
            )
        )

class BasicSuccessSchema(BasicSchema):
    """Basic success schema"""
    success = f.Boolean(required=True)