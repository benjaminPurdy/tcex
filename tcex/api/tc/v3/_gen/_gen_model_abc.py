"""Generate Models for ThreatConnect API"""
# standard library
import sys
from abc import ABC
from textwrap import TextWrapper
from typing import Dict

# first-party
from tcex.api.tc.v3._gen._gen_abc import GenerateABC


class GenerateModelABC(GenerateABC, ABC):
    """Generate Models for Case Management Types"""

    def __init__(self, type_: str) -> None:
        """Initialize class properties."""
        super().__init__(type_)

        # properties
        self.json_encoder = {'datetime': 'lambda v: v.isoformat()'}
        self.requirements = {
            'standard library': [{'module': 'typing', 'imports': ['List', 'Optional']}],
            'third-party': [
                {'module': 'pydantic', 'imports': ['BaseModel', 'Extra', 'Field']},
            ],
            'first-party': [
                {'module': 'tcex.utils', 'imports': ['Utils']},
                {'module': 'datetime', 'imports': ['datetime']},
            ],
            'first-party-forward-reference': [],
        }
        self.validators = {}

    def _add_pydantic_validator(self):
        """Add pydantic validator only when required."""
        for lib in self.requirements['third-party']:
            if isinstance(lib, dict):
                if lib.get('module') == 'pydantic':
                    lib['imports'].append('validator')

    def _configure_type(self, type_: str, field: str) -> str:
        """Return hint type."""
        _types = self._prop_type_common()
        _types.update(self._prop_type_custom(type_, field))

        # handle types
        type_ = self._fix_type(type_)  # swap Attribute for specific type (e.g., CaseAttribute)
        type_data = _types.get(type_, {})
        requirement_data = type_data.get('requirement')

        # add additional requirements, if not current model type
        if requirement_data is not None and not type_ == self.type_.plural().pascal_case():
            from_ = requirement_data.get('from')
            import_ = requirement_data.get('import')
            if import_ not in self.requirements.get(from_):
                self.requirements[from_].append(import_)

        # add validator
        self.validators[type_] = type_data.get('validator')

        return type_data.get('type', type_)

    def _fix_type(self, type_: str) -> str:
        """Fix type for when API returns a "bad" type."""
        if self.type_ == 'cases' and type_ == 'Attributes':
            return 'CaseAttributes'
        if self.type_ == 'groups' and type_ == 'Attributes':
            return 'GroupAttributes'
        if self.type_ == 'indicators' and type_ == 'Attributes':
            return 'IndicatorAttributes'
        if type_ == 'AttributeDatas':
            return 'Attributes'
        return type_

    def _gen_req_code(self, type_: str) -> Dict[str, str]:
        """Return the requirements code"""
        type_ = self.utils.camel_string(type_)
        return {
            'from': 'first-party-forward-reference',
            'import': (
                f'from {self.tap(type_)}.{type_.plural().snake_case()}.'
                f'{type_.singular().snake_case()}_model import {type_}Model'
            ),
        }

    def _gen_code_validator_method(self, type_: str, field: str) -> str:
        """Return the validator code

        @validator('artifact_type', always=True)
        def _validate_artifact_type(cls, v):
            if not v:
                return ArtifactTypeModel()
            return v
        """
        return '\n'.join(
            [
                f'''{self.i1}@validator('{field}', always=True)''',
                f'''{self.i1}def _validate_{field}(cls, v):''',
                f'''{self.i2}if not v:''',
                f'''{self.i3}return {type_}Model()''',
                f'''{self.i2}return v''',
                '',
            ]
        )

    @staticmethod
    def _prop_type_common() -> dict:
        """Return common types."""
        return {
            'boolean': {
                'type': 'bool',
            },
            'BigDecimal': {
                'type': 'Optional[int]',
            },
            'Boolean': {
                'type': 'bool',
            },
            'Date': {
                'requirement': {
                    'from': 'standard library',
                    'import': 'from datetime import datetime',
                },
                'type': 'Optional[datetime]',
            },
            'Double': {
                'type': 'Optional[float]',
            },
            'Integer': {
                'type': 'Optional[int]',
            },
            'JsonNode': {
                'type': 'Optional[dict]',
            },
            'Links': {
                'type': 'Optional[dict]',
            },
            'Long': {
                'type': 'Optional[int]',
            },
            'Short': {
                'type': 'Optional[int]',
            },
            'String': {
                'type': 'Optional[str]',
            },
        }

    def _prop_type_custom(self, type_: str, field: str) -> dict:
        """Return cm types."""
        type_ = self._fix_type(self.utils.snake_string(type_))
        return {
            'AdversaryAssets': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'Artifact': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'Artifacts': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'ArtifactType': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'Assignee': {
                'requirement': {
                    'from': 'first-party-forward-reference',
                    'import': (
                        'from tcex.api.tc.v3.security.assignee import AssigneeModel'
                        '  # pylint: disable=unused-import'
                    ),
                },
                'type': 'Optional[\'AssigneeModel\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'Attributes': {
                'requirement': {
                    'from': 'first-party-forward-reference',
                    'import': (
                        'from tcex.api.tc.v3.attributes.attribute_model import AttributesModel'
                    ),
                },
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'Case': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'CaseAttributes': {
                'requirement': {
                    'from': 'first-party-forward-reference',
                    'import': (
                        'from tcex.api.tc.v3.case_attributes.case_attribute_model '
                        'import CaseAttributesModel'
                    ),
                },
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'Cases': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'FileAction': {
                'requirement': {
                    'from': 'first-party-forward-reference',
                    'import': (
                        'from tcex.api.tc.v3.indicators.file_action_model import FileActionModel'
                    ),
                },
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'FileOccurrences': {
                'requirement': {
                    'from': 'first-party-forward-reference',
                    'import': (
                        'from tcex.api.tc.v3.indicators.file_occurrences_model '
                        'import FileOccurrencesModel'
                    ),
                },
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'GroupAttributes': {
                'requirement': {
                    'from': 'first-party-forward-reference',
                    'import': (
                        'from tcex.api.tc.v3.group_attributes.group_attribute_model '
                        'import GroupAttributesModel'
                    ),
                },
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'Groups': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'IndicatorAttributes': {
                'requirement': {
                    'from': 'first-party-forward-reference',
                    'import': (
                        'from tcex.api.tc.v3.indicator_attributes.indicator_attribute_model '
                        'import IndicatorAttributesModel'
                    ),
                },
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'Indicators': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'Note': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'Notes': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'SecurityLabels': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'Tag': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'Tags': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'Task': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            # TODO: [high] validate this is correct
            'TaskAssignees': {
                'requirement': {
                    'from': 'first-party-forward-reference',
                    'import': 'from tcex.api.tc.v3.security.assignee import AssigneeModel',
                },
                'type': 'Optional[\'AssigneeModel\']',
            },
            'Tasks': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'User': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'Users': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'Victims': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'VictimAssets': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'VictimAttributes': {
                'requirement': {
                    'from': 'first-party-forward-reference',
                    'import': (
                        'from tcex.api.tc.v3.victim_attributes.victim_attribute_model '
                        'import VictimAttributesModel'
                    ),
                },
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'WorkflowEvent': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'WorkflowEvents': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
            'WorkflowTemplate': {
                'requirement': self._gen_req_code(type_),
                'type': f'Optional[\'{type_}Model\']',
                'validator': self._gen_code_validator_method(type_, field),
            },
        }

    def _format_description(self, description: str, length: int) -> str:
        """Format description for field."""
        # fix descriptions coming from core API endpoint
        if description[-1] not in ('.', '?', '!'):
            description += '.'

        # fix core descriptions that are not capitalized.
        description_words = description.split(' ')
        description = f'{description_words[0].title()} ' + ' '.join(description_words[1:])

        # there are 23 characters used on the line (indent -> key -> quote -> comma)
        other_used_space = 22  # space used by indent -> single quote -> key -> comma
        if len(description) < length - other_used_space:
            return f'\'{description}\''

        _description = ['(']
        _description.extend(
            [
                f'{line}\''
                for line in TextWrapper(
                    break_long_words=False,
                    drop_whitespace=False,
                    expand_tabs=True,
                    initial_indent=' ' * 12 + '\'',
                    subsequent_indent=' ' * 12 + '\'',
                    tabsize=15,
                    width=length - 1,
                ).wrap(description)
            ]
        )
        _description.append(f'{self.i2})')
        return '\n'.join(_description)

    def gen_doc_string(self) -> str:
        """Generate doc string."""
        return (
            f'"""{self.type_.singular().title()} / {self.type_.plural().title()} Model"""\n'
            '# pylint: disable=no-member,no-self-argument,no-self-use,wrong-import-position\n'
        )

    def gen_container_class(self) -> str:
        """Generate the Container Model

        class ArtifactsModel(
            BaseModel,
            title='Artifacts Model',
            alias_generator=Utils().snake_to_camel,
            validate_assignment=True,
        ):
        """
        return '\n'.join(
            [
                '',
                f'''class {self.type_.plural().pascal_case()}Model(''',
                f'''{self.i1}BaseModel,''',
                f'''{self.i1}title='{self.type_.plural().pascal_case()} Model',''',
                f'''{self.i1}alias_generator=Utils().snake_to_camel,''',
                f'''{self.i1}validate_assignment=True,''',
                '''):''',
                f'''{self.i1}"""{self.type_.plural().title()} Model"""''',
                '',
                '',
            ]
        )

    def gen_container_fields(self) -> str:
        """Generate the Container Model fields

        data: Optional[List['ArtifactModel']] = Field(
            [],
            description='The data of the Cases.',
            methods=['POST', 'PUT'],
            title='data',
        )
        """
        return '\n'.join(
            [
                (
                    f'''{self.i1}data: '''
                    f'''Optional[List['{self.type_.singular().pascal_case()}Model']] '''
                    '''= Field('''
                ),
                f'''{self.i2}[],''',
                (
                    f'''{self.i2}description='The data for the '''
                    f'''{self.type_.plural().pascal_case()}.','''
                ),
                f'''{self.i2}methods=['POST', 'PUT'],''',
                f'''{self.i2}title='data',''',
                f'''{self.i1})''',
                '',
                '',
            ]
        )

    def gen_data_class(self) -> str:
        """Generate the Data Class

        class ArtifactDataModel(
            BaseModel,
            title='Artifact Data',
            alias_generator=Utils().snake_to_camel,
            validate_assignment=True,
        ):
        """
        return '\n'.join(
            [
                '',
                f'''class {self.type_.singular().pascal_case()}DataModel(''',
                f'''{self.i1}BaseModel,''',
                f'''{self.i1}title='{self.type_.singular().pascal_case()} Data Model',''',
                f'''{self.i1}alias_generator=Utils().snake_to_camel,''',
                f'''{self.i1}validate_assignment=True,''',
                '''):''',
                f'''{self.i1}"""{self.type_.plural().title()} Data Model"""''',
                '',
                '',
            ]
        )

    def gen_data_fields(self) -> str:
        """Generate the Data Model fields

        data: 'Optional[ArtifactModel]' = Field(
            None,
            description='The data of the Artifact.',
            title='data',
        )
        """
        return '\n'.join(
            [
                (
                    f'''{self.i1}data: '''
                    f'''Optional[List['{self.type_.singular().pascal_case()}Model']] '''
                    '''= Field('''
                ),
                f'''{self.i2}[],''',
                (
                    f'''{self.i2}description='The data for the '''
                    f'''{self.type_.plural().pascal_case()}.','''
                ),
                f'''{self.i2}methods=['POST', 'PUT'],''',
                f'''{self.i2}title='data',''',
                f'''{self.i1})''',
                '',
                '',
            ]
        )

    def gen_model_class(self) -> str:
        """Generate the model class

        class ArtifactModel(
            BaseModel,
            title='Artifact Model',
            alias_generator=Utils().snake_to_camel,
            validate_assignment=True,
            json_encoders=json_encoders,
        ):
        """
        return '\n'.join(
            [
                '',
                f'''class {self.type_.singular().pascal_case()}Model(''',
                f'''{self.i1}BaseModel,''',
                f'''{self.i1}alias_generator=Utils().snake_to_camel,''',
                f'''{self.i1}extra=Extra.allow,''',
                f'''{self.i1}title='{self.type_.singular().pascal_case()} Model',''',
                f'''{self.i1}validate_assignment=True,''',
                f'''{self.i1}json_encoders=json_encoders,''',
                '''):''',
                f'''{self.i1}"""{self.type_.singular().title()} Model"""''',
                '',
                f'''{self.i1}# slot attributes are not added to dict()/json()''',
                f'''{self.i1}__slot__ = ('_privates_',)''',
                '',
                f'''{self.i1}def __init__(self, **kwargs):''',
                f'''{self.i2}"""Initialize class properties."""''',
                f'''{self.i2}super().__init__(**kwargs)''',
                f'''{self.i2}super().__setattr__('_privates_', {{'_modified_': 0}})''',
                '',
                f'''{self.i1}def __setattr__(self, name, value):''',
                f'''{self.i2}"""Update modified property on any update."""''',
                (
                    f'''{self.i2}super().__setattr__('_privates_', '''
                    f'''{{'_modified_': self.privates.get('_modified_', 0) + 1}})'''
                ),
                f'''{self.i2}super().__setattr__(name, value)''',
                '',
                f'''{self.i1}@property''',
                f'''{self.i1}def modified(self):''',
                f'''{self.i2}"""Return int value of modified (> 0 means modified)."""''',
                f'''{self.i2}return self._privates_.get('_modified_', 0)''',
                '',
                f'''{self.i1}@property''',
                f'''{self.i1}def privates(self):''',
                f'''{self.i2}"""Return privates dict."""''',
                f'''{self.i2}return self._privates_''',
                '',
                '',
            ]
        )

    def gen_model_fields(self) -> str:
        """Generate the Model

        Example field_data:
        "analyticsPriority": {
            "readOnly": true,
            "type": "String"
        }

        Example Field:
        analytics_priority: Optional[str] = Field(
            None,
            allow_mutation=False,
            description='The **analytics priority** for the Artifact.',
            read_only=True,
            title='analyticsPriority',
        )
        """
        _model = []
        for field_name, field_data in sorted(self._type_properties.items()):
            field_name = self.utils.camel_string(field_name)
            field_alias = None  # only required when field matches a python reserved word
            field_type = field_data.get('type')  # the defined field type

            # fix python reserved words
            if field_name in ['from']:
                field_alias = field_name
                field_name = self.utils.camel_string(f'{field_name}_')

            if field_data.get('data') is not None:
                try:
                    if isinstance(field_data.get('data'), list):
                        field_data = field_data.get('data', [])[0]
                    elif isinstance(field_data.get('data'), dict):
                        # for attributes on groups, this should go away after update to
                        # new attribute format in the future
                        field_data = field_data.get('data')
                except IndexError:
                    print(field_name, field_data)
                    sys.exit(1)

                try:
                    field_type = self.utils.inflect.plural(field_data.get('type'))
                    # field_type = self._fix_type(
                    #     self.utils.inflect.plural(field_data.get('type'))
                    # )  # change field type to plural
                except TypeError:
                    print(field_name, field_type, field_data)
                    sys.exit(1)

            # get the hint type and set requirements
            field_hint_type = self._configure_type(field_type, field_name.snake_case())

            # property to model fields
            field_description = self._format_description(
                field_data.get(
                    'description',
                    (
                        f'The **{field_name.space_case().lower()}** '
                        f'for the {self.type_.singular().title()}.'
                    ),
                ).replace('\'', '\\\''),
                100,
            )

            field_applies_to = field_data.get('appliesTo')
            field_conditional_required = field_data.get('conditionalRequired')
            field_max_length = field_data.get('maxLength')
            field_min_length = field_data.get('minLength')
            # field_max_size = field_data.get('maxSize')
            field_max_value = field_data.get('maxValue')
            field_min_value = field_data.get('minValue')
            field_methods = []
            field_read_only = field_data.get('readOnly', False)
            field_required_alt_field = field_data.get('requiredAltField')
            field_updatable = field_data.get('updatable')

            # method rules
            if field_read_only is False:
                field_methods.append('POST')
                if field_updatable not in [False]:
                    field_methods.append('PUT')
            if (
                    self.type_.lower() == 'workflow_events' and
                    field_name.snake_case() == 'deleted_reason'
            ):
                field_methods = ['DELETE']

            # update model
            _model.append(f'''{self.i1}{field_name.snake_case()}: {field_hint_type} = Field(''')
            _model.append(f'''{self.i2}None,''')  # the default value

            # allow_mutation / readOnly
            if field_read_only is True and field_name != 'id':
                _model.append(f'''{self.i2}allow_mutation=False,''')  # readOnly/mutation setting

            # alias
            if field_alias is not None:
                _model.append(f'''{self.i2}alias='{field_alias}',''')

            # applies_to
            if field_applies_to is not None:
                _model.append(f'''{self.i2}applies_to={field_applies_to},''')

            # applies_to
            if field_conditional_required is not None:
                _model.append(f'''{self.i2}conditional_required={field_conditional_required},''')

            # description
            if field_description is not None:
                _model.append(f'''{self.i2}description={field_description},''')

            # methods (HTTP)
            if field_methods:
                _model.append(f'''{self.i2}methods={field_methods},''')

            # max_length
            if field_max_length is not None:
                _model.append(f'''{self.i2}max_length={field_max_length},''')

            # max_size
            # if field_max_size is not None:
            #     _model.append(f'''{self.i2}max_items={field_max_size},''')

            # max_value
            if field_max_value is not None:
                _model.append(f'''{self.i2}maximum={field_max_value},''')

            # min_length
            if field_min_length is not None:
                _model.append(f'''{self.i2}min_length={field_min_length},''')

            # min_value
            if field_min_value is not None:
                _model.append(f'''{self.i2}minimum={field_min_value},''')

            # readOnly/allow_mutation setting
            _model.append(f'''{self.i2}read_only={field_read_only},''')

            # required-alt-field
            if field_required_alt_field is not None:
                _model.append(f'''{self.i2}required_alt_field='{field_required_alt_field}',''')

            # title
            _model.append(f'''{self.i2}title='{field_name}',''')

            # updatable
            if field_updatable is not None:
                _model.append(f'''{self.i2}updatable={field_updatable},''')

            _model.append(f'''{self.i1})''')
        _model.append('')

        return '\n'.join(_model)

    def gen_requirements_first_party_forward_reference(self):
        """Generate first-party forward reference, imported at the botton of the file."""
        _libs = []
        for from_, libs in self.requirements.items():
            if from_ not in ['first-party-forward-reference']:
                continue

            if libs:
                _libs.append('')  # add newline
                _libs.append('')  # add newline
                _libs.append('# first-party')
                for lib in sorted(libs):
                    _libs.append(lib)
        return '\n'.join(_libs)

    def gen_forward_reference(self):
        """Generate first-party forward reference, imported at the botton of the file."""
        return '\n'.join(
            [
                '',
                '',
                '# add forward references',
                f'{self.type_.singular().pascal_case()}DataModel.update_forward_refs()',
                f'{self.type_.singular().pascal_case()}Model.update_forward_refs()',
                f'{self.type_.plural().pascal_case()}Model.update_forward_refs()',
                '',
            ]
        )

    def gen_validator_methods(self) -> str:
        """Generate model validator."""
        _v = []

        validators = dict(
            sorted({k: v for k, v in self.validators.items() if v is not None}.items())
        )
        for validator in validators.values():
            _v.append(validator)

        # add blank line above validators only if validators exists
        if _v:
            _v.insert(0, '')
            self._add_pydantic_validator()

        return '\n'.join(_v)
