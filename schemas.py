from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    mobile_number: int
    email: EmailStr


class UpdateUser(BaseModel):
    first_name: str | None
    last_name: str | None
    mobile_number: int | None
    email: EmailStr | None
