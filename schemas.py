from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    id: int
    name: str
    age: int
    email: str

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1)
    age: int = Field(..., gt=0, lt=150)
    email: EmailStr

class UserUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    email: EmailStr | None = None

class UserResponse(BaseModel):
    message: str
    data: User

class UsersListResponse(BaseModel):
    message: str
    data: list[User]

class DeleteResponse(BaseModel):
    message: str