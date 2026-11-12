from typing import Literal, Optional

from pydantic import BaseModel, Field  # type: ignore[import-not-found]

# Simple regular expression to validate the format of an email address.
EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int = Field(gt=0)


class ProductCreate(BaseModel):
    name: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)         # ge=0 means Greater than or equal to 0


class ProductUpdate(BaseModel):
    price: float = Field(None, gt=0)
    stock: int = Field(None, ge=0)


# ---------- User module schemas (FR1) ----------

class UserCreate(BaseModel):
    """Data required to register a user."""
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(pattern=EMAIL_PATTERN)
    password: str = Field(min_length=6, max_length=100)
    role: Literal["customer", "admin"] = "customer"


class UserLogin(BaseModel):
    """Data required to log in."""
    email: str = Field(pattern=EMAIL_PATTERN)
    password: str


class UserUpdate(BaseModel):
    """Fields that can be changed on an existing user (all optional)."""
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    role: Optional[Literal["customer", "admin"]] = None