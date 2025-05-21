from datetime import datetime
import logging
from unittest.mock import MagicMock
import pytest
from pytest_bdd import scenario, given, when, then
from copy import deepcopy

from src.core.application.ports.pedido_query import PedidoQuery
from src.core.application.ports.produto_query import ProdutoQuery
from src.core.application.services.pedido_service_command import PedidoServiceCommand
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.domain.entities.categoria_entity import CategoriaEntity
from src.core.domain.entities.cliente_entity import ClienteEntity
from src.core.domain.entities.compra_entity import CompraEntity
from src.core.domain.entities.currency_entity import CurrencyEntity
from src.core.domain.entities.meio_de_pagamento_entity import MeioDePagamentoEntity
from src.core.domain.entities.pagamento_entity import PagamentoEntity
from src.core.domain.entities.produto_entity import PartialProdutoEntity, ProdutoEntity
from src.core.domain.entities.produto_escolhido_entity import ProdutoEscolhidoEntity
from src.core.domain.value_objects.address_value_object import AddressValueObject
from src.core.domain.value_objects.persona_value_object import PersonaValueObject
from src.core.helpers.enums.compra_status import CompraStatus
from src.core.helpers.enums.pagamento_status import PagamentoStatus
from src.core.domain.value_objects.preco_value_object import PrecoValueObject
from src.core.helpers.interfaces.chace_service import CacheService


@pytest.fixture
def produto_query():
    return MagicMock()


@pytest.fixture
def purchase_query():
    return MagicMock()


@pytest.fixture
def purchase_repository():
    return MagicMock()


@pytest.fixture
def cache_service():
    return MagicMock()


@pytest.fixture
def purchase_service(
    purchase_repository: PedidoAggregate,
    purchase_query: PedidoQuery,
    produto_query: ProdutoQuery,
    cache_service: CacheService,
):
    cache_service.get = MagicMock(return_value=None)
    cache_service.set = MagicMock(return_value=None)
    return PedidoServiceCommand(
        purchase_repository=purchase_repository,
        purchase_query=purchase_query,
        produto_repository=produto_query,
        cache_service=cache_service,
    )


@pytest.fixture
def currency():
    return CurrencyEntity(
        id=1,
        symbol="R$",
        name="Real",
        code="BRL",
        created_at=datetime(2021, 1, 1),
        updated_at=datetime(2021, 1, 1),
    )


@pytest.fixture
def preco(currency: CurrencyEntity):
    return PrecoValueObject(
        value=10,
        currency=currency,
    )


@pytest.fixture
def client_entity():
    return ClienteEntity(
        id=1,
        orders=[],
        person=PersonaValueObject(
            name="Test",
            document="12345678900",
            email="email.test@teste.test",
            address=AddressValueObject(
                zip_code="12345678",
                street="Test",
                number="123",
                city="Test",
                state="Test",
                country="Test",
                additional_information="Test",
            ),
            birth_date=datetime(2021, 1, 1),
            phone="11999999999",
        ),
        created_at=datetime(2021, 1, 1),
        updated_at=datetime(2021, 1, 1),
    )


@pytest.fixture
def product_entity(preco: PrecoValueObject):
    produto_entity = ProdutoEntity(
        id=1,
        name="added_component",
        description="produto_test_mock",
        price=preco,
        category=CategoriaEntity(
            name="categoria",
            id=1,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        ),
        is_active=False,
        created_at=datetime(2021, 1, 1),
        updated_at=datetime(2021, 1, 1),
        components=[PartialProdutoEntity(id=2), PartialProdutoEntity(id=3)],
        allow_components=False,
    )
    components = [deepcopy(produto_entity) for _ in range(2)]
    for component in components:
        component.id += 1
    produto_entity.components = components
    return produto_entity


@pytest.fixture
def partial_product_entity(preco: PrecoValueObject):
    produto_entity = PartialProdutoEntity(
        id=1,
        name="added_component",
        description="produto_test_mock",
        price=preco,
        category=CategoriaEntity(
            name="categoria",
            id=1,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        ),
        is_active=False,
        created_at=datetime(2021, 1, 1),
        updated_at=datetime(2021, 1, 1),
        components=[PartialProdutoEntity(id=2), PartialProdutoEntity(id=3)],
        allow_components=False,
    )
    components = [deepcopy(produto_entity) for _ in range(2)]
    for component in components:
        component.id += 1
    produto_entity.components = components
    return produto_entity


@pytest.fixture
def selected_product_entity(partial_product_entity: ProdutoEntity):
    component = deepcopy(partial_product_entity)
    component.id = 2
    return ProdutoEscolhidoEntity(
        id=1,
        product=partial_product_entity,
        added_components=[component],
        created_at=datetime(2021, 1, 1),
        updated_at=datetime(2021, 1, 1),
    )


@pytest.fixture
def compra_entity(
    client_entity: ClienteEntity,
    selected_product_entity: ProdutoEscolhidoEntity,
    currency: CurrencyEntity,
):
    return CompraEntity(
        id=1,
        client=client_entity,
        selected_products=[selected_product_entity],
        status=CompraStatus.CRIANDO,
        total=PrecoValueObject(value=0, currency=currency),
        created_at=datetime(2021, 1, 1),
        updated_at=datetime(2021, 1, 1),
    )


@pytest.fixture
def pagamento_entity(compra_entity: CompraEntity, preco: PrecoValueObject):
    pagamento_price = deepcopy(preco)
    pagamento_price.value = 20
    return PagamentoEntity(
        id=1,
        payment_method=MeioDePagamentoEntity(
            id=1,
            name="mock_payment_method",
            sys_name="mock_payment_method",
            description="This is a mock payment method",
            is_active=True,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        ),
        payment_value=pagamento_price,
        status=PagamentoStatus.PAGO,
        purchase=compra_entity,
        created_at=datetime(2021, 1, 1),
        updated_at=datetime(2021, 1, 1),
    )


@pytest.fixture
def pedido_aggregate(
    compra_entity: CompraEntity,
    pagamento_entity: PagamentoEntity,
):
    return PedidoAggregate(
        purchase=compra_entity,
        payments=[pagamento_entity],
    )


@pytest.fixture
def context():
    return {}


@scenario("test_conclude_purchase.feature", "Successfully conclude a purchase")
def test_conclude_purchase_successfully():
    pass


@given("an existing purchase with products")
def given_existing_purchase_with_products(context, pedido_aggregate):
    logging.info("Step: Given an existing purchase with products")
    context["pedido"] = deepcopy(pedido_aggregate)
    context["pedido"].purchase.selected_products.append(
        deepcopy(context["pedido"].purchase.selected_products[0])
    )


@given("the purchase has a successful payment")
def given_successful_payment(context):
    logging.info("Step: And the purchase has a successful payment")
    context["pedido"].payments[0].status = PagamentoStatus.PAGO


@given("the purchase total value is greater than zero")
def given_positive_total(context, currency):
    logging.info("Step: And the purchase total value is greater than zero")
    context["pedido"].purchase.total = PrecoValueObject(value=100, currency=currency)


@when("I conclude the purchase")
def when_conclude_purchase(context, purchase_service):
    logging.info("Step: When I conclude the purchase")
    purchase_service.purchase_repository.get_by_purchase_id = lambda _: context[
        "pedido"
    ]
    purchase_service.purchase_repository.update = lambda x: x
    context["result"] = purchase_service.concludes_pedido(1)


@then("the purchase should be concluded successfully")
def then_purchase_concluded(context):
    logging.info("Step: Then the purchase should be concluded successfully")
    assert context["result"].status == CompraStatus.CONCLUIDO
