import click
import requests
import json as JSON

@click.command()
@click.option('--jar', help='Path to JAR file.')
@click.option('--json', help='Path to JSON file.')
@click.option('--name', help='Artifact name')
@click.option('--version', help='Artivact version.')
@click.option('--host', default='http://localhost:11015', help="Instance url")
@click.option('--ns', default='default', help='Set your namespace where do you want to deploy the artifact.')
@click.option('--auth_token', help="Authentication token.")
def main(jar, json, name, version, ns, host, auth_token):
    namespaces_url = '/v3/namespaces/'
   
    with open(json, 'r') as f:
        jsonFile = JSON.load(f)

    with open(jar, 'rb') as f:
        jarFile = f.read()

    deploy_jar_headers = {'Artifact-Extends': '/'.join(jsonFile['parents']), 'Artifact-Version': version,
                          'Content-Type': 'application/java-archive', "Authorization": "" if auth_token == None else "Bearer " + auth_token }
    deploy_jar = requests.post(host + namespaces_url + ns +
                               "/artifacts/" + name, headers=deploy_jar_headers, data = jarFile)

    deploy_json_header = {"Authorization": "" if auth_token == None else "Bearer " + auth_token }
    deploy_json = requests.put(host + namespaces_url + ns + "/artifacts/" + name + "/versions/" +
                               version + "/properties", headers=deploy_json_header, data = JSON.dumps(jsonFile['properties']))

    if(deploy_jar.status_code == 200 and deploy_json.status_code == 200):
        print (deploy_jar.content.decode('utf-8'))
    else:
        print("Failed to add artifact.")

if __name__ == '__main__':
    main()
