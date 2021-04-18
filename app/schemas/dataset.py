import pathlib
from typing import List

from pydantic import Field

from .response import BaseSchema, Paginator


class Dataset(BaseSchema):
    """A schema representing a dataset payload object."""

    name: str = Field(
        ...,
        max_length=255,
        example="Nearby Social Network - All Posts",
        description="Name of the dataset",
    )

    path: pathlib.Path = Field(
        ...,
        example="{shortuuid}/{file_name}.csv",
        description="Relative path to the dataset inside object storage",
    )


class DatasetList(BaseSchema, Paginator):
    """A schema representing collection of dataset objects."""

    datasets: List[Dataset] = []
