from pydantic import BaseModel


class UpdateStatusSchema(BaseModel):
    pedido_id: int
    status: str
