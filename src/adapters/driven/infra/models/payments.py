from peewee import ForeignKeyField, IntegerField

from src.adapters.driven.infra.models.base_model import BaseModel
from src.adapters.driven.infra.models.purchases import Purchase


class Payment(BaseModel):
    payment = IntegerField()
    purchase = ForeignKeyField(Purchase, backref="payments", null=True, unique=True)
