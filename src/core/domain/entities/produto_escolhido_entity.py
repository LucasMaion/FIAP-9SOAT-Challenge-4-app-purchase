from typing import List, Optional

from src.core.domain.base.entity import Entity, PartialEntity
from src.core.domain.entities.produto_entity import PartialProdutoEntity, ProdutoEntity


class ProdutoEscolhidoEntity(Entity):
    product: PartialProdutoEntity
    added_components: Optional[List[PartialProdutoEntity]] = None


class PartialProdutoEscolhidoEntity(PartialEntity, ProdutoEscolhidoEntity):
    product: ProdutoEntity = None
