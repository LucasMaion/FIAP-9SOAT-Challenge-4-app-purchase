from src.core.domain.entities.categoria_entity import PartialCategoriaEntity


class CategoriaEntityDataMapper:
    @classmethod
    def from_api_to_domain(cls, api_response: dict):
        return PartialCategoriaEntity(
            id=api_response["id"],
            description=api_response["description"],
            is_component=api_response["is_component"],
            created_at=api_response["created_at"],
            updated_at=api_response["updated_at"],
            deleted_at=api_response["deleted_at"],
        )
