# Deploy Pipelines to CDAP/CDF

## Function

This will loop through a directory of .JSON files that were exported from cdap/cdf and upload all files in that directory to the specified namespace.

### How to Use

| Variable | Use
|----------- |-------------------------------------------------------------------
| dir	    | ${DIR} - Env Variable for the Directory that contains your JSON files
| namespace | ${NAMESPACE} - Namespace to upload pipelines to
| host | ${CDAP_ENDPOINT} - Endpoint for PUT command (APIEndpoint)
| authToken | ${AUTH_TOKEN} - GCloud Auth Token for CDF

### Terminal commands to fill Environment Variables

```bash
gcloud auth login

export AUTH_TOKEN=$(gcloud auth print-access-token)

export LOCATION=region

export INSTANCE_ID=instance-id

export CDAP_ENDPOINT=$(gcloud beta data-fusion instances describe \
--location=${LOCATION} \
--format="value(apiEndpoint)" \
${INSTANCE_ID})

export DIR=directory

export NAMESPACE=namespace

```