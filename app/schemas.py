from pydantic import BaseModel, Field  # type: ignore[import-not-found]



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