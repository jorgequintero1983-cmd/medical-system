from pydantic import BaseModel, Field, field_validator


class PatientCreate(BaseModel):

    document: str = Field(
        ...,
        min_length=3
    )

    full_name: str = Field(
        ...,
        min_length=3
    )

    phone: str = Field(
        ...,
        min_length=7
    )

    @field_validator("document")
    @classmethod
    def validate_document(cls, value):

        value = value.strip()

        if not value:
            raise ValueError(
                "El documento es obligatorio"
            )

        if not value.isdigit():
            raise ValueError(
                "El documento solo debe contener números"
            )

        return value

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value):

        value = value.strip()

        if not value:
            raise ValueError(
                "El nombre es obligatorio"
            )

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):

        value = value.strip()

        if not value:
            raise ValueError(
                "El celular es obligatorio"
            )

        if not value.isdigit():
            raise ValueError(
                "El celular solo debe contener números"
            )

        return value