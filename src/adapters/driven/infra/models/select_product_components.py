from peewee import ForeignKeyField, IntegerField

from src.adapters.driven.infra.models.base_model import BaseModel
from src.adapters.driven.infra.models.select_product import SelectedProduct


class SelectedProductComponent(BaseModel):
    class Meta:
        db_table = "selected_product_component"

    selected_product = ForeignKeyField(SelectedProduct, backref="added_components")
    component = IntegerField()
