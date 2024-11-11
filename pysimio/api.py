import requests
from http_exceptions import HTTPException, UnauthorizedException
from tenacity import retry, retry_if_exception_type, stop_after_attempt
from pysimio.exceptions import AuthenticationError
from pysimio.classes import SimioExperimentRun
from pysimio.logger import logger

class pySimio():
    def __init__(self, 
                 baseURL: str
                ):
        self.apiURL = f"{baseURL}/api"
        self.authToken = None
        self.headers = {
            "accept": "application/json",
            "Authorization": ""
            }
        self.personalAccessToken = None
        self.logger = logger
           
    def status(self):
        """
        Return the current heartbeat status from the Simio Portal Instance

        Returns:
            bool: The status of the Server. (True is Up, False is Down)
        """        
        apiStatus = requests.get(f"{self.apiURL}/v1/heartbeat", headers=self.headers)
        if apiStatus.status_code == 204:
            return True
        else:
            return False
    
    def reauthenticate(self):
        """Attempts to reauthenticate to the API using the PAT provided during authentication

        Raises:
            AuthenticationError: Indicates that reauthentication failed

        Returns:
            bool: Returns True if reauthentication request was successful
        """        
        try:
            if self.personalAccessToken is not None:
                self.authenticate(self.personalAccessToken)
                return True
            else:
                raise AuthenticationError
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")
    
    def authenticate(self, 
                     personalAccessToken: str
                    ):
        try:
            self.personalAccessToken = personalAccessToken
            authBody = {
                "personalAccessToken": personalAccessToken
            }
            authenticationRequest = requests.post(f"{self.apiURL}/auth", json=authBody)
            if authenticationRequest.status_code == 200:
                authenticationRequest = authenticationRequest.json()
                if authenticationRequest["token"]:
                    self.authToken = authenticationRequest["token"]
                    self.headers['Authorization'] = f"Bearer {self.authToken}"
                else:
                    raise AuthenticationError
            else:
                raise HTTPException.from_status_code(status_code=authenticationRequest.status_code)(message=authenticationRequest.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")
            
    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def getModels(self, 
                  project_id: int = None, 
                  owned_models: bool = False, 
                  include_published: bool = False
                ):
        """Returns a json list of all current models

        Args:
            project_id (int, optional): _description_. Defaults to None.
            owned_models (bool, optional): _description_. Defaults to False.
            include_published (bool, optional): _description_. Defaults to False.

        Raises:
            HTTPException.from_status_code: _description_

        Returns:
            _type_: _description_
        """        
        try:
            params = []
            if project_id is not None:
                params.append(('project_id', project_id))
            if owned_models:
                params.append(('owned_models', owned_models))
            if include_published:
                params.append(('include_published', include_published))
            modelsRequest = requests.get(f"{self.apiURL}/v1/models", params=params, headers=self.headers)
            if modelsRequest.status_code == 200:
                return modelsRequest.json()
            elif modelsRequest.status_code == 204:
                return {}
            else:
                raise HTTPException.from_status_code(status_code=modelsRequest.status_code)(message=modelsRequest.text)
        except Exception:
            pass

    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def getModel(self, 
                 model_id: int
                ):
        try:
            modelRequest = requests.get(f"{self.apiURL}/v1/models/{model_id}", headers=self.headers)
            if modelRequest.status_code == 200:
                return modelRequest.json()
            else:
                raise HTTPException.from_status_code(status_code=modelRequest.status_code)(message=modelRequest.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")

    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def getModelTable(self, 
                      model_id: int, 
                      table_name: str = None
                    ):
        try:
            params = []
            if table_name is not None:
                params.append(("table_name", table_name))
            modelTableRequest = requests.get(f"{self.apiURL}/v1/models/{model_id}/table-schemas", headers=self.headers, params=params)
            if modelTableRequest.status_code == 200:
                return modelTableRequest.json()
            else:
                raise HTTPException.from_status_code(status_code=modelTableRequest.status_code)(message=modelTableRequest.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")

    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def getExperiments(self, 
                       model_id: int = None, 
                       include_published: bool = False
                    ):
        try:
            params = []
            if model_id is not None:
                params.append(('model_id', model_id))
            if include_published:
                params.append(('include_published', include_published))
            experimentsRequest = requests.get(f"{self.apiURL}/v1/experiments", params=params, headers=self.headers)
            if experimentsRequest.status_code == 200:
                return experimentsRequest.json()
            elif experimentsRequest.status_code == 204:
                return {}
            else:
                raise HTTPException.from_status_code(status_code=experimentsRequest.status_code)(message=experimentsRequest.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")
    
    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def getExperiment(self, 
                      experiment_id: int
                    ):
        try:
            experimentRequest = requests.get(f"{self.apiURL}/v1/experiments/{experiment_id}", headers=self.headers)
            if experimentRequest.status_code == 200:
                return experimentRequest.json()
            else:
                raise HTTPException.from_status_code(status_code=experimentRequest.status_code)(message=experimentRequest.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")

    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def publishPlan(self, 
                    publishName: str, 
                    publishDescription: str, 
                    experimentRunId: int, 
                    scenarioName: str
                ):
        try:
            requestBody = {
                "publishName": publishName,
                "publishDescription": publishDescription,
                "experimentRunId": experimentRunId,
                "scenarioName": scenarioName
            }
            publishRequest = requests.post(f"{self.apiURL}/v1/published-plans/publish-plan", headers=self.headers, json=requestBody)
            if publishRequest.status_code == 201:
                return True
            else:
                raise HTTPException.from_status_code(status_code=publishRequest.status_code)(message=publishRequest.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")

    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def uploadAndPublishPlan(self, 
                             publishName: str, 
                             publishDescription: str, 
                             modelToPublish: str, 
                             modelFile: str
                            ):
        try:
            body = {
                "PublishName": publishName,
                "PublishDescription": publishDescription,
                "ModelToPublish": modelToPublish
            }
            request = requests.post(f"{self.apiURL}/v1/published-plans/upload-and-publish-plan", headers=self.headers, json=body, files={'file': open(modelFile, 'rb')})
            if request.status_code == 201:
                return request.text
            else:
               raise HTTPException.from_status_code(status_code=request.status_code)(message=request.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")

    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def publishRun(self, 
                   experimentRunId: int, 
                   publishName: str, 
                   publishDescription: str
                ):
        try:
            body = {
                "experimentRunId": experimentRunId,
                "publishName": publishName,
                "publishDescription": publishDescription
            }
            request = requests.post(f"{self.apiURL}/v1/published-runs", headers=self.headers, json=body)
            if request.status_code == 201:
                return request.text
            else:
                raise HTTPException.from_status_code(status_code=request.status_code)(message=request.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")
    
    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def deletePublishedRun(self, 
                           publishedName: str
                        ):
        try:
            request = requests.delete(f"{self.apiURL}/v1/published-runs/{publishedName}", headers=self.headers)
            if request.status_code == 204:
                return True
            else:
                raise HTTPException.from_status_code(status_code=request.status_code)(message=request.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")

    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def getRuns(self, 
                experimentId: int = None
            ):
        try:
            params = []
            if experimentId is not None:
                params.append(('experiment_id', experimentId))
            request = requests.get(f"{self.apiURL}/v1/runs", headers=self.headers, params=params)
            if request.status_code == 200:
                return request.json()
            else:
                raise HTTPException.from_status_code(status_code=request.status_code)(message=request.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")

    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def getRun(self, 
                runId: int = None
            ):
        try:
            params = []
            if runId is not None:
                params.append(('run_id', runId))
            request = requests.get(f"{self.apiURL}/v1/runs/{runId}", headers=self.headers, params=params)
            if request.status_code == 200:
                return request.json()
            else:
                raise HTTPException.from_status_code(status_code=request.status_code)(message=request.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")

    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def deleteRun(self, 
                  runId: int
                ):
        try:
            request = requests.delete(f"{self.apiURL}/v1/runs/{runId}", headers=self.headers)
            if request.status_code == 204:
                return True
            else:
                raise HTTPException.from_status_code(status_code=request.status_code)(message=request.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")

    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def cancelRun(self, 
                  runId: int
                ):
        try:
            body = {
                "status": "cancelled"
            }
            request = requests.patch(f"{self.apiURL}/v1/runs/{runId}", headers=self.headers, json=body)
            if request.status_code == 204:
                return True
            else:
                raise HTTPException.from_status_code(status_code=request.status_code)(message=request.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")
    
    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def setRunTimeOptions(self, 
                          runId: int, 
                          specificStartingTime: str, 
                          startTimeSelection: str, 
                          specificEndingTime: str, 
                          endTimeSelection: str, endTimeRunValue: int, 
                          isSpecificStartTime: bool = True, 
                          isSpecificEndTime: bool = False, 
                          isInfinite: bool = True, 
                          isRunLength: bool=True
                        ):
        try:
            body = {
                "isSpecificStartTime": isSpecificStartTime,
                "specificStartingTime": specificStartingTime,
                "startTimeSelection": startTimeSelection,
                "isSpecificEndTime": isSpecificEndTime,
                "isInfinite": isInfinite,
                "specificEndingTime": specificEndingTime,
                "isRunLength": isRunLength,
                "endTimeSelection": endTimeSelection,
                "endTimeRunValue": endTimeRunValue
            }
            request = requests.put(f"{self.apiURL}/v1/runs/{runId}/time-options", headers=self.headers, json=body)
            if request.status_code == 204:
                return True
            else:
                raise HTTPException.from_status_code(status_code=request.status_code)(message=request.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")
    
    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def cancelPlan(self, 
                   runId: int, 
                   additionalRunId: int
                ):
        try:
            body = {
                "status": "cancelled"
            }
            request = requests.patch(f"{self.apiURL}/v1/runs/{runId}/additional-runs/{additionalRunId}", headers=self.headers, json=body)
            if request.status_code == 204:
                return True
            else:
                raise HTTPException.from_status_code(status_code=request.status_code)(message=request.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")
    
    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def createRun(self, 
                  modelId: int, 
                  experimentRunName: str
                ):
        try:
            body = {
                "modelId": modelId,
                "experimentRunName": experimentRunName
            }
            request = requests.post(f"{self.apiURL}/v1/runs/create", headers=self.headers, json=body)
            if request.status_code == 201:
                return request.json()
            else:
                raise HTTPException.from_status_code(status_code=request.status_code)(message=request.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")

    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def startRun(self, 
                 experimentRunData: SimioExperimentRun
                ):
        try:
            body = experimentRunData.get_data()
            request = requests.post(f"{self.apiURL}/v1/runs/start-experiment-run", headers=self.headers, json=body)
            if request.status_code == 201:
                return request.json()
            else:
                raise HTTPException.from_status_code(status_code=request.status_code)(message=request.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")
    
    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def createRunFromExisting(self, 
                              modelId: int, 
                              experimentRunName: str, 
                              sourceExperimentRunId: int, 
                              sourceExperimentRunScenarioName: str
                            ):
        try:
            body = {
                "modelId": modelId,
                "experimentRunName": experimentRunName,
                "sourceExperimentRunId": sourceExperimentRunId,
                "sourceExperimentRunScenarioName": sourceExperimentRunScenarioName
            }
            request = requests.post(f"{self.apiURL}/v1/runs/create-from-existing", headers=self.headers, json=body)
            if request.status_code == 201:
                return request.json()
            else:
                raise HTTPException.from_status_code(status_code=request.status_code)(message=request.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")
    
    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def startRunFromExisting(self, 
                             existingExperimentRunId: int, 
                             runPlan: bool = True, 
                             runReplications: bool = True
                            ):
        try:
            body = {
                "existingExperimentRunId": existingExperimentRunId,
                "runPlan": runPlan,
                "runReplications": runReplications
            }
            request = requests.post(f"{self.apiURL}/v1/runs/start-existing-plan-run", headers=self.headers, json=body)
            if request.status_code == 201:
                return request.json()
            else:
                raise HTTPException.from_status_code(status_code=request.status_code)(message=request.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")
            
    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def getExport(self, 
                  runId: int, 
                  exportId: int
                  ):
        try:
            params = []
            if runId is not None:
                params.append(('run_id', runId))
            if exportId is not None:
                params.append(('export_id', exportId))
            request = requests.get(f"{self.apiURL}/v1/runs/{runId}/scenarios/exports/{exportId}", headers=self.headers, params=params)
            if request.status_code == 200:
                return request.json()
            else:
                raise HTTPException.from_status_code(status_code=request.status_code)(message=request.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")
            
    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def getImport(self, 
                  runId: int, 
                  importId: int
                  ):
        try:
            params = []
            if runId is not None:
                params.append(('run_id', runId))
            if importId is not None:
                params.append(('export_id', importId))
            request = requests.get(f"{self.apiURL}/v1/runs/{runId}/scenarios/imports/{importId}", headers=self.headers, params=params)
            if request.status_code == 200:
                return request.json()
            else:
                raise HTTPException.from_status_code(status_code=request.status_code)(message=request.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")
            
    @retry(retry=retry_if_exception_type(UnauthorizedException), stop=stop_after_attempt(2), before=lambda retry_state: retry_state.args[0].reauthenticate())
    def getTableData(self, 
                  runId: int, 
                  scenarioName: str,
                  tableName: str
                  ):
        try:
            params = []
            if runId is not None:
                params.append(('run_id', runId))
            if scenarioName is not None:
                params.append(('scenario_name', scenarioName))
            if tableName is not None:
                params.append(('table_name', tableName))
            request = requests.get(f"{self.apiURL}/v1/runs/{runId}/scenarios/{scenarioName}/table-data/{tableName}", headers=self.headers, params=params)
            if request.status_code == 200:
                return request.json()
            else:
                raise HTTPException.from_status_code(status_code=request.status_code)(message=request.text)
        except Exception:
            self.logger.exception("An unhandled exception occurred - please try again")