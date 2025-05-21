from typing import List, Optional
from src.adapters.data_mappers.produto_entity_data_mapper import ProdutoEntityDataMapper
from src.adapters.driven.infra.models.purchases import Purchase
from src.core.domain.aggregates.produto_aggregate import ProdutoAggregate
from src.core.helpers.enums.compra_status import CompraStatus


class ProdutoAggregateDataMapper:
    @classmethod
    def from_api_to_domain(
        cls, api_response: dict, purchases: Optional[List[Purchase]] = None
    ):
        return ProdutoAggregate(
            orders=purchases if purchases else [],
            product=ProdutoEntityDataMapper.from_api_to_domain(api_response),
            sold_amount=(
                len(
                    [
                        purchase
                        for purchase in purchases
                        if not purchase.status == CompraStatus.CANCELADO
                    ]
                )
                if purchases
                else 0
            ),
        )
