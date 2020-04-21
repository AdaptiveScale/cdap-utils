#! /usr/bin/env python

##################################################################
# CDAP Pipeline Extraction Tool
#
# Author: Tony Hajdari, tony@adaptivescale.com
#
# Use:  Allows you to extract all the deployed 
#       pipelines from your CDAP instance.
##################################################################
import requests, json, logging, sys, os

# Logger Config
log = logging.getLogger('')
log.setLevel(logging.DEBUG)
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
log.addHandler(ch)

host = 'localhost'
port = '11015'
cdap = 'http://' + host + ':' + port
namespaces = '/v3/namespaces'
version = '/v3/version'
drafts = '/v3/configuration/user'
p = {'name': '', 'description': '', 'artifact': '', 'config': ''}
output = 'exported_pipelines'


def getJSON(url):
    r = requests.get(url)
    d = r.json()
    return d  # returns a dict

def getVersion():
    ver = getJSON(cdap + version).get('version')
    return ver

# Example of an App collection endpoint
# http://localhost:11015/v3/namespaces/default/apps
def getApps(ns):
    return getJSON(cdap + namespaces + '/' + ns + '/apps')


# Example of an individual App endpoint
# http://localhost:11015/v3/namespaces/default/apps/MyAppName
def getApp(ns,pipeline_name):
    return getJSON(cdap + namespaces + '/' + ns + '/apps' + '/' + pipeline_name)


# Get the available namespaces for this CDAP instance
def getNamespaces():
    return getJSON(cdap + namespaces)


# Get pipeline drafts
def getDrafts():
    return getJSON(cdap + drafts)


# Write the pipelline config out to a file
def exportPipeline(ns, pipeline_name, data):
    fileName = pipeline_name + '.json'
    directory = output + '/' + ns
    path = directory + '/' + fileName

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, 'w') as f:
        f.write(data)


# Get the draft pipelines -- this is NOT namespace specific
# will retrieve the drafts in ALL namespaces
cdap_version = getVersion()
drafts = getDrafts()

# loop through all namespaces
for namespace in getNamespaces():

    # set the global namespace name
    ns = namespace.get('name')
    log.debug('Namespace: %s', ns)

    # get all the drafts per namespace
    d = drafts.get('property').get('hydratorDrafts').get(ns)
    if not d:
        log.info('There are no draft pipelines in namespace: {}'.format(ns))
    else:
        for item in d.items():
            name = item[1]['name']
            p['name'] = name
            p['description'] = item[1]['description']
            p['artifact'] = item[1]['artifact']
            p['config'] = item[1]['config']
            spec = json.dumps(p)
            # log.debug('Draft Pipeline: %s', spec)
            exportPipeline(ns, name + '-DRAFT-' + cdap_version, spec)

    # get the deployed pipelines in this namespace
    for i in getApps(ns):
        # filer out anything other than cdap-data-pipeline
        artifactType = i.get('artifact').get('name')
        if "cdap-data-pipeline" in artifactType:
            pipeline_name = i['name']
            if not pipeline_name in ('_Tracker', 'dataprep'):
                log.debug('App Namespace: %s', ns)
                log.debug('Pipeline name: %s', pipeline_name)
                app = getApp(ns, pipeline_name)
                # log.debug('Pipeline = %s', json.dumps(app, sort_keys=True, indent=4))
                p['name'] = app.get('name')
                p['description'] = app.get('description')
                p['artifact'] = app.get('artifact')
                p['config'] = json.loads(app.get('configuration'))
                spec = json.dumps(p, sort_keys=True, indent=4)
                # exportPipeline(ns, pipeline_name + cdap_version, spec)
                exportPipeline(ns, pipeline_name + "-cdap-data-pipeline", spec)
