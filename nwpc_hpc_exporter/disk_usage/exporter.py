import time

import click
import yaml
from prometheus_client import start_http_server, Gauge

from nwpc_hpc_exporter.disk_usage.collector import get_disk_usage

item_map = {
    'block_limits': [
        'current',
        'quota',
        'limit'
    ]
}


def load_config(config_file):
    config = None
    with open(config_file, 'r') as f:
        config = yaml.load(f)
    return config


def process_request(tasks):
    t = 5
    for a_task in tasks:
        auth = a_task['auth']

        disk_space_result = get_disk_usage(auth)

        for a_file_system in disk_space_result['file_systems']:
            block_limits = a_file_system['block_limits']
            for an_item in item_map['block_limits']:
                a_task['block_limits_gauge_map'][an_item].labels(
                    file_system=a_file_system['file_system']
                ).set(block_limits[an_item])

    time.sleep(t)


@click.command()
@click.option('--config-file', help="config file path")
def main(config_file):
    config = load_config(config_file)

    start_http_server(8000)

    tasks_config = config['tasks']
    tasks = []
    for a_task in tasks_config:
        block_limits_gauge_map = {
            an_item: Gauge(
                'hpc_' + a_task['name'] + '_disk_usage_block_limit_' + an_item, an_item, ['file_system']
            ) for an_item in item_map['block_limits']
        }
        tasks.append({
            'name': a_task['name'],
            'auth': a_task['auth'],
            'block_limits_gauge_map': block_limits_gauge_map
        })

    while True:
        process_request(tasks)


if __name__ == '__main__':
    main()