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


class StartingTimeUnitType(str, Enum):
    Second = "Second"
    Minute = "Minute"
    Hour = "Hour"
    Day = "Day"
    Week = "Week"
    Month = "Month"
    Year = "Year"


class EndingTimeUnitType(str, Enum):
    Hours = "Hours"
    Minutes = "Minutes"
    Seconds = "Seconds"
    Days = "Days"
    Weeks = "Weeks"


class RunTimeOptions(BaseModel):
    model_config = ConfigDict(extra="ignore")

    isSpecificStartTime: bool
    specificStartingTime: datetime | None = None
    startTimeSelection: StartingTimeUnitType | None = None
    isSpecificEndTime: bool
    isInfinite: bool
    specificEndingTime: datetime | None = None
    isRunLength: bool
    endTimeSelection: EndingTimeUnitType | None = None
    endTimeRunValue: float

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


class TableColumnForeignKeySchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    toTableName: str = ""
    toColumnName: str = ""


class TableStateForeignKeySchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    toTableName: str = ""
    toColumnName: str = ""


class TablePropertyColumnSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str = ""
    displayName: str = ""
    isKey: bool | None = None
    foreignKeyInfo: list[TableColumnForeignKeySchema] | None = None


class TableStateColumnSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str = ""
    displayName: str = ""
    isKey: bool | None = None
    foreignKeyInfo: list[TableStateForeignKeySchema] | None = None


class TableTargetColumnSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str = ""
    displayName: str = ""


class TableColumnIncomingRelationSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    fromTableName: str = ""
    fromColumnName: str = ""


class TableStateIncomingRelationSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    fromTableName: str = ""
    fromStateName: str = ""


class SimioTableSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str = ""
    columnSchemas: list[TablePropertyColumnSchema] | None = None
    stateSchemas: list[TableStateColumnSchema] | None = None
    targetSchemas: list[TableTargetColumnSchema] | None = None
    columnIncomingRelationSchemas: list[TableColumnIncomingRelationSchema] | None = None
    stateIncomingRelationSchemas: list[TableStateIncomingRelationSchema] | None = None


class ExperimentRunStatus(str, Enum):
    Pending = "Pending"
    Running = "Running"
    Complete = "Complete"
    Cancelled = "Cancelled"
    Failed = "Failed"
    Faulted = "Faulted"
    NotStarted = "NotStarted"


class ExperimentConfidenceLevelType(Enum):
    Point90 = 0
    Point95 = 1
    Point98 = 2
    Point99 = 3
    NONE = 4


class UpperPercentile(str, Enum):
    Percent75 = "Percent75"
    Percent80 = "Percent80"
    Percent90 = "Percent90"
    Percent95 = "Percent95"
    Percent99 = "Percent99"


class LowerPercentile(str, Enum):
    Percent25 = "Percent25"
    Percent20 = "Percent20"
    Percent10 = "Percent10"
    Percent5 = "Percent5"
    Percent1 = "Percent1"


class RunType(str, Enum):
    Validate = "Validate"
    AnalyzeRisk = "AnalyzeRisk"
    RunPlan = "RunPlan"
    RunExperiment = "RunExperiment"


class ActiveRunStage(str, Enum):
    NoneStage = "None"
    LoadModel = "LoadModel"
    Import = "Import"
    Run = "Run"
    Export = "Export"
    Publish = "Publish"


class RunStageProgress(BaseModel):
    model_config = ConfigDict(extra="ignore")

    isSucceeded: bool | None = None
    total: int | None = None
    completed: int | None = None


class RunStatusAndTotals(BaseModel):
    model_config = ConfigDict(extra="ignore")

    isSucceeded: bool | None = None
    total: int | None = None
    completed: int | None = None


class ResourceUsageSnapshot(BaseModel):
    model_config = ConfigDict(extra="ignore")

    timestampInUTC: datetime
    creationTimestampInUTC: datetime
    systemMemorySize: float
    privateMemorySize: float
    virtualMemorySize: float
    workingSetSize: float
    numberOfCoresAvailable: int
    cpuTimeAvailable: float
    cpuTimeUsed: float


class ExperimentRunProgress(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int = 0
    name: str | None = None
    description: str | None = None
    status: ExperimentRunStatus = ExperimentRunStatus.NotStarted
    runType: RunType = RunType.Validate
    submissionTime: datetime
    creatorName: str | None = None
    activeStage: ActiveRunStage = ActiveRunStage.NoneStage
    loadModelSucceeded: bool | None = None
    importProgress: RunStageProgress | None = None
    runProgress: RunStatusAndTotals | None = None
    exportProgress: RunStageProgress | None = None
    publishSucceeded: bool | None = None
    usageSnapshot: ResourceUsageSnapshot | None = None


class ExperimentRunAdditionalRunStatus(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    scenarioNames: list[str] | None = None
    status: ExperimentRunStatus | None = None
    statusMessage: str | None = None
    warnings: str | None = None
    planRun: bool = False
    replicationRun: bool = False
    resultsOutOfDate: bool = False
    submissionTime: datetime
    planRunEndTime: datetime | None = None


class ExperimentRuns(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int = 0
    experimentId: int = 0
    name: str | None = None
    description: str | None = None
    status: ExperimentRunStatus | None = None
    submissionTime: datetime
    createdTime: datetime
    scenarioNames: list[str] | None = None
    totalReplications: int = 0
    completedReplications: int = 0
    statusMessage: str | None = None
    warningMessage: str | None = None
    modelId: int = 0
    creatorName: str | None = None
    projectId: int = 0
    projectName: str | None = None
    modelName: str | None = None
    modelRiskAnalysisConfidenceLevel: ExperimentConfidenceLevelType | None = None
    riskAnalysisConfidenceLevel: ExperimentConfidenceLevelType | None = None
    warmUpPeriodHours: float = 0.0
    upperPercentile: UpperPercentile | None = None
    lowerPercentile: LowerPercentile | None = None
    primaryResponse: str | None = None
    defaultReplicationsRequired: int = 0
    concurrentReplicationLimit: int | None = None
    startTime: datetime
    endTime: datetime | None = None
    planRun: bool = False
    replicationRun: bool = False
    additionalRunsStatus: list[ExperimentRunAdditionalRunStatus] | None = None
    timeOptions: RunTimeOptions | None = None
    isModelOwner: bool = False
    isModelUser: bool = False
    startUsingCurrentTimeZoneIdentifier: str | None = None


class TableImportExportStatus(str, Enum):
    Pending = "Pending"
    InProgress = "InProgress"
    Complete = "Complete"
    Failed = "Failed"


class ExperimentRunScenarioTableImportExportStatus(BaseModel):
    model_config = ConfigDict(extra="ignore")

    tableName: str
    status: TableImportExportStatus
    statusMessage: str | None = None


class ExperimentRunScenarioImportExportStatus(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    experimentRunId: int
    scenarioName: str
    tableNames: list[str]
    matchActiveBindingName: str | None = None
    submissionTime: datetime
    completionTime: datetime | None = None
    status: TableImportExportStatus
    statusMessage: str | None = None
    perTableStatus: list[ExperimentRunScenarioTableImportExportStatus] | None = None


class TableRowDataPropertyValue(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str
    value: str | None = None


class TableRowDataStateValue(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str
    value: Any | None = None


class TableRowDataTargetValue(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str
    planValue: Any | None = None
    planStatus: str | None = None
    planLowerBound: Any | None = None
    planUpperBound: Any | None = None
    riskExpectedValue: Any | None = None
    riskWithinBoundsProbability: float | None = None


class TableColumnType(str, Enum):
    Property = "Property"
    State = "State"
    PlanValue = "PlanValue"
    PlanStatus = "PlanStatus"
    PlanLowerBound = "PlanLowerBound"
    PlanUpperBound = "PlanUpperBound"
    RiskAverage = "RiskAverage"
    RiskProbability = "RiskProbability"


class TableRowDataError(BaseModel):
    model_config = ConfigDict(extra="ignore")

    columnType: TableColumnType
    columnName: str
    errorMessage: str


class TableRowData(BaseModel):
    model_config = ConfigDict(extra="ignore")

    rowIndex: int
    properties: list[TableRowDataPropertyValue] | None = None
    states: list[TableRowDataStateValue] | None = None
    targetValues: list[TableRowDataTargetValue] | None = None
    errors: list[TableRowDataError] | None = None


class Project(BaseModel):
    model_config = ConfigDict(extra="ignore")

    projectId: int | None = None
    projectName: str | None = None
    modelId: list[int] | None = None


class ExperimentRunScenarioControlValueDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    value: str | None = None


class ExperimentRunScenarioResponseValueDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    value: float = 0.0
    description: str | None = None
    displayName: str | None = None
    lowerBound: float | None = None
    upperBound: float | None = None
    objective: int | None = None
    average: float = 0.0
    minimum: float = 0.0
    maximum: float = 0.0
    halfWidth: float = 0.0
    averageConfidenceIntervalStart: float = 0.0
    averageConfidenceIntervalEnd: float = 0.0
    lowerPercentile: float = 0.0
    median: float = 0.0
    upperPercentile: float = 0.0
    lowerPercentileConfidenceIntervalStart: float = 0.0
    lowerPercentileConfidenceIntervalEnd: float = 0.0
    upperPercentileConfidenceIntervalStart: float = 0.0
    upperPercentileConfidenceIntervalEnd: float = 0.0
    observations: list[float] | None = None


class ExperimentRunScenarioCurrentDataConnectorConfigurationDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    dataConnectorName: str | None = None
    currentConfigurationName: str | None = None


class ExperimentRunActiveTableBindingDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    tableName: str | None = None
    activeBindingName: str | None = None
    lastTableImport: datetime | None = None


class ExperimentRunScenarioResponseDataComputedResults(BaseModel):
    model_config = ConfigDict(extra="ignore")

    scenarioName: str | None = None
    replicationsCompleted: int = 0
    replicationsRequired: int = 0
    controlValues: list[ExperimentRunScenarioControlValueDTO] | None = None
    responseValues: list[ExperimentRunScenarioResponseValueDTO] | None = None
    connectorConfigurations: list[ExperimentRunScenarioCurrentDataConnectorConfigurationDTO] | None = None
    activeTableBindings: list[ExperimentRunActiveTableBindingDTO] | None = None


class LogPropertyNameAndDataFormatStringDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    type: list[str] | None = None


class LogSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    logName: str | None = None
    logProperties: list[LogPropertyNameAndDataFormatStringDTO] | None = None


class LogSchemaDetails(BaseModel):
    model_config = ConfigDict(extra="ignore")

    scenarioName: str | None = None
    experimentRunId: int
    logSchema: list[LogSchema] | None = None


class ResourceUsageRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    resourceId: str | None = None
    resourceName: str | None = None
    resourceList: str | None = None
    nodeList: str | None = None
    ownerId: str | None = None
    ownerName: str | None = None
    taskId: int | None = None
    entityName: str | None = None
    startTime: datetime | None = None
    endTime: datetime | None = None
    duration: float | None = None
    startTimeOffset: float | None = None
    endTimeOffset: float | None = None
    averageUnitsOwned: float | None = None
    minimumUnitsOwned: float | None = None
    maximumUnitsOwned: float | None = None


class ResourceStateRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    resourceId: str | None = None
    resourceName: str | None = None
    stateName: str | None = None
    autoStateName: str | None = None
    startTime: datetime | None = None
    displayableEndTime: datetime | None = None
    duration: float | None = None
    startTimeOffset: float | None = None
    endTimeOffset: float | None = None


class ResourceCapacityRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    resourceId: str | None = None
    resourceName: str | None = None
    capacityScheduled: float | None = None
    capacityAllocated: float | None = None
    capacityUtilized: float | None = None
    startTime: datetime | None = None
    displayableEndTime: datetime | None = None
    duration: float | None = None
    startTimeOffset: float | None = None
    endTimeOffset: float | None = None


class TransporterUsageRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    transporterId: str | None = None
    transporterName: str | None = None
    resourceName: str | None = None
    riderId: str | None = None
    riderName: str | None = None
    taskId: int | None = None
    entityName: str | None = None
    fromNodeName: str | None = None
    toNodeName: str | None = None
    startTimeDisplay: datetime | None = None
    startRideTimeDisplay: datetime | None = None
    endRideTimeDisplay: datetime | None = None
    endTimeDisplay: datetime | None = None
    duration: float | None = None
    startTimeOffset: float | None = None
    startRideTimeOffset: float | None = None
    endRideTimeOffset: float | None = None
    endTimeOffset: float | None = None


class ConstraintRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    constrainedEntityId: str | None = None
    entityName: str | None = None
    taskId: int | None = None
    facilityLocationName: str | None = None
    stationName: str | None = None
    constraintTypeString: str | None = None
    constraintItemId: str | None = None
    constraintItem: str | None = None
    constraintDescription: str | None = None
    startTimeDisplay: datetime | None = None
    endTimeDisplay: datetime | None = None
    duration: float | None = None
    startTimeOffset: float | None = None
    endTimeOffset: float | None = None


class MaterialUsageRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    time: datetime | None = None
    materialName: str | None = None
    lotId: str | None = None
    entityId: str | None = None
    entityName: str | None = None
    siteId: str | None = None
    siteName: str | None = None
    taskId: int | None = None
    bomGroupName: str | None = None
    bomName: str | None = None
    componentId: str | None = None
    quantity: float | None = None
    stockLevel: float | None = None
    lotStockLevel: float | None = None
    timeOffset: float | None = None


class InventoryReviewRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    time: datetime | None = None
    materialName: str | None = None
    siteId: str | None = None
    siteName: str | None = None
    quantityInStock: float | None = None
    quantityOnOrder: float | None = None
    quantityBackordered: float | None = None
    quantityReserved: float | None = None
    inventoryPosition: float | None = None
    qualifiedSpikeDemand: float | None = None
    netFlowPosition: float | None = None
    redZoneSize: float | None = None
    yellowZoneSize: float | None = None
    greenZoneSize: float | None = None
    recommendedOrderQuantity: float | None = None
    timeOffset: float | None = None


class StateObservationRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    startTime: datetime | None = None
    displayableEndTime: datetime | None = None
    duration: float | None = None
    objectType: str | None = None
    objectName: str | None = None
    dataSource: str | None = None
    category: str | None = None
    dataItem: str | None = None
    displayCategory: str | None = None
    startTimeOffset: float | None = None
    endTimeOffset: float | None = None
    time: datetime | None = None
    timeOffset: float | None = None
    value: float | None = None
    units: str | None = None
    rate: float | None = None
    rateUnits: str | None = None
    acceleration: float | None = None
    accelerationUnits: str | None = None
    stringValue: str | None = None


class TallyObservationRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    time: datetime | None = None
    objectType: str | None = None
    objectName: str | None = None
    dataSource: str | None = None
    category: str | None = None
    dataItem: str | None = None
    timeOffset: float | None = None
    value: float | None = None
    units: str | None = None


class TaskRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    taskId: int | None = None
    entityId: str | None = None
    entityName: str | None = None
    facilityLocationId: str | None = None
    facilityLocationName: str | None = None
    stationName: str | None = None
    taskSequenceName: str | None = None
    taskName: str | None = None
    startTime: datetime | None = None
    displayableEndTime: datetime | None = None
    duration: float | None = None
    startTimeOffset: float | None = None
    endTimeOffset: float | None = None


class TaskStateRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    taskId: int | None = None
    stateName: str | None = None
    entityId: str | None = None
    entityName: str | None = None
    startTime: datetime | None = None
    displayableEndTime: datetime | None = None
    duration: float | None = None
    startTimeOffset: float | None = None
    endTimeOffset: float | None = None


class ResourceInfoRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    resourceId: str | None = None
    resourceName: str | None = None
    displayCategory: str | None = None


class PeriodicOutputStatisticRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    timePeriod: str | None = None
    startTime: datetime | None = None
    displayableEndTime: datetime | None = None
    duration: float | None = None
    startTimeOffset: float | None = None
    endTimeOffset: float | None = None
    objectType: str | None = None
    objectName: str | None = None
    dataSource: str | None = None
    category: str | None = None
    dataItem: str | None = None
    startValue: float | None = None
    endValue: float | None = None
    valueChange: float | None = None
    units: str | None = None


class PeriodicStateStatisticRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    timePeriod: str | None = None
    startTime: datetime | None = None
    displayableEndTime: datetime | None = None
    duration: float | None = None
    startTimeOffset: float | None = None
    endTimeOffset: float | None = None
    objectType: str | None = None
    objectName: str | None = None
    dataSource: str | None = None
    category: str | None = None
    dataItem: str | None = None
    startValue: float | None = None
    endValue: float | None = None
    valueChange: float | None = None
    average: float | None = None
    minimum: float | None = None
    maximum: float | None = None
    units: str | None = None


class PeriodicTallyStatisticRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    timePeriod: str | None = None
    startTime: datetime | None = None
    endTime: datetime | None = None
    displayableEndTime: datetime | None = None
    duration: float | None = None
    startTimeOffset: float | None = None
    endTimeOffset: float | None = None
    objectType: str | None = None
    objectName: str | None = None
    dataSource: str | None = None
    category: str | None = None
    dataItem: str | None = None
    observations: int | None = None
    average: float | None = None
    minimum: float | None = None
    maximum: float | None = None
    units: str | None = None


class RunsInProgressStatistics(BaseModel):
    model_config = ConfigDict(extra="ignore")

    plansPending: int = 0
    plansRunning: int = 0
    experimentRunsPending: int = 0
    experimentRunsRunning: int = 0

```



## License
This project is licensed under the Apache License.
