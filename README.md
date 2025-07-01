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
from pysimio import pySimio

simio_portal_url = "https://simio.portal"
personal_access_token = os.getenv("PERSONAL_ACCESS_TOKEN")

api = pySimio(simio_portal_url)
api.authenticate(personalAccessToken=personal_access_token)
```

## Available Methods
### Additional documentation and usage examples are coming soon.

* status: Return the current heartbeat status from the Simio Portal Instance
* reauthenticate: Attempts to reauthenticate to the API using the PAT provided during authentication
* authenticate: Authenticate to the API using a PAT or SAML Assertion
* getModels: Returns a json list of all current Simio Portal models
* getModel: Returns a json representation of a specific Simio Portal model
* getModelTable: Returns a json representation of a table on a Simio Portal model
* getExperiments: Returns a json list of all current Simio Portal expermients on a model
* getExperiment: Returns a json representation of a Simio Portal experiment
* publishPlan: Publish a specific Simio Plan within Simio Portal
* uploadAndPublishPlan: Upload a Simio Model, and publish the plan within Simio Portal
* publishRun: Publish a specific Simio Run within Simio Portal
* deletePublishedRun: Deletes a published Simio Portal Run
* getRuns: Returns a json list of all current Simio Portal runs
* getRun: Returns a json representation of a specific Simio Portal run
* deleteRun: Delete a specific Simio Run within Simio Portal
* cancelRun: Cancels a specific Simio Run within Simio Portal
* setRunTimeOptions: Sets the Time Options on a specific Simio Portal Run
* cancelPlan: Cancels a specific Simio Plan within Simio Portal
* createRun: Creates a new Simio Run within Simio Portal
* startRun: Creates and starts a new Simio Experiment run within Simio Portal. To update control parameters, you would add them to the "scenarios" section in the JSON and run it again.
* createRunFromExisting: Create a new instances of a Simio Run within Simio Portal from an existing Simio Run
* startRunFromExisting: Start a new run of a Simio Run from an existing Simio Run
* getExport: Returns a json representation of a Simio Export from Simio Portal
* getImport: Returns a json representation of a Simio Import from Simio Portal
* getTableData: Returns a json representation of a Simio Table
* deleteModel: Deletes a Simio Model from Simio Portal
* deleteProject: Deletes a Simio Project from Simio Portal
* uploadProject: Upload a new Simio Project file to Simio Portal
* getProjects: Returns a json list of existing Simio Projects from Simio Portal
* getProject: Returns a json representation of a Simio Project from Simio Portal
* setControlValues: Update Control Values
* setScenarioName: Update Scenario Name in a Simio Run within Simio Portal

## License
This project is licensed under the Apache License.
