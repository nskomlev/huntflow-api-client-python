from typing import Optional

from huntflow_api_client.entities.base import BaseEntity, CreateEntityMixin, ListEntityMixin
from huntflow_api_client.models.request.divisions import BatchDivisionsRequest
from huntflow_api_client.models.response.divisions import (
    BatchDivisionsResponse,
    DivisionsListResponse,
)


class AccountDivision(BaseEntity, ListEntityMixin, CreateEntityMixin):
    async def list(  # noqa: A003
        self,
        account_id: int,
        coworker_id: Optional[int] = None,
    ) -> DivisionsListResponse:
        path = f"/accounts/{account_id}"
        if coworker_id is not None:
            path += f"/coworkers/{coworker_id}"
        path += "/divisions"
        response = await self._api.request(
            "GET",
            path,
        )
        return DivisionsListResponse.parse_obj(response.json())

    async def create(
        self,
        account_id: int,
        divisions: BatchDivisionsRequest,
    ) -> BatchDivisionsResponse:
        response = await self._api.request(
            "POST",
            f"/accounts/{account_id}/divisions/batch",
            json=divisions.jsonable_dict(),
        )
        return BatchDivisionsResponse.parse_obj(response.json())
