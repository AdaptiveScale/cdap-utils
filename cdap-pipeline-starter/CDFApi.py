import requests
import time


class CDFApi:
    token = None
    api_endpoint = None
    headers = None
    namespace = 'default'
    status_url = '/status'
    namespaces_url = '/v3/namespaces'
    version_url = '/v3/version'
    drafts_url = '/v3/configuration/user'

    def __init__(self, auth_token, api_endpoint, namespace):
        self.api_endpoint = api_endpoint
        self.token = auth_token
        self.namespace = namespace
        if auth_token is not None:
            self.headers = {"Authorization": "Bearer " + self.token}

    def check_status(self):
        return requests.get(self.api_endpoint + self.status_url, allow_redirects=True, headers=self.headers)

    def get_individual_namespace(self):
        return requests.get(self.api_endpoint + self.namespaces_url + "/" + self.namespace, allow_redirects=True,
                            headers=self.headers).json()

    def get_deployed_pipelines(self):
        return requests.get(self.api_endpoint + self.namespaces_url + "/" + self.namespace + "/apps",
                            headers=self.headers).json()

    def get_individual_deployed_pipeline(self, name):
        return requests.get(self.api_endpoint + self.namespaces_url + "/" + self.namespace + "/apps/" + name,
                            headers=self.headers).json()

    async def start_pipeline(self, pipeline_name, program_type, program_id, macros):
        if self.headers != None:
            self.headers.update({'Content-Type': 'application/json'})
        else:
            self.headers = {'Content-Type': 'application/json'}
        response = requests.post(self.api_endpoint + self.namespaces_url + "/" + self.namespace + "/apps/" +
                                 pipeline_name + "/" + program_type + "/" + program_id + "/start", headers=self.headers)
        tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
        return {"pipeline_name": pipeline_name, "program_type": program_type, "program_id": program_id,
                "status": response.status_code, "time_stamp": tm}

    def check_pipeline_status(self, pipeline_name, program_type, program_id):
        return requests.get(
            self.api_endpoint + self.namespaces_url + "/" + self.namespace + "/apps/" + pipeline_name + "/" + program_type + "/" + program_id + "/status",
            headers=self.headers).json()
