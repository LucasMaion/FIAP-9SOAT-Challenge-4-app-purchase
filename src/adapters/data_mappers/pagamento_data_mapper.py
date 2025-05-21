from decimal import Decimal
from typing import Optional
from src.adapters.data_mappers.currency_entity_data_mapper import (
    CurrencyEntityDataMapper,
)
from src.adapters.data_mappers.meio_de_pagamento_data_mapper import (
    MeioDePagamentoEntityDataMapper,
)
from src.adapters.driven.infra.models.payments import Payment
from src.core.domain.entities.compra_entity import PartialCompraEntity
from src.core.domain.entities.pagamento_entity import (
    PartialPagamentoEntity,
)
from src.core.domain.value_objects.preco_value_object import PrecoValueObject
from src.core.helpers.enums.pagamento_status import PagamentoStatus


class PagamentoEntityDataMapper:
    @classmethod
    def from_api_to_domain(cls, api_response: dict):
        return PartialPagamentoEntity(
            id=api_response["id"],
            created_at=api_response["created_at"],
            updated_at=api_response["updated_at"],
            deleted_at=api_response["deleted_at"],
            payment_method=MeioDePagamentoEntityDataMapper.from_api_to_domain(
                api_response["payment_method"]
            ),
            status=PagamentoStatus(api_response["status"]),
            payment_value=PrecoValueObject(
                value=Decimal(api_response["value"]),
                currency=CurrencyEntityDataMapper.from_db_to_domain(
                    api_response["currency"]
                ),
            ),
        )
