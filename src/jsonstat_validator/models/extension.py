from pydantic import ConfigDict

from jsonstat_validator.models.base import JSONStatBaseModel


class Extension(JSONStatBaseModel):
    """Extension allows JSON-stat to be extended for particular needs.

    Providers are free to define where they include this property and
    what children are allowed in each case.
    """

    # Free-form dictionary of any properties.
    model_config = ConfigDict(extra="allow", serialize_by_alias=True)
