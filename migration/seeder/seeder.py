from decimal import Decimal
import os
import re
import sys
import random
from typing import List, Tuple
from faker import Faker


from src.adapters.driven.infra.models.address import Address
from src.adapters.driven.infra.models.currencies import Currency
from src.adapters.driven.infra.models.persona import Persona
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


def _seed_currency() -> int:
    currency = Currency(
        symbol="R$",
        name="Real",
        code="BRL",
        is_active=True,
    )
    currency.save()
    return currency.id


def _seed_purchases_selected_products_selected_products_components_and_payments(
    product_ids: List[int],
    components: List[List[int]],
    personas: List[int],
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
    total_value = 100
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

    # 2nd purchase
    second_products = [
        SelectedProduct(product=product_ids[1]),
        SelectedProduct(product=product_ids[2]),
        SelectedProduct(product=product_ids[0]),
    ]
    for product in second_products:
        product.save()
    total_value = 200
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
    # 3th purchase
    third_products = [
        SelectedProduct(product=product_ids[1]),
        SelectedProduct(product=product_ids[2]),
        SelectedProduct(product=product_ids[0]),
    ]
    for product in third_products:
        product.save()
    total_value = 300
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
    return [
        first_purchase.id,
        second_purchase.id,
        third_purchase.id,
    ]


def seed_data():
    addresses = _seed_address(5)
    personas = _seed_persona(5, addresses)
    _seed_user(3, personas)
    currency = _seed_currency()
    product_ids = [1, 2, 3, 4, 5, 6, 7]
    components = [[8, 10], [9, 11], [12]]  # 8,9,10,11,12
    _seed_purchases_selected_products_selected_products_components_and_payments(
        product_ids, components, personas
    )
