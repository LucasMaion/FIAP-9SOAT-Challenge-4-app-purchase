from src.adapters.driven.infra.models.purchase_selected_products import (
    PurchaseSelectedProducts,
)
from src.core.domain.entities.produto_entity import PartialProdutoEntity
from src.core.domain.entities.produto_escolhido_entity import ProdutoEscolhidoEntity


class ProdutoEscolhidoEntityDataMapper:
    @classmethod
    def from_db_to_domain(
        cls,
        selected_product: PurchaseSelectedProducts,
    ):
        return ProdutoEscolhidoEntity(
            id=selected_product.product.id,
            product=PartialProdutoEntity(id=selected_product.product.product),
            added_components=[
                PartialProdutoEntity(id=added_comp.component)
                for added_comp in selected_product.product.added_components
            ]
            or [],
            created_at=selected_product.product.created_at,
            updated_at=selected_product.product.updated_at,
            deleted_at=selected_product.product.deleted_at,
        )

    @classmethod
    def from_domain_to_db(cls, selected_product: ProdutoEscolhidoEntity):
        return {
            "selected_product": selected_product.product.id,
            "components": [
                {"selected_product": selected_product.id, "component": comp.id}
                for comp in selected_product.added_components
            ],
        }
