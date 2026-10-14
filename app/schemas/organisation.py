
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class OrganisationCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(
        min_length=2,
        max_length=100,
        examples=["TCS"],
    )

    slug: str = Field(
        min_length=2,
        max_length=50,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
        examples=["tcs"],
    )


class OrganisationResponse(BaseModel):
    id: str
    name: str
    slug: str
    branch_name: str
    status: Literal[
        "PENDING",
        "PROVISIONING",
        "RUNNING",
        "FAILED",
    ]
