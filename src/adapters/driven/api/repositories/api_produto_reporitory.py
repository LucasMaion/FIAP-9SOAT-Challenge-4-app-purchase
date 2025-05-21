import os
from typing import List, Union

import requests
from src.adapters.data_mappers.produto_aggregate_data_mapper import (
    ProdutoAggregateDataMapper,
)
from src.core.domain.aggregates.produto_aggregate import ProdutoAggregate
from src.core.domain.entities.produto_entity import ProdutoEntity
from src.core.domain.entities.produto_escolhido_entity import ProdutoEscolhidoEntity
from src.core.domain.repositories.produto_repository import ProdutoRepository


class ApiProdutoRepository(ProdutoRepository):
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __init__(self, base_url: str = None):
        super().__init__()
        self.base_url = base_url or os.getenv(
            "PRODUTO_API_BASE_URL", "http://localhost:8003/dev/produto"
        )

    def get_from_purchase(self, purchase_id: int) -> List[ProdutoAggregate]:
        response = requests.get(f"{self.base_url}/purchase/{purchase_id}")
        produto = [
            ProdutoAggregateDataMapper.from_api_to_domain(r) for r in response.json()
        ]
        return produto

    def sync(
        self, purchase_id: int, selected_products: List[ProdutoEscolhidoEntity]
    ) -> ProdutoAggregate:
        request = {
            "purchase_id": purchase_id,
            "products": [
                {
                    "product_id": p.product.id,
                    "components": (
                        [component.id for component in p.added_components] or None
                    ),
                }
                for p in selected_products
            ],
        }
        response = requests.post("/add_purchase", json=request)
        produto = ProdutoAggregateDataMapper.from_api_to_domain(response.json())
        return produto

    def get_entity(self, produto_id: int) -> Union[ProdutoEntity, None]:
        response = requests.get(f"{self.base_url}/get_entity/{produto_id}")
        produto = ProdutoAggregateDataMapper.from_api_to_domain(response.json())
        return produto
