import requests
import json
import asyncio
from os import environ
import click
import time
from CDFApi import CDFApi

loop = asyncio.get_event_loop()
running_pipeline = {}


@click.command()
@click.option('--host', default='http://localhost:11015', help="Instance api_endpoint")
@click.option('--ns', default='default', help='Namespace')
@click.option('--auth_token', help="Instance auth_token")
@click.option('--json_file', required=True, help="Set path to Dependency JSON file.")
@click.option('--sequence', is_flag=True, help="Run pipelines in a particual")
def main(host, ns, auth_token, json_file, sequence):
    auth_token = auth_token if auth_token is not None else environ.get(
        'AUTH_TOKEN')
    cdf_api = CDFApi(auth_token, host, ns)
    all_deployed_pipelines = cdf_api.get_deployed_pipelines()
    istance_pipelines = pipelines_datas(cdf_api, all_deployed_pipelines)
    output_file = open("output_status.txt", "w")
    with open(json_file, 'r') as f:
        pipelines_json_file = json.load(f)

    result = loop.run_until_complete(
        check_and_execute_sequence(cdf_api, istance_pipelines, pipelines_json_file, output_file, sequence)
        ) if sequence else loop.run_until_complete(
        check_and_execute(cdf_api, istance_pipelines, pipelines_json_file, output_file))
    if not sequence:
        write_status(cdf_api, result, output_file)

    print("Successfully executed. Check output_file.txt to see status result.")


async def check_and_execute(cdf_api, istance_pipelines, pipelines_json_file, output_file):
    tasks = []
    for pipeline in istance_pipelines:
        if pipeline['name'] in pipelines_json_file['pipelines']:
            macros = pipelines_json_file.get('pipelines').get(pipeline['name'])[0] if len(
                pipelines_json_file.get('pipelines').get(pipeline['name'])) > 0 else None
            task = asyncio.ensure_future(cdf_api.start_pipeline(
                pipeline['name'], pipeline['program_type'], pipeline['program_id'], macros))
            tasks.append(task)
        # else:
        #     output_file.write(pipeline['name'] + " does not exist on JSON file." + "\n")
    return await asyncio.gather(*tasks, return_exceptions=True)


async def check_and_execute_sequence(cdf_api, instance_pipelines, pipelines_json_file, output_file, sequence):
    tasks = []
    for pipeline in instance_pipelines:
        if pipeline['name'] in pipelines_json_file['pipelines']:
            macros = pipelines_json_file.get('pipelines').get(pipeline['name'])[0] if len(
                pipelines_json_file.get('pipelines').get(pipeline['name'])) > 0 else None
            task = asyncio.ensure_future(start_and_wait_to_stop(
                cdf_api, pipeline, macros, output_file))
            tasks.append(task)
        # else:
        #     output_file.write(pipeline['name'] + " does not exist on JSON file." + "\n")
    return await asyncio.gather(*tasks, return_exceptions=True)


async def start_and_wait_to_stop(cdf_api, pipeline, macros, output_file):
    response = await cdf_api.start_pipeline(
        pipeline['name'], pipeline['program_type'], pipeline['program_id'], macros)
    if response['status'] == 200:
        running_pipeline.update(pipeline)
        print(response['pipeline_name'], 'started successfully.')
        output_file.write(
            response['pipeline_name'] + " started successfully at " + response['time_stamp'] + "." + "\n")
    else:
        print(response['pipeline_name'], 'failed to start.')
        output_file.write(response['pipeline_name'] +
                          " failed to start." + "\n")

    await check_status(cdf_api, pipeline, output_file)


def pipelines_datas(cdf_api, all_deployed_pipelines):
    result = []
    for pipeline in all_deployed_pipelines:
        # ignore properties by name
        if not pipeline['name'] in ('_Tracker', 'dataprep'):
            individual_pipeline = cdf_api.get_individual_deployed_pipeline(
                pipeline['name'])
            result.append({
                'name': pipeline['name'],
                'program_type': 'workflows' if individual_pipeline['programs'][-1]['type'] == 'Workflow' else
                individual_pipeline['programs'][-1]['type'].lower(),
                'program_id': individual_pipeline['programs'][-1]['name'],
            })
    return result


async def check_status(cdf_api, pipeline, output_file):
    looping = True
    while looping:
        time.sleep(15)
        response = cdf_api.check_pipeline_status(running_pipeline['name'], running_pipeline['program_type'],
                                                 running_pipeline['program_id']).get('status')
        print(running_pipeline['name'], "is", response)
        if response == 'STOPPED':
            looping = False

    tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
    output_file.write(running_pipeline['name'] + " status: " +
                      running_pipeline['status'] + " at " + tm + "\n")
    return None


def write_status(cdf_api, result, output_file):
    for value in result:
        if value['status'] == 200:
            print(value['pipeline_name'], 'started successfully.')
            output_file.write(
                value['pipeline_name'] + " started successfully at " + value['time_stamp'] + "." + "\n")
        else:
            print(value['pipeline_name'], 'failed to start.')
            output_file.write(
                value['pipeline_name'] + " failed to start at " + value['time_stamp'] + "." + "\n")

    for pipeline in result:
        time.sleep(10)
        while True:
            pipeline['status'] = cdf_api.check_pipeline_status(
                pipeline['pipeline_name'], pipeline['program_type'], pipeline['program_id']).get('status')
            if pipeline['status'] == "STOPPED" or pipeline['status'] == "RUNNING":
                break
        output_file.write(pipeline['pipeline_name'] +
                          " status: " + pipeline['status'] + "\n")


if __name__ == '__main__':
    main()
