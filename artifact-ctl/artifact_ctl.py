import json as JSON
import os
import re
import urllib.parse

import click
import requests


def extract_name(filepath: str) -> str:
    filename = os.path.basename(filepath)  # Get the filename from the path
    match = re.match(r'^(.*)-\d+\.\d+\.\d+\.json$', filename)
    if match:
        return match.group(1)
    return ""


def extract_version(filepath: str) -> str:
    filename = os.path.basename(filepath)  # Get the filename from the path
    match = re.search(r'-(\d+\.\d+\.\d+)\.json$', filename)
    if match:
        return match.group(1)
    return ""


@click.group()
def cli():
    """A CLI tool to manage artifacts."""
    pass


@click.command()
@click.option('--jar', help='Path to JAR file.')
@click.option('--json', help='Path to JSON file.')
@click.option('--host', default='http://localhost:11015', help='Instance url')
@click.option('--namespace', default='default', help='Set your namespace where do you want to deploy the artifact.')
@click.option('--auth_token', help='Auth Token', default='')
def load(jar, json, namespace, host, auth_token):
    namespaces_url = '/v3/namespaces/'
    name = extract_name(json)
    version = extract_version(json)

    with open(json, 'r') as f:
        json_file = JSON.load(f)

    with open(jar, 'rb') as f:
        jar_file = f.read()

    auth_headers = get_auth_headers(auth_token)

    deploy_jar_headers = {
        'Artifact-Extends': '/'.join(json_file['parents']),
        'Artifact-Version': version,
        'Content-Type': 'application/java-archive',
        **auth_headers
    }
    deploy_jar = requests.post(
        f'{host}{namespaces_url}{namespace}/artifacts/{name}',
        headers=deploy_jar_headers,
        data=jar_file
    )

    deploy_json = requests.put(
        f'{host}{namespaces_url}{namespace}/artifacts/{name}/versions/{version}/properties',
        headers=auth_headers,
        data=JSON.dumps(json_file['properties'])
    )

    if deploy_jar.status_code == 200 and deploy_json.status_code == 200:
        print('Successfully deployed artifact')
    else:
        print('Failed to add artifact.')


@click.command()
@click.option('--name', help='Artifact name')
@click.option('--version', help='Artivact version.')
@click.option('--namespace', default='default', help='Set your namespace where do you want to deploy the artifact.')
@click.option('--host', default='http://localhost:11015', help='Instance url')
@click.option('--auth_token', help='Auth Token')
def delete(name, version, ns, host, auth_token):
    namespaces_url = '/v3/namespaces/'
    auth_headers = get_auth_headers(auth_token)

    delete_artifact_res = requests.delete(
        f'{host}{namespaces_url}{ns}/artifacts/{name}/versions/{version}',
        headers=auth_headers
    )

    if delete_artifact_res.status_code == 200:
        print('Successfully deleted artifact')
    else:
        print('Failed to delete artifact.')


def get_auth_headers(auth_token: str = None):
    if auth_token and auth_token != '':
        decoded_token = urllib.parse.unquote(auth_token)
        return {'Authorization': f'Bearer {decoded_token}'}
    return {}


cli.add_command(load)
cli.add_command(delete)

if __name__ == '__main__':
    cli()
