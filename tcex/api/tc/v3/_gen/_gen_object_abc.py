"""Generate Object for ThreatConnect API"""
# standard library
from abc import ABC
from typing import Dict, List, Optional

# first-party
from tcex.api.tc.v3._gen._gen_abc import GenerateABC
from tcex.api.tc.v3._gen._gen_args_abc import GenerateArgsABC


class GenerateArgs(GenerateArgsABC):
    """Generate Models for TC API Types"""


class GenerateObjectABC(GenerateABC, ABC):
    """Generate Models for Case Management Types"""

    def __init__(self, type_: str) -> None:
        """Initialize class properties."""
        super().__init__(type_)

        # properties
        self.requirements = {
            'standard library': [],
            'third-party': [],
            'first-party': [
                'from tcex.api.tc.v3.api_endpoints import ApiEndpoints',
                'from tcex.api.tc.v3.object_abc import ObjectABC',
                'from tcex.api.tc.v3.object_collection_abc import ObjectCollectionABC',
            ],
            'first-party-forward-reference': [],
            'type-checking': [],
        }

    def _gen_code_api_endpoint_property(self) -> str:
        """Return the method code.

        @property
        def _api_endpoint(self) -> str:
            '''Return the type specific API endpoint.'''
            return ApiEndpoints.ARTIFACTS.value
        """
        return '\n'.join(
            [
                f'''{self.i1}@property''',
                f'''{self.i1}def _api_endpoint(self) -> str:''',
                f'''{self.i2}"""Return the type specific API endpoint."""''',
                f'''{self.i2}return ApiEndpoints.{self.type_.upper()}.value''',
                '',
                '',
            ]
        )

    def _gen_code_container_init_method(self) -> str:
        """Return the method code.

        def __init__(self, **kwargs) -> None:
            '''Initialize Class properties.'''
            super().__init__(
                kwargs.pop('session', None),
                kwargs.pop('tql_filter', None),
                kwargs.pop('params', None)
            )
            self._model = ArtifactsModel(**kwargs)
        """
        # add method import requirement
        classes = [
            f'{self.type_.singular().pascal_case()}Model',
            f'{self.type_.plural().pascal_case()}Model',
        ]
        self.update_requirements(self.type_, f'{self.type_.singular()}_model', classes)

        return '\n'.join(
            [
                f'''{self.i1}def __init__(self, **kwargs) -> None:''',
                f'''{self.i2}"""Initialize class properties."""''',
                f'''{self.i2}super().__init__(''',
                (
                    f'''{self.i3}kwargs.pop('session', None), '''
                    f'''kwargs.pop('tql_filter', None), '''
                    f'''kwargs.pop('params', None)'''
                ),
                f'''{self.i2})''',
                f'''{self.i2}self._model = {self.type_.plural().pascal_case()}Model(**kwargs)''',
                f'''{self.i2}self.type_ = \'{self.type_.plural()}\'''',
                '',
                '',
            ]
        )

    def _gen_code_container_iter_method(self) -> str:
        """Return the method code.

        def __iter__(self) -> 'Artifact':
            '''Iterate over CM objects.'''
            return self.iterate(base_class=Artifact)
        """
        return '\n'.join(
            [
                f'''{self.i1}def __iter__(self) -> '{self.type_.singular().pascal_case()}':''',
                f'''{self.i2}"""Iterate over CM objects."""''',
                (
                    f'''{self.i2}return self.iterate(base_class='''
                    f'''{self.type_.singular().pascal_case()})'''
                ),
                '',
                '',
            ]
        )

    def _gen_code_container_filter_property(self) -> str:
        """Return the method code.

        @property
        def filter(self) -> 'ArtifactFilter':
            '''Return the type specific filter object.'''
            return ArtifactFilter(self._session, self.tql)
        """
        filter_class = f'{self.type_.singular().pascal_case()}Filter'
        self.update_requirements(self.type_, f'{self.type_.singular()}_filter', [filter_class])
        return '\n'.join(
            [
                f'''{self.i1}@property''',
                f'''{self.i1}def filter(self) -> '{filter_class}':''',
                f'''{self.i2}"""Return the type specific filter object."""''',
                f'''{self.i2}return {filter_class}(self.tql)''',
                '',
                '',
            ]
        )

    def _gen_code_deleted_method(self) -> str:
        """Return the method code.

        @property
        def filter(self) -> 'ArtifactFilter':
            '''Return the type specific filter object.'''
            return ArtifactFilter(self._session, self.tql)
        """
        self.requirements['first-party'].append({'module': 'datetime', 'imports': ['datetime']})
        self.requirements['standard library'].append({'module': 'typing', 'imports': ['Optional']})
        return '\n'.join(
            [
                f'''{self.i1}def deleted(''',
                f'''{self.i2}self,''',
                f'''{self.i2}deleted_since: Optional[Union[datetime, str]],''',
                f'''{self.i2}type_: Optional[str] = None,''',
                f'''{self.i2}owner: Optional[str] = None''',
                f'''{self.i1}) -> None:''',
                f'''{self.i2}"""Return deleted indicators.''',
                '',
                f'''{self.i2}This will not use the default params set on the "Indicators" ''',
                f'''{self.i2}object and instead used the params that are passed in.''',
                f'''{self.i2}"""''',
                '',
                f'''{self.i2}if deleted_since is not None:''',
                f'''{self.i3}deleted_since = str(''',
                (
                    f'''{self.i4}self.utils.any_to_datetime(deleted_since)'''
                    '''.strftime('%Y-%m-%dT%H:%M:%SZ')'''
                ),
                f'''{self.i3})''',
                '',
                f'''{self.i2}yield from self.iterate(''',
                f'''{self.i3}base_class=Indicator,''',
                f'''{self.i3}api_endpoint=f'{{self._api_endpoint}}/deleted',''',
                (
                    f'''{self.i3}params={{'deletedSince': deleted_since, '''
                    ''''owner': owner, 'type': type_}'''
                ),
                f'''{self.i2})''',
                '',
            ]
        )

    def _gen_code_group_methods(self) -> str:
        """Return the method code.

        @property
        def filter(self) -> 'ArtifactFilter':
            '''Return the type specific filter object.'''
            return ArtifactFilter(self._session, self.tql)
        """
        self.requirements['standard library'].append({'module': 'typing', 'imports': ['Optional']})
        self.requirements['type-checking'].append('''from requests import Response''')
        return '\n'.join(
            [
                f'''{self.i1}def download(self, params: Optional[dict] = None) -> bytes:''',
                f'''{self.i2}"""Return the document attachment for Document/Report Types."""''',
                f'''{self.i2}self._request(''',
                f'''{self.i3}method='GET',''',
                f'''{self.i3}url=f\'\'\'{{self.url('GET')}}/download\'\'\',''',
                f'''{self.i3}# headers={{'content-type': 'application/octet-stream'}},''',
                f'''{self.i3}headers=None,''',
                f'''{self.i3}params=params,''',
                f'''{self.i2})''',
                f'''{self.i2}return self.request.content''',
                '',
                f'''{self.i1}def pdf(self, params: Optional[dict] = None) -> bytes:''',
                f'''{self.i2}"""Return the document attachment for Document/Report Types."""''',
                f'''{self.i2}self._request(''',
                f'''{self.i3}method='GET',''',
                f'''{self.i3}body=None,''',
                f'''{self.i3}url=f\'\'\'{{self.url('GET')}}/pdf\'\'\',''',
                f'''{self.i3}headers=None,''',
                f'''{self.i3}params=params,''',
                f'''{self.i2})''',
                '',
                f'''{self.i2}return self.request.content''',
                '',
                (
                    f'''{self.i1}def upload(self, content: Union[bytes, str], '''
                    '''params: Optional[dict] = None) -> 'Response':'''
                ),
                f'''{self.i2}"""Return the document attachment for Document/Report Types."""''',
                f'''{self.i2}self._request(''',
                f'''{self.i3}method='POST',''',
                f'''{self.i3}url=f\'\'\'{{self.url('GET')}}/upload\'\'\',''',
                f'''{self.i3}body=content,''',
                f'''{self.i3}headers={{'content-type': 'application/octet-stream'}},''',
                f'''{self.i3}params=params,''',
                f'''{self.i2})''',
                f'''{self.i2}return self.request''',
                '',
                '',
            ]
        )

    def _gen_code_object_init_method(self) -> str:
        """Return the method code.

        def __init__(self, **kwargs) -> None:
            '''Initialize Class properties'''
            super().__init__(kwargs.pop('session', None))
            self._model = ArtifactModel(**kwargs)
        """
        # add method import requirement
        # classes = [f'{self.type_.singular().pascal_case()}Model']
        # self.update_requirements(self.type_, 'model', classes)

        # set nested type
        nested_field_name = self.utils.snake_string(self.type_).camel_case().plural()
        if self.type_ in ['indicators', 'groups']:
            nested_field_name = (
                self.utils.snake_string(f'associated_{self.type_}').camel_case().plural()
            )
        elif self.type_ in ['case_attributes', 'group_attributes', 'indicator_attributes']:
            nested_field_name = 'attributes'

        return '\n'.join(
            [
                f'''{self.i1}def __init__(self, **kwargs) -> None:''',
                f'''{self.i2}"""Initialize class properties."""''',
                f'''{self.i2}super().__init__(kwargs.pop('session', None))''',
                '',
                f'''{self.i2}# properties''',
                f'''{self.i2}self._model = {self.type_.singular().pascal_case()}Model(**kwargs)''',
                f'''{self.i2}self._nested_field_name = '{nested_field_name}' ''',
                f'''{self.i2}self._nested_filter = 'has_{self.type_.singular()}' ''',
                f'''{self.i2}self.type_ = \'{self.type_.singular().space_case()}\'''',
                '',
                '',
            ]
        )

    # def _gen_code_object_base_filter_method(self) -> str:
    #     """Return the method code.

    #     @property
    #     def _base_filter(self) -> dict:
    #         '''Return the default filter.'''
    #         return {
    #             'keyword': 'artifactid',
    #             'operator': TqlOperator.EQ,
    #             'value': self.model.id,
    #             'type_': 'integer',
    #         }
    #     """
    #     return '\n'.join(
    #         [
    #             f'''{self.i1}@property''',
    #             f'''{self.i1}def _base_filter(self) -> dict:''',
    #             f'''{self.i2}"""Return the default filter."""''',
    #             f'''{self.i2}return {{''',
    #             f'''{self.i3}'keyword': '{self.type_.singular()}_id',''',
    #             f'''{self.i3}'keyword': 'id',''',
    #             f'''{self.i3}'operator': TqlOperator.EQ,''',
    #             f'''{self.i3}'value': self.model.id,''',
    #             f'''{self.i3}'type_': 'integer',''',
    #             f'''{self.i2}}}''',
    #             '',
    #             '',
    #         ]
    #     )

    def _gen_code_object_as_entity_property_method(self) -> str:
        """Return the method code.

        @property
        def as_entity(self) -> dict:
            '''Return the entity representation of the object.'''
            case - name
            notes - summary
            tag - name
            task - name
            workflow_event - summary
            workflow_template_model - name

            return {'type': 'Artifact', 'id': self.model.id, 'value': self.model.summary}
        """
        name_entities = ['artifact_types', 'cases', 'tags', 'tasks', 'workflow_templates']
        value_type = 'summary'
        if self.type_.lower() in name_entities:
            value_type = 'name'

        return '\n'.join(
            [
                f'''{self.i1}@property''',
                f'''{self.i1}def as_entity(self) -> dict:''',
                f'''{self.i2}"""Return the entity representation of the object."""''',
                f'''{self.i2}type_ = self.type_''',
                f'''{self.i2}if hasattr(self.model, 'type'):''',
                f'''{self.i3}type_ = self.model.type''',
                '',
                (
                    f'''{self.i2}return {{'type': type_, 'id': '''
                    f'''self.model.id, 'value': self.model.{value_type}}}'''
                ),
                '',
                '',
            ]
        )

    def _gen_code_object_add_type_method(self, type_: str, model_type: Optional[str] = None) -> str:
        """Return the method code.

        def stage_artifact(self, **kwargs) -> None:
            '''Stage an Artifact on the object.

            ...
            '''
            self.model.artifacts.data.append(ArtifactModel(**kwargs))
        """
        type_ = self.utils.camel_string(type_)
        model_type = self.utils.camel_string(model_type or type_)
        model_reference = model_type

        # Unlike all of the other objects on the victims model, it references 'assets' not the
        # model name 'VictimAsset'
        # VictimAsset
        # object just Assets.
        if type_.lower() == 'victim_assets':
            model_reference = self.utils.camel_string('assets')


        # get model from map and update requirements
        model_import_data = self._module_import_data(type_)
        self.requirements['standard library'].append('''from typing import Union''')
        self.requirements['first-party'].append(
            f'''from {model_import_data.get('model_module')} '''
            f'''import {model_import_data.get('model_class')}'''
        )
        return '\n'.join(
            [
                (
                    f'''{self.i1}def stage_{model_type.singular()}(self, '''
                    f'''data: Union[dict, 'ObjectABC', '{model_import_data.get('model_class')}'''
                    f'''']) -> None:'''
                ),
                f'''{self.i2}"""Stage {type_.singular()} on the object."""''',
                f'''{self.i2}if isinstance(data, ObjectABC):''',
                f'''{self.i3}data = data.model''',
                f'''{self.i2}elif isinstance(data, dict):''',
                f'''{self.i3}data = {model_import_data.get('model_class')}(**data)''',
                '',
                f'''{self.i2}if not isinstance(data, {model_import_data.get('model_class')}):''',
                (
                    f'''{self.i3}raise RuntimeError('Invalid type '''
                    f'''passed in to stage_{model_type.singular()}')'''
                ),
                f'''{self.i2}self.model.{model_reference.plural()}.data.append(data)''' '',
                '',
            ]
        )

    def _gen_code_object_remove_method(self) -> str:
        """Return the method code."""
        self.requirements['standard library'].append('import json')
        self.requirements['standard library'].append({'module': 'typing', 'imports': ['Optional']})
        return '\n'.join(
            [
                f'''{self.i1}def remove(self, params: Optional[dict] = None) -> None:''',
                f'''{self.i2}"""Remove a nested object."""''',
                f'''{self.i2}method = \'PUT\'''',
                f'''{self.i2}unique_id = self._calculate_unique_id()''',
                '',
                f'''{self.i2}# validate an id is available''',
                f'''{self.i2}self._validate_id(unique_id.get('value'), '')''',
                '',
                f'''{self.i2}body = json.dumps(''',
                f'''{self.i3}{{''',
                f'''{self.i4}self._nested_field_name: {{''',
                f'''{self.i5}'data': [{{unique_id.get('filter'): unique_id.get('value')}}],''',
                f'''{self.i5}'mode': 'delete',''',
                f'''{self.i4}}}''',
                f'''{self.i3}}}''',
                f'''{self.i2})''',
                '',
                f'''{self.i2}# get the unique id value for id, xid, summary, etc ...''',
                f'''{self.i2}parent_api_endpoint = self._parent_data.get('api_endpoint')''',
                f'''{self.i2}parent_unique_id = self._parent_data.get('unique_id')''',
                f'''{self.i2}url = f\'{{parent_api_endpoint}}/{{parent_unique_id}}\'''',
                '',
                f'''{self.i2}# validate parent an id is available''',
                f'''{self.i2}self._validate_id(parent_unique_id, url)''',
                '',
                f'''{self.i2}self._request(''',
                f'''{self.i3}method=method,''',
                f'''{self.i3}url=url,''',
                f'''{self.i3}body=body,''',
                f'''{self.i3}headers={{'content-type': 'application/json'}},''',
                f'''{self.i3}params=params,''',
                f'''{self.i2})''',
                '',
                f'''{self.i2}return self.request''',
                '',
                '',
            ]
        )

    def _gen_code_object_type_property_method(
        self, type_: str, model_type: Optional[str] = None
    ) -> str:
        """Return the method code.

        @property
        def artifacts(self):
            '''Yield Artifact from Artifacts'''
            from tcex.api.tc.v3.artifacts.model import Artifact, Artifacts

            yield from self._iterate_over_sublist(Artifacts)
        """
        type_ = self.utils.camel_string(type_)
        model_type = self.utils.camel_string(model_type or type_)

        # get model from map and update requirements
        model_import_data = self._module_import_data(type_)

        # don't add import if class is in same file
        if self.type_ != type_:
            self.requirements['type-checking'].append(
                f'''from {model_import_data.get('object_module')} '''
                f'''import {model_import_data.get('object_class')}'''
            )
        _code = [
            f'''{self.i1}@property''',
            (
                f'''{self.i1}def {model_type.plural()}(self) ->'''
                f''' '{model_import_data.get('object_class')}':'''
            ),
            (
                f'''{self.i2}"""Yield {type_.singular().pascal_case()} '''
                f'''from {type_.plural().pascal_case()}."""'''
            ),
        ]

        if self.type_ != type_:
            _code.extend(
                [
                    (
                        f'''{self.i2}from {model_import_data.get('object_module')} '''
                        f'''import {model_import_data.get('object_collection_class')}'''
                    ),
                    '',
                ]
            )

        _code.extend(
            [
                (
                    f'''{self.i2}yield from self._iterate_over_sublist'''
                    f'''({model_import_data.get('object_collection_class')})'''
                ),
                '',
                '',
            ]
        )
        return '\n'.join(_code)

    def gen_container_class(self) -> str:
        """Generate the Container Model

        class Artifacts(ObjectCollectionABC):
            '''Artifacts Collection.

            # Example of params input
            {
                'result_limit': 100,  # Limit the retrieved results.
                'result_start': 10,  # Starting count used for pagination.
                'fields': ['caseId', 'summary']  # Select additional return fields.
            }

            Arg:
                session (Session): Session object configured with TC API Auth.
                tql_filters (list): List of TQL filters.
                params (dict): Additional query params (see example above).
            '''
        """
        return '\n'.join(
            [
                '',
                f'''class {self.type_.plural().pascal_case()}(ObjectCollectionABC):''',
                f'''{self.i1}"""{self.type_.plural().pascal_case()} Collection.''',
                '',
                f'''{self.i1}# Example of params input''',
                f'''{self.i1}{{''',
                f'''{self.i2}'result_limit': 100,  # Limit the retrieved results.''',
                f'''{self.i2}'result_start': 10,  # Starting count used for pagination.''',
                f'''{self.i2}'fields': ['caseId', 'summary']  # Select additional return fields.''',
                f'''{self.i1}}}''',
                '',
                f'''{self.i1}Args:''',
                f'''{self.i2}session (Session): Session object configured with TC API Auth.''',
                f'''{self.i2}tql_filters (list): List of TQL filters.''',
                f'''{self.i2}params (dict): Additional query params (see example above).''',
                f'{self.i1}"""',
                '',
                '',
            ]
        )

    def gen_container_methods(self) -> str:
        """Return the container methods.

        def __init__ ...

        def __iter__ ...

        def filter ...

        """
        _code = ''
        # generate __init__ method
        _code += self._gen_code_container_init_method()

        # generate __iter__ method
        _code += self._gen_code_container_iter_method()

        # generate api_endpoint property method
        _code += self._gen_code_api_endpoint_property()

        # generate filter property method
        _code += self._gen_code_container_filter_property()

        if self.type_.lower() == 'indicators':
            _code += self._gen_code_deleted_method()

        return _code

    def gen_doc_string(self) -> str:
        """Generate doc string."""
        return (
            f'"""{self.type_.singular().pascal_case()} '
            f'/ {self.type_.plural().pascal_case()} Object"""\n'
        )

    def gen_object_class(self) -> str:
        """Generate the Object Model

        class Artifact(ObjectABC):
            '''Case Management Artifact

            Arg:
                case_id (int, kwargs): The **case id** for the Artifact.
                case_xid (str, kwargs): The **case xid** for the Artifact.
                derived_link (bool, kwargs): Flag to specify if this artifact should be used for
                    potentially associated cases or not.
                ...
            '''
        """
        args = GenerateArgs(self.type_).gen_args()
        return '\n'.join(
            [
                '',
                f'''class {self.type_.singular().pascal_case()}(ObjectABC):''',
                f'''{self.i1}"""{self.type_.plural().pascal_case()} Object.''',
                '',
                f'{args}',
                f'{self.i1}"""',
                '',
                '',
            ]
        )

    def gen_object_methods(self) -> str:
        """Return the container methods.

        def __init__ ...

        def __iter__ ...

        def filter ...

        """
        _code = ''

        # generate __init__ method
        _code += self._gen_code_object_init_method()

        # generate api_endpoint property method
        _code += self._gen_code_api_endpoint_property()

        # generate base_filter property method
        # _code += self._gen_code_object_base_filter_method()

        # skip object that don't require as_entity method
        if self.type_ not in [
            'case_attributes',
            'victim_attributes',
            'group_attributes',
            'indicator_attributes',
            'security_labels',
            'tags',
            'attribute_types',
            'owner_roles',
            'owners',
            'system_roles',
            'user_groups',
            'users',
            'victim_assets',
        ]:
            # generate as_entity property method
            _code += self._gen_code_object_as_entity_property_method()

        # skip object that don't require as_entity method
        if self.type_ in [
            'groups',
            'indicators',
            'security_labels',
            'tags',
        ]:
            # generate as_entity property method
            _code += self._gen_code_object_remove_method()

        # generate group specific methods
        if self.type_.lower() == 'groups':
            _code += self._gen_code_group_methods()

        # get NON read-only properties of endpoint (OPTIONS: /v3/<object>)
        add_properties = []
        for field_name, field_data in self._type_properties.items():
            if isinstance(field_data.get('data'), dict):
                field_data['data'] = [field_data.get('data')]

            if field_data.get('data') is None:
                # normalize the data format
                field_data = {'data': [field_data]}

            if field_data.get('data')[0].get('readOnly', False) is False:
                add_properties.append(field_name)

        # properties of endpoint
        # properties = list(self._type_properties.keys())

        # generate artifacts property method
        if 'artifacts' in add_properties:
            _code += self._gen_code_object_type_property_method('artifacts')

        # generate add_associated_group method
        if 'associatedGroups' in add_properties:
            _code += self._gen_code_object_type_property_method('groups', 'associated_groups')

        # generate add_associated_indicator method
        if 'associatedIndicators' in add_properties:
            _code += self._gen_code_object_type_property_method(
                'indicators', 'associated_indicators'
            )

        # generate attributes property method
        if 'attributes' in add_properties:
            _code += self._gen_code_object_type_property_method('attributes')

        # generate cases add_property method
        if 'cases' in add_properties:
            _code += self._gen_code_object_type_property_method('cases')

        # generate notes property method
        if 'notes' in add_properties:
            _code += self._gen_code_object_type_property_method('notes')

        # generate security_labels property method
        if 'securityLabels' in add_properties:
            _code += self._gen_code_object_type_property_method('security_labels')

        # generate tags property method
        if 'tags' in add_properties:
            _code += self._gen_code_object_type_property_method('tags')

        # generate tasks property method
        if 'tasks' in add_properties:
            _code += self._gen_code_object_type_property_method('tasks')

        # Stage Method

        # generate add_artifact method
        if 'artifacts' in add_properties:
            _code += self._gen_code_object_add_type_method('artifacts')

        # generate add_asset method
        if 'assets' in add_properties:
            _code += self._gen_code_object_add_type_method('victim_assets')

        # generate add_associated_group method
        if 'associatedGroups' in add_properties:
            _code += self._gen_code_object_add_type_method('groups', 'associated_groups')

        # generate add_associated_indicator method
        if 'associatedIndicators' in add_properties and self.type_ != 'indicators':
            _code += self._gen_code_object_add_type_method('indicators', 'associated_indicators')

        # generate add_attribute method
        if 'attributes' in add_properties:
            _code += self._gen_code_object_add_type_method('attributes')

        # generate add_case method
        if 'cases' in add_properties:
            _code += self._gen_code_object_add_type_method('cases')

        # generate add_note method
        if 'notes' in add_properties:
            _code += self._gen_code_object_add_type_method('notes')

        # generate add_security_labels method
        if 'securityLabels' in add_properties:
            _code += self._gen_code_object_add_type_method('security_labels')

        # generate add_tag method
        if 'tags' in add_properties:
            _code += self._gen_code_object_add_type_method('tags')

        # generate add_task method
        if 'tasks' in add_properties:
            _code += self._gen_code_object_add_type_method('tasks')

        return _code

    def update_requirements(
        self, type_: str, filename: str, classes: List[str], from_: Optional[str] = 'first-party'
    ) -> Dict[str, str]:
        """Return the requirements code."""
        type_ = self.utils.camel_string(type_)
        classes = ', '.join(classes)
        self.requirements[from_].append(
            f'from {self.tap(type_)}.{type_.plural().snake_case()}.{filename} import {classes}'
        )