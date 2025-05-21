from src.adapters.data_mappers.compra_data_mapper import CompraEntityDataMapper
from src.adapters.data_mappers.pagamento_data_mapper import PagamentoEntityDataMapper
from src.adapters.driven.infra.models.payments import Payment
from src.core.domain.aggregates.pagamento_aggregate import PagamentoAggregate
from src.core.domain.entities.compra_entity import CompraEntity


class PagamentoAggregateDataMapper:
    @classmethod
    def from_db_to_domain(cls, payment: Payment) -> PagamentoAggregate:
        return PagamentoAggregate(
            purchase=(
                CompraEntityDataMapper.from_db_to_domain(payment.purchase)
                if hasattr(payment, "purchase")
                else None
            ),
            payment=PagamentoEntityDataMapper.from_db_to_domain(payment),
        )

    @classmethod
    def from_api_to_domain(
        cls, api_response: dict, purchase: CompraEntity = None
    ) -> PagamentoAggregate:
        return PagamentoAggregate(
            purchase=purchase,
            payment=PagamentoEntityDataMapper.from_api_to_domain(api_response),
        )
