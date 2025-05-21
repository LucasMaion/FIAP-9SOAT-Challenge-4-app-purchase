from src.adapters.driven.infra.models.currencies import Currency
from src.core.domain.entities.currency_entity import PartialCurrencyEntity


class CurrencyEntityDataMapper:
    @classmethod
    def from_db_to_domain(cls, currency: Currency):
        return PartialCurrencyEntity(
            id=currency.id,
            name=currency.name,
            symbol=currency.symbol,
            code=currency.code,
            created_at=currency.created_at,
            updated_at=currency.updated_at,
            deleted_at=currency.deleted_at,
        )

    @classmethod
    def from_api_to_domain(cls, api_response: dict):
        return PartialCurrencyEntity(
            id=api_response["id"],
            name=api_response["name"],
            symbol=api_response["symbol"],
            code=api_response["code"],
            created_at=api_response["created_at"],
            updated_at=api_response["updated_at"],
            deleted_at=api_response["deleted_at"],
        )
