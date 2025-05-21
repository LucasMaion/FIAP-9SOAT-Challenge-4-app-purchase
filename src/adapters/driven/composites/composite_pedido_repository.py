from datetime import datetime
from typing import List, Optional, Union
from src.adapters.data_mappers.compra_data_mapper import CompraEntityDataMapper
from src.adapters.data_mappers.pagamento_data_mapper import PagamentoEntityDataMapper
from src.adapters.data_mappers.pedido_aggregate_data_mapper import (
    PedidoAggregateDataMapper,
)
from src.adapters.driven.api.repositories.api_produto_reporitory import (
    ApiProdutoRepository,
)
from src.adapters.driven.infra.models.payments import Payment
from src.adapters.driven.infra.models.purchase_selected_products import (
    PurchaseSelectedProducts,
)
from src.adapters.driven.infra.models.purchases import Purchase
from src.adapters.driven.infra.models.select_product import SelectedProduct
from src.adapters.driven.infra.models.select_product_components import (
    SelectedProductComponent,
)
from src.adapters.driven.infra.ports.orm_pedido_query import OrmPedidoQuery
from src.adapters.driven.infra.repositories.orm_pedido_repository import (
    OrmPedidoRepository,
)
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.domain.entities.compra_entity import CompraEntity, PartialCompraEntity
from src.core.domain.repositories.pedido_repository import PedidoRepository
from src.core.helpers.options.pedido_find_options import PedidoFindOptions


class CompositePedidoRepository(PedidoRepository):

    def __init__(self):
        super().__init__()
        self.ormPedidoRepository = OrmPedidoRepository()
        self.apiProdutoRepository = ApiProdutoRepository()

    def create(self, pedido: PartialCompraEntity) -> PedidoAggregate:
        purchase = self.ormPedidoRepository.create(pedido)
        self.apiProdutoRepository.sync(purchase.purchase.selected_products)
        return purchase

    def update(self, pedido: CompraEntity) -> PedidoAggregate:
        purchase = self.ormPedidoRepository.update(pedido)
        self.apiProdutoRepository.sync(purchase.purchase.selected_products)
        return purchase

    def delete(self, pedido_id: int):
        purchase = self.ormPedidoRepository.delete(pedido_id)
        return purchase

    def get_by_purchase_id(self, pedido_id: int) -> PedidoAggregate:
        pedido = self.cache_service.get(pedido_id)
        if pedido:
            return pedido
        pedido = self.ormPedidoRepository.get_by_purchase_id(pedido_id)
        self.apiProdutoRepository.get_from_purchase(pedido_id)
        return pedido

    def find(self, query_options: PedidoFindOptions) -> list[PedidoAggregate]:
        return self.ormPedidoRepository.find(query_options)
