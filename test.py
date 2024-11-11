from pysimio import pySimio

def auth():
    api = pySimio("https://test.internal.simioportal.com:8443")
    api.authenticate("eyJ1IjoicG9ydGFsLmFkbWluQGZha2VBZGRyZXNzLmNvbSIsInQiOiJzWG9ibU5iRDlmQnNmMERwSGJyOFBteUErNzd3ekxXWk5mU3M5MTE4MTFOaFlXRFA5VlNIazEyc0cyVEVhNmZnb0RIY2Z5RXAvYXByR2xqcHRsdi9MUT09In0=")
    return api

def getExperiments(api):
    return api.getExperiments()

if __name__ == "__main__":
    api = auth()
    # print(api.status())
    print(api.getExperiments())
    # print(api.getExperiment(3926))
    # print(api.getModels())
    # print(api.getModel(4216))
    # print(api.getModelTable(4216))
    # print(api.getRuns())
    # print(api.publishPlan(experimentRunId=39693, publishName="TReedAPITest", publishDescription="Test", scenarioName="treedAPITest1"))
    # print(api.createRun(modelId=14923, experimentRunName="treedAPITest1"))
    # print(api.startRunFromExisting(existingExperimentRunId=39692))
    # print(api.publishRun(experimentRunId=39693, publishName="TReedAPITest", publishDescription="Testing from the API"))
    # print(api.createRunFromExisting(modelId=14923, experimentRunName="treedAPITest2", sourceExperimentRunId=39692, sourceExperimentRunScenarioName="treedAPITest1"))
    print("Complete")