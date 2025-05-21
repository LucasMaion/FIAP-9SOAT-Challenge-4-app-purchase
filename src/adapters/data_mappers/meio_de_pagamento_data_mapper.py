from src.core.domain.entities.meio_de_pagamento_entity import MeioDePagamentoEntity


class MeioDePagamentoEntityDataMapper:
    @classmethod
    def from_api_to_domain(cls, api_response: dict):
        return MeioDePagamentoEntity(
            id=api_response["id"],
            sys_name=api_response["sys_name"],
            created_at=api_response["created_at"],
            updated_at=api_response["updated_at"],
            deleted_at=api_response["deleted_at"],
            name=api_response["name"],
            description=api_response["description"],
            is_active=api_response["is_active"],
            internal_comm_method_name=api_response["internal_comm_method_name"],
            internal_comm_delay=api_response["internal_comm_delay"],
        )
