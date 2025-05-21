from decimal import Decimal
from src.core.domain.entities.produto_entity import PartialProdutoEntity
from src.core.domain.value_objects.preco_value_object import PrecoValueObject
from src.adapters.data_mappers.currency_entity_data_mapper import (
    CurrencyEntityDataMapper,
)
from src.adapters.data_mappers.categoria_entity_data_mapper import (
    CategoriaEntityDataMapper,
)


class ProdutoEntityDataMapper:
    @classmethod
    def from_api_to_domain(cls, api_response: dict):
        return PartialProdutoEntity(
            id=api_response["id"],
            name=api_response["name"],
            price=(
                PrecoValueObject(
                    value=round(Decimal(api_response["price"]["value"]), 2),
                    currency=CurrencyEntityDataMapper.from_api_to_domain(
                        api_response["price"]["currency"]
                    ),
                )
                if api_response["price"]["currency"]
                else None
            ),
            category=(
                CategoriaEntityDataMapper.from_api_to_domain(api_response["category"])
                if api_response["category"]
                else None
            ),
            created_at=api_response["created_at"],
            updated_at=api_response["updated_at"],
            deleted_at=api_response["deleted_at"],
            allow_components=api_response["allow_components"],
            is_active=api_response["is_active"],
            components=(
                [cls.from_api_to_domain(comp) for comp in api_response["components"]]
                if api_response.get("components", None)
                else None
            ),
        )
