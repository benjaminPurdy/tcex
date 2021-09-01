"""Artifact Model"""
# standard library
from datetime import datetime
from typing import Optional, List

# third-party
from pydantic import BaseModel, Extra, Field, validator

# first-party
from tcex.utils import Utils


class ArtifactsModel(
    BaseModel,
    title='Artifacts Model',
    alias_generator=Utils().snake_to_camel,
    validate_assignment=True,
):
    """Artifacts Model"""

    data: 'Optional[List[ArtifactModel]]' = Field(
        [],
        description='The data for the Artifact.',
        methods=['POST', 'PUT'],
        title='data',
    )


class ArtifactData(
    BaseModel,
    title='Artifact Data',
    alias_generator=Utils().snake_to_camel,
    validate_assignment=True
):
    """Artifact Data"""

    data: 'Optional[ArtifactModel]' = Field(
        None,
        description='The data for the Artifact.',
        methods=['POST', 'PUT'],
        title='data',
    )


class ArtifactModel(
    BaseModel,
    title='Artifact Model',
    alias_generator=Utils().snake_to_camel,
    extra=Extra.allow,
    validate_assignment=True
):
    """Artifact Model"""

    analytics_priority: Optional[str] = Field(
        None,
        allow_mutation=False,
        description='The **analytics priority** for the Artifact.',
        read_only=True,
        title='analyticsPriority',
    )
    analytics_priority_level: Optional[int] = Field(
        None,
        allow_mutation=False,
        description='The **analytics priority level** for the Artifact.',
        read_only=True,
        title='analyticsPriorityLevel',
    )
    analytics_score: Optional[int] = Field(
        None,
        allow_mutation=False,
        description='The **analytics score** for the Artifact.',
        read_only=True,
        title='analyticsScore',
    )
    analytics_status: Optional[str] = Field(
        None,
        allow_mutation=False,
        description='The **analytics status** for the Artifact.',
        read_only=True,
        title='analyticsStatus',
    )
    analytics_type: Optional[str] = Field(
        None,
        allow_mutation=False,
        description='The **analytics type** for the Artifact.',
        read_only=True,
        title='analyticsType',
    )
    artifact_type: 'Optional[ArtifactTypeModel]' = Field(
        None,
        allow_mutation=False,
        description='The **artifact type** for the Artifact.',
        read_only=True,
        title='artifactType',
    )
    case_id: Optional[int] = Field(
        None,
        description='The **case id** for the Artifact.',
        methods=['POST'],
        read_only=False,
        required_alt_field='caseXid',
        title='caseId',
        updatable=False,
    )
    case_xid: Optional[str] = Field(
        None,
        description='The **case xid** for the Artifact.',
        methods=['POST'],
        read_only=False,
        required_alt_field='caseId',
        title='caseXid',
        updatable=False,
    )
    date_added: Optional[datetime] = Field(
        None,
        allow_mutation=False,
        description='The **date added** for the Artifact.',
        read_only=True,
        title='dateAdded',
    )
    derived_link: bool = Field(
        None,
        description=(
            'Flag to specify if this artifact should be used for potentially associated cases or '
            'not.'
        ),
        methods=['POST', 'PUT'],
        read_only=False,
        title='derivedLink',
    )
    field_name: Optional[str] = Field(
        None,
        description='The field name for the artifact.',
        methods=['POST', 'PUT'],
        max_length=100,
        min_length=0,
        read_only=False,
        title='fieldName',
    )
    file_data: Optional[str] = Field(
        None,
        description='Base64 encoded file attachment required only for certain artifact types.',
        methods=['POST', 'PUT'],
        read_only=False,
        title='fileData',
    )
    hash_code: Optional[str] = Field(
        None,
        description='Hashcode of Artifact of type File.',
        methods=['POST'],
        read_only=False,
        title='hashCode',
        updatable=False,
    )
    id: Optional[int] = Field(
        None,
        description='The id of the **Object**.',
        read_only=True,
        title='id',
    )
    intel_type: Optional[str] = Field(
        None,
        allow_mutation=False,
        description='The **intel type** for the Artifact.',
        read_only=True,
        title='intelType',
    )
    links: Optional[dict] = Field(
        None,
        allow_mutation=False,
        description='The **links** for the Artifact.',
        read_only=True,
        title='links',
    )
    notes: 'Optional[NotesModel]' = Field(
        None,
        description='A list of Notes corresponding to the Artifact.',
        methods=['POST', 'PUT'],
        max_size=1000,
        read_only=False,
        title='notes',
    )
    parent_case: 'Optional[CaseModel]' = Field(
        None,
        allow_mutation=False,
        description='The **parent case** for the Artifact.',
        read_only=True,
        title='parentCase',
    )
    source: Optional[str] = Field(
        None,
        description='The **source** for the Artifact.',
        methods=['POST', 'PUT'],
        max_length=100,
        min_length=0,
        read_only=False,
        title='source',
    )
    summary: Optional[str] = Field(
        None,
        description='The **summary** for the Artifact.',
        methods=['POST', 'PUT'],
        max_length=500,
        min_length=1,
        read_only=False,
        title='summary',
    )
    task: 'Optional[TaskModel]' = Field(
        None,
        allow_mutation=False,
        description='The **task** for the Artifact.',
        read_only=True,
        title='task',
    )
    task_id: Optional[int] = Field(
        None,
        description='The ID of the task which the Artifact references.',
        methods=['POST'],
        read_only=False,
        title='taskId',
        updatable=False,
    )
    task_xid: Optional[str] = Field(
        None,
        description='The XID of the task which the Artifact references.',
        methods=['POST'],
        read_only=False,
        title='taskXid',
        updatable=False,
    )
    type: Optional[str] = Field(
        None,
        description='The **type** for the Artifact.',
        methods=['POST'],
        read_only=False,
        title='type',
        updatable=False,
    )

    @validator('artifact_type', always=True)
    def _validate_artifact_type(cls, v):
        if not v:
            return ArtifactTypeModel()
        return v

    @validator('parent_case', always=True)
    def _validate_parent_case(cls, v):
        if not v:
            return CaseModel()
        return v

    @validator('notes', always=True)
    def _validate_notes(cls, v):
        if not v:
            return NotesModel()
        return v

    @validator('task', always=True)
    def _validate_task(cls, v):
        if not v:
            return TaskModel()
        return v


# first-party
from tcex.case_management.models.artifact_type_model import ArtifactTypeModel
from tcex.case_management.models.case_model import CaseModel
from tcex.case_management.models.note_model import NotesModel
from tcex.case_management.models.task_model import TaskModel


# add forward references
ArtifactData.update_forward_refs()
ArtifactModel.update_forward_refs()
ArtifactsModel.update_forward_refs()