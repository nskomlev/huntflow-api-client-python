from __future__ import annotations

import datetime
import typing as t
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, PositiveInt

from huntflow_api_client.models.common import File, PaginatedResponse


class VacancyRequestStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class UserInfo(BaseModel):
    id: PositiveInt = Field(
        ...,
        description="Coworker who create the vacancy request",
    )
    name: str = Field(
        ...,
        description="Name of coworker who create the vacancy request",
        example="John Doe",
    )
    email: EmailStr = Field(..., description="Email of coworker who create the vacancy request")


class VacancyRequestApprovalState(BaseModel):
    id: PositiveInt = Field(..., description="Approval ID")

    status: VacancyRequestStatus = Field(..., description="Approval status")
    email: EmailStr = Field(
        ...,
        description="Email, which was used to send the request for approval",
    )
    reason: t.Optional[str] = Field(
        None,
        description="Rejection reason",
        example="Inappropriate qualifications",
    )
    order: t.Optional[int] = Field(None, description="Approval order number", example=2)
    changed: t.Optional[datetime.datetime] = Field(
        None,
        description="Date and time of the last approval change",
    )


class VacancyRequest(BaseModel):
    id: PositiveInt = Field(..., description="Vacancy request ID")
    position: str = Field(
        ...,
        description="The name of the vacancy (occupation)",
        example="Developer",
    )
    status: VacancyRequestStatus = Field(..., description="Vacancy request status")
    account_vacancy_request: PositiveInt = Field(
        ...,
        description="Account vacancy request ID",
    )
    created: datetime.datetime = Field(..., description="Date and time of creation of the request")
    updated: t.Optional[datetime.datetime] = Field(
        None,
        description="Date and time of editing of the request",
    )
    changed: t.Optional[datetime.datetime] = Field(
        None,
        description="Date and time of attaching to vacancy",
    )
    vacancy: t.Optional[PositiveInt] = Field(None, description="Vacancy ID")
    creator: UserInfo = Field(..., description="User who create the request")
    files: t.Optional[t.List[File]] = Field(
        None,
        description="List of files attached to the request",
    )
    states: t.List[VacancyRequestApprovalState] = Field(..., description="List of approval states")
    values: t.Optional[t.Dict] = Field(
        None,
        description="Vacancy request values, depends on account_vacancy_request",
        example={"position": "Developer", "account_division": 1844, "category": 687},
    )


class VacancyRequestListResponse(PaginatedResponse):
    total_items: t.Optional[int] = Field(..., description="Total number of items", example=50)
    items: t.List[VacancyRequest]


class VacancyRequestResponse(VacancyRequest):
    taken_by: t.Optional[UserInfo] = Field(
        None,
        description="User who accepted the vacancy request for work",
    )