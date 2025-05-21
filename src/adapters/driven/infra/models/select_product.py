from peewee import IntegerField

from src.adapters.driven.infra.models.base_model import BaseModel


class SelectedProduct(BaseModel):
    class Meta:
        db_table = "selected_product"

    product = IntegerField()
