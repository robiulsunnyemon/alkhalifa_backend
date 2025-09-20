from pydantic import BaseModel
from datetime import datetime

class PaymentResponse(BaseModel):
    id: int
    user_id: int
    order_id: int
    total_amount: float
    trx_id: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True