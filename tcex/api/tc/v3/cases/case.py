"""Case / Cases Object"""
# standard library
from typing import TYPE_CHECKING, Union

# first-party
from tcex.api.tc.v3.api_endpoints import ApiEndpoints
from tcex.api.tc.v3.artifacts.artifact_model import ArtifactModel
from tcex.api.tc.v3.case_attributes.case_attribute_model import CaseAttributeModel
from tcex.api.tc.v3.cases.case_filter import CaseFilter
from tcex.api.tc.v3.cases.case_model import CaseModel, CasesModel
from tcex.api.tc.v3.notes.note_model import NoteModel
from tcex.api.tc.v3.object_abc import ObjectABC
from tcex.api.tc.v3.object_collection_abc import ObjectCollectionABC
from tcex.api.tc.v3.tags.tag_model import TagModel
from tcex.api.tc.v3.tasks.task_model import TaskModel

if TYPE_CHECKING:  # pragma: no cover
    # first-party
    from tcex.api.tc.v3.artifacts.artifact import Artifact
    from tcex.api.tc.v3.case_attributes.case_attribute import CaseAttribute
    from tcex.api.tc.v3.notes.note import Note
    from tcex.api.tc.v3.tags.tag import Tag
    from tcex.api.tc.v3.tasks.task import Task


class Cases(ObjectCollectionABC):
    """Cases Collection.

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
        self._model = CasesModel(**kwargs)
        self.type_ = 'cases'

    def __iter__(self) -> 'Case':
        """Iterate over CM objects."""
        return self.iterate(base_class=Case)

    @property
    def _api_endpoint(self) -> str:
        """Return the type specific API endpoint."""
        return ApiEndpoints.CASES.value

    @property
    def filter(self) -> 'CaseFilter':
        """Return the type specific filter object."""
        return CaseFilter(self.tql)


class Case(ObjectABC):
    """Cases Object.

    Args:
        artifacts (Artifacts, kwargs): A list of Artifacts corresponding to the Case.
        assignee (Assignee, kwargs): The user or group Assignee object for the Case.
        attributes (CaseAttributes, kwargs): A list of Attributes corresponding to the Case.
        case_close_time (str, kwargs): The date and time that the Case was closed.
        case_detection_time (str, kwargs): The date and time that ends the user initiated Case
            duration.
        case_occurrence_time (str, kwargs): The date and time that starts the user initiated Case
            duration.
        case_open_time (str, kwargs): The date and time that the Case was first opened.
        description (str, kwargs): The description of the Case.
        name (str, kwargs): The name of the Case.
        notes (Notes, kwargs): A list of Notes corresponding to the Case.
        resolution (str, kwargs): The Case resolution.
        severity (str, kwargs): The Case severity.
        status (str, kwargs): The Case status.
        tags (Tags, kwargs): A list of Tags corresponding to the Case (NOTE: Setting this parameter
            will replace any existing tag(s) with the one(s) specified).
        tasks (Tasks, kwargs): A list of Tasks corresponding to the Case.
        user_access (Users, kwargs): A list of Users that, when defined, are the only ones allowed
            to view or edit the Case.
        workflow_events (WorkflowEvents, kwargs): A list of workflowEvents (timeline) corresponding
            to the Case.
        workflow_template (WorkflowTemplate, kwargs): The Template that the Case is populated by.
        xid (str, kwargs): The **xid** for the Case.
    """

    def __init__(self, **kwargs) -> None:
        """Initialize class properties."""
        super().__init__(kwargs.pop('session', None))

        # properties
        self._model = CaseModel(**kwargs)
        self._nested_field_name = 'cases'
        self._nested_filter = 'has_case'
        self.type_ = 'Case'

    @property
    def _api_endpoint(self) -> str:
        """Return the type specific API endpoint."""
        return ApiEndpoints.CASES.value

    @property
    def as_entity(self) -> dict:
        """Return the entity representation of the object."""
        type_ = self.type_
        if hasattr(self.model, 'type'):
            type_ = self.model.type

        return {'type': type_, 'id': self.model.id, 'value': self.model.name}

    @property
    def artifacts(self) -> 'Artifact':
        """Yield Artifact from Artifacts."""
        # first-party
        from tcex.api.tc.v3.artifacts.artifact import Artifacts

        yield from self._iterate_over_sublist(Artifacts)

    @property
    def attributes(self) -> 'CaseAttribute':
        """Yield Attribute from Attributes."""
        # first-party
        from tcex.api.tc.v3.case_attributes.case_attribute import CaseAttributes

        yield from self._iterate_over_sublist(CaseAttributes)

    @property
    def notes(self) -> 'Note':
        """Yield Note from Notes."""
        # first-party
        from tcex.api.tc.v3.notes.note import Notes

        yield from self._iterate_over_sublist(Notes)

    @property
    def tags(self) -> 'Tag':
        """Yield Tag from Tags."""
        # first-party
        from tcex.api.tc.v3.tags.tag import Tags

        yield from self._iterate_over_sublist(Tags)

    @property
    def tasks(self) -> 'Task':
        """Yield Task from Tasks."""
        # first-party
        from tcex.api.tc.v3.tasks.task import Tasks

        yield from self._iterate_over_sublist(Tasks)

    def stage_artifact(self, data: Union[dict, 'ObjectABC', 'ArtifactModel']) -> None:
        """Stage artifact on the object."""
        if isinstance(data, ObjectABC):
            data = data.model
        elif isinstance(data, dict):
            data = ArtifactModel(**data)

        if not isinstance(data, ArtifactModel):
            raise RuntimeError('Invalid type passed in to stage_artifact')
        self.model.artifacts.data.append(data)

    def stage_attribute(self, data: Union[dict, 'ObjectABC', 'CaseAttributeModel']) -> None:
        """Stage attribute on the object."""
        if isinstance(data, ObjectABC):
            data = data.model
        elif isinstance(data, dict):
            data = CaseAttributeModel(**data)

        if not isinstance(data, CaseAttributeModel):
            raise RuntimeError('Invalid type passed in to stage_attribute')
        self.model.attributes.data.append(data)

    def stage_note(self, data: Union[dict, 'ObjectABC', 'NoteModel']) -> None:
        """Stage note on the object."""
        if isinstance(data, ObjectABC):
            data = data.model
        elif isinstance(data, dict):
            data = NoteModel(**data)

        if not isinstance(data, NoteModel):
            raise RuntimeError('Invalid type passed in to stage_note')
        self.model.notes.data.append(data)

    def stage_tag(self, data: Union[dict, 'ObjectABC', 'TagModel']) -> None:
        """Stage tag on the object."""
        if isinstance(data, ObjectABC):
            data = data.model
        elif isinstance(data, dict):
            data = TagModel(**data)

        if not isinstance(data, TagModel):
            raise RuntimeError('Invalid type passed in to stage_tag')
        self.model.tags.data.append(data)

    def stage_task(self, data: Union[dict, 'ObjectABC', 'TaskModel']) -> None:
        """Stage task on the object."""
        if isinstance(data, ObjectABC):
            data = data.model
        elif isinstance(data, dict):
            data = TaskModel(**data)

        if not isinstance(data, TaskModel):
            raise RuntimeError('Invalid type passed in to stage_task')
        self.model.tasks.data.append(data)