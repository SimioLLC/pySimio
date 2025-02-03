from datetime import datetime, timezone
from dataclasses import dataclass, asdict, fields
from typing import Optional
import json

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
    endTimeRunValue: Optional[int] = None
    specificStartingTime: Optional[str] = None
    startTimeSelection: Optional[str] = None
    specificEndingTime: Optional[str] = None
    endTimeSelection: Optional[str] = None
    isSpecificStartTime: Optional[bool] = None
    isSpecificEndTime: Optional[bool] = None
    isInfinite: Optional[bool] = None
    isRunLength: Optional[bool] = None

@dataclass
class SimioExperiment(SimioDataClass):
    id: int
    name: Optional[str] = None
    modelId: Optional[int] = None
    modelName: Optional[str] = None
    projectName: Optional[str] = None
    hasExperimentRuns: Optional[bool] = None
    hasPlanRuns: Optional[bool] = None

@dataclass
class SimioModel(SimioDataClass):
    id: int
    name: Optional[str] = None
    projectId: Optional[int] = None
    projectName: Optional[str] = None
    projectOwner: Optional[str] = None
    projectUploadDateTime: Optional[str] = None
    projectSavedDate: Optional[str] = None
    projectSavedInVersion: Optional[str] = None
