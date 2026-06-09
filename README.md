# pysimio

## Description
pySimio is the official Python Library wrapper for the Simio Portal REST API.

## Installation
```sh
pip install pysimio
```

## Usage
```python
import pysimio

# Example usage
```python
from pysimio import pySimio, SimioModel
import os

simio_portal_url = "https://simio.portal"
personal_access_token = os.getenv("PERSONAL_ACCESS_TOKEN")

api = pySimio(simio_portal_url)
api.authenticate(personalAccessToken=personal_access_token)

models = api.getModels()
if isinstance(models, list) and models:
    first: SimioModel = models[0]
    print(first.id, first.name)
```

## Available Methods
### Additional documentation and usage examples are coming soon.

* status: Return the current heartbeat status from the Simio Portal instance. Returns `bool`.
* reauthenticate: Reauthenticate to the API using the PAT provided during authentication. Returns `bool | None`.
* authenticate: Authenticate to the API using a PAT or SAML Assertion.
* getModels: Return models, optionally filtered by project, ownership, and published state. Returns `list[SimioModel]`.
* getModel: Return a single model by model id. Returns `SimioModel`.
* getModelTable: Return model table schema metadata. Returns `list[SimioTableSchema]`.
* getExperiments: Return all current Simio Portal experiments for a model. Returns `list[SimioExperiment]`.
* getExperiment: Return a specific experiment by id. Returns `SimioExperiment`.
* publishPlan: Publish a specific Simio Plan within Simio Portal. Returns `bool`.
* uploadAndPublishPlan: Upload a Simio Model, and publish the plan within Simio Portal. Returns `str`.
* getRuns: Return runs with optional filters (experiment id, name, model id). Returns `list[ExperimentRuns]`.
* getRun: Returns a specific Simio Portal run. Returns `ExperimentRuns`.
* getRunProgress: Return stage and progress details for a run. Returns `ExperimentRunProgress`.
* deleteRun: Delete a specific Simio Run within Simio Portal. Returns `bool`.
* cancelRun: Cancel a specific Simio Run within Simio Portal. Returns `bool`.
* setRunTimeOptions: Set the Time Options on a specific Simio Portal Run. Returns `bool`.
* cancelPlan: Cancel a specific Simio Plan within Simio Portal. Returns `bool`.
* createRun: Creates a new Simio Run within Simio Portal. Returns `int`.
* startRun: Create and start a new Simio Experiment run within Simio Portal. To update control parameters, you would add them to the "scenarios" section in the JSON and run it again. Returns `int`.
* createRunFromExisting: Create a new instances of a Simio Run within Simio Portal from an existing Simio Run. Returns `int`.
* startRunFromExisting: Start a new run of a Simio Run from an existing Simio Run. Returns `int`.
* getExport: Return export status of a Simio Export from Simio Portal. Returns `ExperimentRunScenarioImportExportStatus`.
* getImport: Return import status of a Simio Import from Simio Portal. Returns `ExperimentRunScenarioImportExportStatus`.
* getTableData: Return table rows for a run scenario table, with optional paging, filter, and columns. Returns `list[TableRowData]`.
* deleteModel: Delete a Simio Model from Simio Portal. Returns `bool`.
* deleteProject: Delete a Simio Project from Simio Portal. Returns `bool`.
* uploadProject: Upload a new Simio Project file to Simio Portal. Returns `str`.
* getProjects: Return list of existing Simio Projects from Simio Portal. Returns `list[Project]`.
* getProject: Return a specific Simio Project from Simio Portal. Returns `Project`.
* setControlValues: Update Control Values. Returns `bool`.
* setScenarioName: Update Scenario Name in a Simio Run within Simio Portal. Returns `bool`.
* modifyDataConnectorConfiguration: Update connector configuration state for a run. Returns `bool`.
* getScenarios: Return Simio Portal Scenario from a specified run. Returns `list[ExperimentRunScenarioResponseDataComputedResults]`.
* getScenariosLogSchemas: Return available scenario log schemas. Returns `list[LogSchemaDetails]`.
* getScenariosResourceUsageLogData: Return resource usage log rows. Returns `list[ResourceUsageRecord]`.
* getScenariosResourceStateLogData: Return resource state log rows. Returns `list[ResourceStateRecord]`.
* getScenariosResourceCapacityLogData: Return resource capacity log rows. Returns `list[ResourceCapacityRecord]`.
* getScenariosTransporterUsageLogData: Return transporter usage log rows. Returns `list[TransporterUsageRecord]`.
* getScenariosConstraintLogData: Return constraint log rows. Returns `list[ConstraintRecord]`.
* getScenariosMaterialUsageLogData: Return material usage log rows. Returns `list[MaterialUsageRecord]`.
* getScenariosInventoryReviewLogData: Return inventory review log rows. Returns `list[InventoryReviewRecord]`.
* getScenariosStateObservationLogData: Return state observation log rows. Returns `list[StateObservationRecord]`.
* getScenariosTallyObservationLogData: Return tally observation log rows. Returns `list[TallyObservationRecord]`.
* getScenariosTaskLogData: Return task log rows. Returns `list[TaskRecord]`.
* getScenariosTaskStateLogData: Return task state log rows. Returns `list[TaskStateRecord]`.
* getScenariosResourceInformationLogData: Return resource information log rows. Returns `list[ResourceInfoRecord]`.
* getScenariosPeriodicOutputStatisticLogData: Return periodic output statistic rows. Returns `list[PeriodicOutputStatisticRecord]`.
* getScenariosPeriodicStateStatisticLogData: Return periodic state statistic rows. Returns `list[PeriodicStateStatisticRecord]`.
* getScenariosPeriodicTallyStatisticLogData: Return periodic tally statistic rows. Returns `list[PeriodicTallyStatisticRecord]`.
* getTotalRunsInProgress: Return aggregate counts of plans and experiment runs that are pending/running. Returns `list[RunsInProgressStatistics]`.

## Classes
```python
@dataclass
class TimeOptions:
    runId: int
    endTimeRunValue: int | None = None
    specificStartingTime: str | None = None
    startTimeSelection: str | None = None
    specificEndingTime: str | None = None
    endTimeSelection: str | None = None
    isSpecificStartTime: bool | None = None
    isSpecificEndTime: bool | None = None
    isInfinite: bool | None = None
    isRunLength: bool | None = None


class SimioExperiment(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    name: str | None = None
    modelId: int | None = None
    modelName: str | None = None
    projectName: str | None = None
    hasExperimentRuns: bool | None = None
    hasPlanRuns: bool | None = None

class SimioModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    name: str | None = None
    projectId: int | None = None
    projectName: str | None = None
    projectOwner: str | None = None
    projectUploadDateTime: str | None = None
    projectSavedDate: str | None = None
    projectSavedInVersion: str | None = None

```



## License
This project is licensed under the Apache License.
