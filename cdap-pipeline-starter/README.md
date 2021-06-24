# CDF Batch Pipeline Starter Tool

## Intro
**CDF Batch Pipeline Starter** - is a tool for automated pipeline starter .
This Python script is used as command-line tool. It starts the pipelines that are given in a document.

### Build from Source Code

**Note:** Python 3.7+ is required

1. Clone document-cleaning from the GitHub repo:

    `git clone https://github.com/orcadaco/document-cleaning.git`

2. Run Setup

    `python setup.py install`


## CLI Usage
To list the available sub-commands for **batch-pipeline-starter** use the `--help` argument.  


Each sub command has usage information available.
``` commandline
batch-pipeline-starter --help
``


## Example usage
``` commandline
batch-pipeline-starter --auth_token <gcloud auth_token> --json_file <json-file-path> --jar <jar-file-path> --host <api_endpoint> --ns <namespace>
```


#### Flags

* --host ................... CDF to connect to.
* --ns ..................... Namespace where the pipelines are.
* --auth_token ............. gcloud auth_token
* --json_file .............. Set path to Dependency JSON file

