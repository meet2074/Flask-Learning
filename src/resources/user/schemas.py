from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    mobile_number: int
    email: EmailStr

