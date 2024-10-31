import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ContactForm(BaseModel):
    documentNumber: str = Field(
        ..., description="CPF cannot be empty and must have exactly 11 characters"
    )
    documentType: str = Field(..., description="Document type cannot be empty")
    name: str = Field(
        ..., description="Name cannot be empty and must be within a limit of 100"
    )
    lastName: str = Field(..., description="Last name cannot be empty")
    email: str = Field(..., description="Email cannot be empty")
    phone: str = Field(..., description="Phone can be empty but the field must exist")
    celPhone: str = Field(..., description="Cell phone cannot be empty")
    isPrime: bool = Field(..., description="Mandatory field")
    isMobile: bool = Field(..., description="Mandatory field")
    description: str = Field(..., description="Description cannot be empty")
    contactReason: str = Field(..., description="Reason for contact cannot be empty")
    contactRelatedTo: str = Field(..., description="Related to cannot be empty")
    tenantId: str = Field(..., description="tenantId cannot be empty")
    created_at: Optional[str] = None

    # empty validation
    @field_validator(
        "documentNumber",
        "documentType",
        "name",
        "email",
        "celPhone",
        "isPrime",
        "isMobile",
        "description",
        "contactReason",
        "contactRelatedTo",
        "tenantId",
        mode="before",
    )
    def not_empty(cls, v, info):
        if isinstance(v, str) and not v.strip():
            raise ValueError(f"{info.field_name} cannot be empty")
        return v

    # verify brazilian id(CPF)
    @field_validator("documentNumber")
    def cpf_must_have_11_characters(cls, v, info):
        if len(v) != 11:
            raise ValueError(f"{info.field_name} must have exactly 11 characters")
        if not cls.is_valid_cpf(v):
            raise ValueError(f"{info.field_name} is not valid")
        return v

    # name and last name validation
    @field_validator("name", "lastName")
    def must_have_min_2_max_100_characters_and_only_latin(cls, v, info):
        v = v.strip()
        if len(v) > 100 or len(v) < 2:
            raise ValueError(
                f"{info.field_name} name and last name must have between 2 and 100 characters"
            )
        if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", v):
            raise ValueError(
                f"{info.field_name} name and last name must contain only latin characters"
            )
        if any(c in v for c in "\t\n\r\f\v"):
            raise ValueError(
                f"{info.field_name} name and last name must not contain whitespace characters"
            )
        return v

    # celphone validation
    @field_validator("celPhone")
    def must_have_11_digits(cls, v, info):
        if len(v) != 11:
            raise ValueError(f"{info.field_name} must have exactly 11 digits")
        return v

    # email validation
    @field_validator("email")
    def must_be_valid_email(cls, v, info):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError(f"{info.field_name} must be a valid email")
        return v

    # cpf validation
    @staticmethod
    def is_valid_cpf(cpf: str) -> bool:
        if len(cpf) != 11 or not cpf.isdigit():
            return False

        def calculate_digit(digits: str) -> int:
            weight = len(digits) + 1
            total = sum(
                int(digit) * weight
                for digit, weight in zip(digits, range(weight, 1, -1))
            )
            remainder = total % 11
            return 0 if remainder < 2 else 11 - remainder

        first_digit = calculate_digit(cpf[:9])
        second_digit = calculate_digit(cpf[:9] + str(first_digit))

        return cpf[-2:] == f"{first_digit}{second_digit}"
