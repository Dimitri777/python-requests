from pydantic import BaseModel


class UserModel(BaseModel):
    user_id: str
    email: str
    name: str
    age: int
    is_student: bool

response = {
    "user_id": "abc-777-41_xyz",
    "email": "abc@yahoo.com",
    "name": "Dick",
    "age": 33,
    "is_student": False
}

user = UserModel(**response)
print(user.name)
print(user.model_dump_json())
