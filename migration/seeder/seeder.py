from decimal import Decimal
import os
import re
import sys
import random
from typing import List, Tuple
from faker import Faker


from src.adapters.driven.infra.models.address import Address
from src.adapters.driven.infra.models.categories import Category
from src.adapters.driven.infra.models.currencies import Currency
from src.adapters.driven.infra.models.payment_methods import PaymentMethod
from src.adapters.driven.infra.models.persona import Persona
from src.adapters.driven.infra.models.product_components import ProductComponent
from src.adapters.driven.infra.models.products import Product
from src.adapters.driven.infra.models.purchases import Purchase
from src.adapters.driven.infra.models.purchase_selected_products import (
    PurchaseSelectedProducts,
)
from src.adapters.driven.infra.models.select_product import SelectedProduct
from src.adapters.driven.infra.models.select_product_components import (
    SelectedProductComponent,
)
from src.adapters.driven.infra.models.payments import Payment
from src.adapters.driven.infra.models.user import User

fake = Faker("pt_BR")


def _seed_address(amount: int) -> List[int]:
    ids = []
    for _ in range(amount):
        address: Address = Address(
            zip_code=fake.postcode(),
            street=fake.street_name(),
            number=fake.random_number(3),
            city=fake.city(),
            state=fake.state(),
            country=fake.country(),
            additional_information=fake.random_letters(15),
        )

        address.save()
        ids.append(address.id)
    return ids


def _seed_persona(amount: int, address_ids: List[int]) -> List[int]:
    ids = []
    for index in range(amount):
        persona = Persona(
            name=fake.name(),
            document=re.sub(r"\D", "", fake.cpf()),
            email=fake.email(),
            phone=re.sub(r"\D", "", fake.phone_number()),
            birth_date=fake.date_of_birth(),
            address=address_ids[index],
        )
        persona.save()
        ids.append(persona.id)
    return ids


def _seed_user(amount: int, person_ids: List[int]) -> List[int]:
    ids = []
    for index in range(amount):
        if index >= len(person_ids):
            break
        user = User(
            username=fake.email(), password=fake.password(), person=person_ids[index]
        )
        user.save()
        ids.append(user.id)
    return ids


def _seed_category() -> List[int]:
    bebidas = Category(
        name="Bebidas",
        description="Bebidas refrigerantes, sucos, água, etc.",
        is_component=False,
    )
    bebidas.save()
    lanches = Category(
        name="Lanches",
        description="Lanches e produtos principais",
        is_component=False,
    )
    lanches.save()
    acompanhamentos = Category(
        name="Acompanhamentos",
        description="Batatas fritas, nuggets, etc.",
        is_component=False,
    )
    acompanhamentos.save()
    adicionais = Category(
        name="Adicionais",
        description="Queijo, bacon, hambúrguer, etc.",
        is_component=True,
    )
    adicionais.save()
    return [bebidas.id, lanches.id, acompanhamentos.id, adicionais.id]


def _seed_currency() -> int:
    currency = Currency(
        symbol="R$",
        name="Real",
        code="BRL",
        is_active=True,
    )
    currency.save()
    return currency.id


def _seed_payment_methods() -> int:
    payment_method = PaymentMethod(
        name="Mercado Pago QR Code",
        sys_name="DefaultPaymentProvider",
        internal_comm_method_name="PaymentEvent.internal_finalize_payment",
        internal_comm_delay=5,
        description="Pagamento para processar pelo mercado pago, cliente escaneia o QR Code para realizar transação.",
        is_active=True,
    )
    payment_method.save()
    return payment_method.id


def _seed_product_and_product_components(
    bebida_id: List[int], lanche_id: int, acompanhamento_id: int, adicional_id: int
) -> Tuple[List[int], List[List[int]]]:

    big = Product(
        name="Big Lanche",
        description="big lanchinho",
        price=Decimal(27.90),
        category=lanche_id,
        allow_components=True,
        is_active=True,
        currency=1,
    )
    big.save()
    chester_b = Product(
        name="Chester Burger",
        description="diferentão",
        price=Decimal(32.90),
        category=lanche_id,
        allow_components=True,
        is_active=True,
        currency=1,
    )
    chester_b.save()
    cocorico = Product(
        name="Cocoricó",
        description="franguinho",
        price=Decimal(22.90),
        category=lanche_id,
        allow_components=True,
        is_active=True,
        currency=1,
    )
    cocorico.save()
    fritas = Product(
        name="Fritas",
        description="fritinhas",
        price=Decimal(12.90),
        category=acompanhamento_id,
        is_active=True,
        currency=1,
    )
    fritas.save()
    fritas_special = Product(
        name="Fritas Special",
        description="fritinhas",
        price=Decimal(12.90),
        category=acompanhamento_id,
        is_active=False,
        currency=1,
    )
    fritas_special.save()
    nuggets = Product(
        name="nuggets",
        description=fake.sentence(),
        price=fake.random_number(2),
        category=acompanhamento_id,
        is_active=True,
        currency=1,
    )
    nuggets.save()
    doll = Product(
        name="doll cola",
        description="refri",
        price=Decimal(5.90),
        category=bebida_id,
        is_active=True,
        currency=1,
    )
    doll.save()
    sukinho = Product(
        name="sukinho",
        description="suco",
        price=Decimal(4.90),
        category=bebida_id,
        is_active=True,
        currency=1,
    )
    sukinho.save()
    hambuguer = Product(
        name="hambuguer",
        price=Decimal(5),
        category=adicional_id,
        is_active=True,
        currency=1,
    )
    chicken = Product(
        name="chicken",
        price=Decimal(5),
        category=adicional_id,
        is_active=True,
        currency=1,
    )
    chicken.save()
    hambuguer.save()
    queijo = Product(
        name="queijo",
        price=Decimal(2),
        category=adicional_id,
        is_active=True,
        currency=1,
    )
    queijo.save()
    bacon = Product(
        name="bacon",
        price=Decimal(3),
        category=adicional_id,
        is_active=True,
        currency=1,
    )
    bacon.save()
    chester = Product(
        name="chester",
        price=Decimal(6),
        category=adicional_id,
        is_active=True,
        currency=1,
    )
    chester.save()
    big_comps = [
        ProductComponent(product=big.id, component=hambuguer.id),
        ProductComponent(product=big.id, component=queijo.id),
    ]
    for big_comp in big_comps:
        big_comp.save()
    big_comps = [big_comp.id for big_comp in big_comps]

    cocorico_comps = [
        ProductComponent(product=cocorico.id, component=chicken.id),
        ProductComponent(product=cocorico.id, component=bacon.id),
    ]
    for cocorico_comp in cocorico_comps:
        cocorico_comp.save()
    cocorico_comps = [cocorico_comp.id for cocorico_comp in cocorico_comps]

    chester_b_comps = [
        ProductComponent(product=chester_b.id, component=chester.id),
    ]
    for chester_b_comp in chester_b_comps:
        chester_b_comp.save()
    chester_b_comps = [chester_b_comp.id for chester_b_comp in chester_b_comps]

    return [
        big.id,
        chester_b.id,
        cocorico.id,
        fritas.id,
        nuggets.id,
        doll.id,
        sukinho.id,
    ], [big_comps, cocorico_comps, chester_b_comps]


def _seed_purchases_selected_products_selected_products_components_and_payments(
    product_ids: List[int],
    components: List[List[int]],
    personas: List[int],
    payment_method: int,
    currency: int,
):
    # 1st purchase
    first_products = [
        SelectedProduct(product=product_ids[0]),
        SelectedProduct(product=product_ids[2]),
        SelectedProduct(product=product_ids[0]),
    ]
    for product in first_products:
        product.save()
    component = SelectedProductComponent(
        selected_product=first_products[0].id, component=components[0][0]
    )
    component.save()
    total_value = sum([product.product.price for product in first_products])
    first_purchase = Purchase(
        status=1, total_value=total_value, currency=1, client=personas[0]
    )
    first_purchase.save()
    purchase_selected_products = []
    for product in first_products:
        product.save()
        purchase_selected_products.append(
            PurchaseSelectedProducts(product=product.id, purchase=first_purchase.id)
        )
        purchase_selected_products[-1].save()
    first_payment = Payment(
        payment_method=payment_method,
        currency=currency,
        value=total_value,
        status=4,
        purchase=first_purchase.id,
    )
    first_payment.save()

    # 2nd purchase
    second_products = [
        SelectedProduct(product=product_ids[1]),
        SelectedProduct(product=product_ids[2]),
        SelectedProduct(product=product_ids[0]),
    ]
    for product in second_products:
        product.save()
    total_value = sum([product.product.price for product in second_products])
    second_purchase = Purchase(
        status=6, total_value=total_value, currency=1, client=personas[0]
    )
    second_purchase.save()
    purchase_selected_products = []
    for product in second_products:
        product.save()
        purchase_selected_products.append(
            PurchaseSelectedProducts(product=product.id, purchase=second_purchase.id)
        )
        purchase_selected_products[-1].save()
    second_payment = Payment(
        payment_method=payment_method,
        currency=currency,
        value=total_value,
        status=2,
        purchase=second_purchase.id,
    )
    second_payment.save()
    # 3th purchase
    third_products = [
        SelectedProduct(product=product_ids[1]),
        SelectedProduct(product=product_ids[2]),
        SelectedProduct(product=product_ids[0]),
    ]
    for product in third_products:
        product.save()
    total_value = sum([product.product.price for product in third_products])
    third_purchase = Purchase(
        status=7, total_value=total_value, currency=1, client=personas[0]
    )
    third_purchase.save()
    purchase_selected_products = []
    for product in third_products:
        product.save()
        purchase_selected_products.append(
            PurchaseSelectedProducts(product=product.id, purchase=third_purchase.id)
        )
        purchase_selected_products[-1].save()
    third_payment = Payment(
        payment_method=payment_method,
        currency=currency,
        value=total_value,
        status=3,
        purchase=third_purchase.id,
    )
    third_payment.save()
    return [
        first_purchase.id,
        second_purchase.id,
        third_purchase.id,
    ]


def seed_data():
    addresses = _seed_address(5)
    personas = _seed_persona(5, addresses)
    _seed_user(3, personas)
    bebidas, lanches, acompanhamentos, adicionais = _seed_category()
    currency = _seed_currency()
    payment_method = _seed_payment_methods()
    product_ids, components = _seed_product_and_product_components(
        bebidas, lanches, acompanhamentos, adicionais
    )
    _seed_purchases_selected_products_selected_products_components_and_payments(
        product_ids, components, personas, payment_method, currency
    )
