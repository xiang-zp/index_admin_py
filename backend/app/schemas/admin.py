from pydantic import BaseModel
from typing import Optional


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminUserResponse(BaseModel):
    id: str
    username: str
    role: str


class AdminLoginResponse(BaseModel):
    token: str
    user: AdminUserResponse
