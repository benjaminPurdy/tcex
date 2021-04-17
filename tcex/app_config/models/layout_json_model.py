"""Layout JSON Model"""
# standard library
from functools import lru_cache
from typing import List, Optional, Union

# third-party
from pydantic import BaseModel
from pydantic.types import constr

# first-party
from tcex.pleb import NoneModel

__all__ = ['LayoutJsonModel']


def snake_to_camel(snake_string: str) -> str:
    """Convert snake_case to camelCase"""
    components = snake_string.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


class ParametersModel(BaseModel):

    display: Optional[str]
    name: str

    class Config:
        """DataModel Config"""

        alias_generator = snake_to_camel
        validate_assignment = True


class InputsModel(BaseModel):

    parameters: List[ParametersModel]
    sequence: int
    title: constr(min_length=3, max_length=100)

    class Config:
        """DataModel Config"""

        alias_generator = snake_to_camel
        validate_assignment = True


class OutputsModel(BaseModel):

    display: Optional[str]
    name: str

    class Config:
        """DataModel Config"""

        alias_generator = snake_to_camel
        validate_assignment = True


class LayoutJsonModel(BaseModel):
    """Layout JSON Model"""

    inputs: List[InputsModel]
    outputs: Optional[List[OutputsModel]]

    class Config:
        """DataModel Config"""

        alias_generator = snake_to_camel
        validate_assignment = True

    def get_param(self, name: str) -> Union[NoneModel, ParametersModel]:
        """Return the param or a None Model."""
        return self.params.get(name) or NoneModel()

    def get_output(self, name) -> Union[NoneModel, OutputsModel]:
        """Return layout.json outputs in a flattened dict with name param as key."""
        return self.outputs_.get(name) or NoneModel

    @property
    @lru_cache
    def outputs_(self) -> dict[str, OutputsModel]:
        """Return layout.json outputs in a flattened dict with name param as key."""
        return {o.name: o for o in self.outputs}

    @property
    @lru_cache
    def param_names(self) -> list:
        """Return all param names in a single list."""
        return self.params.keys()

    @property
    @lru_cache
    def params(self) -> dict[str, ParametersModel]:
        """Return layout.json params in a flattened dict with name param as key."""
        parameters = {}
        for i in self.inputs:
            for p in i.parameters:
                parameters.setdefault(p.name, p)
        return parameters