"""SecurityLabel / SecurityLabels Object"""
# standard library
import json
from typing import Optional

# first-party
from tcex.api.tc.v3.api_endpoints import ApiEndpoints
from tcex.api.tc.v3.object_abc import ObjectABC
from tcex.api.tc.v3.object_collection_abc import ObjectCollectionABC
from tcex.api.tc.v3.security_labels.security_label_filter import SecurityLabelFilter
from tcex.api.tc.v3.security_labels.security_label_model import (
    SecurityLabelModel,
    SecurityLabelsModel,
)


class SecurityLabels(ObjectCollectionABC):
    """SecurityLabels Collection.

    # Example of params input
    {
        'result_limit': 100,  # Limit the retrieved results.
        'result_start': 10,  # Starting count used for pagination.
        'fields': ['caseId', 'summary']  # Select additional return fields.
    }

    Args:
        session (Session): Session object configured with TC API Auth.
        tql_filters (list): List of TQL filters.
        params (dict): Additional query params (see example above).
    """

    def __init__(self, **kwargs) -> None:
        """Initialize class properties."""
        super().__init__(
            kwargs.pop('session', None), kwargs.pop('tql_filter', None), kwargs.pop('params', None)
        )
        self._model = SecurityLabelsModel(**kwargs)
        self.type_ = 'security_labels'

    def __iter__(self) -> 'SecurityLabel':
        """Iterate over CM objects."""
        return self.iterate(base_class=SecurityLabel)

    @property
    def _api_endpoint(self) -> str:
        """Return the type specific API endpoint."""
        return ApiEndpoints.SECURITY_LABELS.value

    @property
    def filter(self) -> 'SecurityLabelFilter':
        """Return the type specific filter object."""
        return SecurityLabelFilter(self.tql)


class SecurityLabel(ObjectABC):
    """SecurityLabels Object.

    Args:
        color (str, kwargs): Color of the security label.
        description (str, kwargs): Description of the security label.
        name (str, kwargs): Name of the security label.
        owner (str, kwargs): The name of the Owner of the Label.
    """

    def __init__(self, **kwargs) -> None:
        """Initialize class properties."""
        super().__init__(kwargs.pop('session', None))

        # properties
        self._model = SecurityLabelModel(**kwargs)
        self._nested_field_name = 'securityLabels'
        self._nested_filter = 'has_security_label'
        self.type_ = 'Security Label'

    @property
    def _api_endpoint(self) -> str:
        """Return the type specific API endpoint."""
        return ApiEndpoints.SECURITY_LABELS.value

    def remove(self, params: Optional[dict] = None) -> None:
        """Remove a nested object."""
        method = 'PUT'
        unique_id = self._calculate_unique_id()

        # validate an id is available
        self._validate_id(unique_id.get('value'), '')

        body = json.dumps(
            {
                self._nested_field_name: {
                    'data': [{unique_id.get('filter'): unique_id.get('value')}],
                    'mode': 'delete',
                }
            }
        )

        # get the unique id value for id, xid, summary, etc ...
        parent_api_endpoint = self._parent_data.get('api_endpoint')
        parent_unique_id = self._parent_data.get('unique_id')
        url = f'{parent_api_endpoint}/{parent_unique_id}'

        # validate parent an id is available
        self._validate_id(parent_unique_id, url)

        self._request(
            method=method,
            url=url,
            body=body,
            headers={'content-type': 'application/json'},
            params=params,
        )

        return self.request