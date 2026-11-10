
from datetime import date

from marshmallow import (
    Schema,
    fields,
    validate,
    validates,
    ValidationError
)


class ApplicationSchema(Schema):

    company = fields.String(required=True)

    role = fields.String(required=True)

    status = fields.String(
        load_default="APPLIED",
        validate=validate.OneOf([
            "APPLIED",
            "PHONE_SCREEN",
            "INTERVIEW",
            "OFFER",
            "REJECTED"
        ])
    )

    applied_date = fields.Date(
        load_default=date.today
    )

    notes = fields.String(
        allow_none=True,
        load_default=None
    )

    user_id = fields.Integer(required=False)

    @validates("company")
    def validate_company(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Company name cannot be empty.")

    @validates("applied_date")
    def validate_applied_date(self, value, **kwargs):
        if value > date.today():
            raise ValidationError(
                "Applied date cannot be in the future."
            )
