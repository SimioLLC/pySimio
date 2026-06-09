from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from typing import Any
from enum import Enum
from pydantic import BaseModel, ConfigDict

@dataclass
class SimioDataClass:
    def as_json(self, include_null: bool = False) -> dict:
        return asdict(
                self,
                dict_factory=lambda fields: {
                    key: value
                    for (key, value) in fields
                    if value is not None or include_null
                },
            )
    
    @classmethod
    def from_json(cls, data: dict):

        return cls(**data)  # Create an instance of the dataclass

class SimioScenario():
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', "DefaultScenario")
        self.replications_required = kwargs.get('replications_required', 0)
        self.control_values = kwargs.get('control_values', [
            {
                "name": "string",
                "value": "string"
            }
        ])
        self.connector_configurations = kwargs.get('connector_configurations', [
            {
                "dataConnectorName": "string",
                "currentConfigurationName": "string"
            }
        ])
        self.active_table_bindings = kwargs.get('active_table_bindings', [
            {
                "tableName": "string",
                "activeBindingName": "string",
                "lastTableImport": datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')
            }
        ])
    
    def get_scenario(self):
        return {
                    "name": self.name,
                    "replicationsRequired": self.replications_required,
                    "controlValues": self.control_values,
                    "connectorConfigurations": self.connector_configurations,
                    "activeTableBindings": self.active_table_bindings
                }

class SimioExperimentRun():
    class CreateInfo:        
        def __init__(self, **kwargs):
            self.scenarios = kwargs.get('scenarios', [SimioScenario()])

            self.external_inputs = kwargs.get('external_inputs', [
                {
                    "inputId": 0,
                    "inputFileId": 0
                }
            ])
            self.risk_analysis_confidence_level = kwargs.get('risk_analysis_confidence_level', "Point90")
            self.warm_up_period_hours = kwargs.get('warm_up_period_hours', 0)
            self.upper_percentile = kwargs.get('upper_percentile', "Percent75")
            self.lower_percentile = kwargs.get('lower_percentile', "Percent1")
            self.primary_response = kwargs.get('primary_response', 'string')
            self.default_replications_required = kwargs.get('default_replications_required', 0)
            self.concurrent_replication_limit = kwargs.get('concurrent_replication_limit', 0)
            self.start_end_time = kwargs.get('start_end_time', {
                "isSpecificStartTime": True,
                "specificStartingTime": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                "startTimeSelection": "Second",
                "isSpecificEndTime": True,
                "isInfinite": True,
                "specificEndingTime": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                "isRunLength": True,
                "endTimeSelection": "Hours",
                "endTimeRunValue": 0
            })
        
        def get_info(self):
            return {
                "scenarios": self.scenarios,
                "externalInputs": self.external_inputs,
                "riskAnalysisConfidenceLevel": self.risk_analysis_confidence_level,
                "warmUpPeriodHours": self.warm_up_period_hours,
                "upperPercentile": self.upper_percentile,
                "lowerPercentile": self.lower_percentile,
                "primaryResponse": self.primary_response,
                "defaultReplicationsRequired": self.default_replications_required,
                "concurrentReplicationLimit": self.concurrent_replication_limit,
                "startEndTime": self.start_end_time
            }
        
    def __init__(self, **kwargs):
        self.experiment_id = kwargs.get('experiment_id', 0)
        self.description = kwargs.get('description', 'string')
        self.name = kwargs.get('name', 'string')
        self.existing_experiment_run_id = kwargs.get('existing_experiment_run_id', 0)
        self.run_plan = kwargs.get('run_plan', True)
        self.run_replications = kwargs.get('run_replications', True)
        self.allow_export_at_end_of_replication = kwargs.get('allow_export_at_end_of_replication', True)
        
        self.create_info = self.CreateInfo(**(kwargs.get('create_info', {})))
        
    def update(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(f"{key} is not a valid property of SimioExperimentRun")
    
    def get_data(self):
        return {
            "experimentId": self.experiment_id,
            "description": self.description,
            "name": self.name,
            "existingExperimentRunId": self.existing_experiment_run_id,
            "runPlan": self.run_plan,
            "runReplications": self.run_replications,
            "allowExportAtEndOfReplication": self.allow_export_at_end_of_replication,
            "createInfo": self.create_info.get_info()  # Retrieve info from the nested CreateInfo class
        }

@dataclass
class TimeOptions(SimioDataClass):
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

    # def as_json(self, include_null: bool = False) -> dict:
    #     return self.model_dump(exclude_none=not include_null)

    # @classmethod
    # def from_json(cls, data: dict):
    #     if data is None:
    #         return None
    #     return cls.model_validate(data)


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