from src.adapters.driven.infra import db
from src.adapters.driven.infra.models.address import Address
from src.adapters.driven.infra.models.currencies import Currency
from src.adapters.driven.infra.models.payments import Payment
from src.adapters.driven.infra.models.persona import Persona
from src.adapters.driven.infra.models.purchase_selected_products import (
    PurchaseSelectedProducts,
)
from src.adapters.driven.infra.models.purchases import Purchase
from src.adapters.driven.infra.models.select_product import SelectedProduct

from src.adapters.driven.infra.models.select_product_components import (
    SelectedProductComponent,
)
from src.adapters.driven.infra.models.user import User


def create_tables():
    db.create_tables(
        [
            Address,
            Currency,
            Payment,
            Persona,
            PurchaseSelectedProducts,
            Purchase,
            SelectedProductComponent,
            SelectedProduct,
            User,
        ],
        safe=True,
    )
