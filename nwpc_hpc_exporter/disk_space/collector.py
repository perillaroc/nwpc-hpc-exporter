import re
import locale
from paramiko import SSHClient, AutoAddPolicy


def get_ssh_client(auth):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(auth['host'], auth['port'], auth['user'], auth['password'])
    return client


def run_df_command(client) -> (str,str):
    command = '/usr/bin/df -m'

    stdin, stdout, stderr = client.exec_command(command)
    std_out_string = stdout.read().decode('UTF-8')
    std_error_out_string = stderr.read().decode('UTF-8')

    return std_out_string, std_error_out_string


def get_disk_space(client) -> dict:
    std_out_string, std_error_out_string = run_df_command(client)
    result_lines = std_out_string.split("\n")

    detail_pattern = r'^(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+)'
    detail_prog = re.compile(detail_pattern)
    disk_space_result = dict()
    file_system_list = list()

    for a_line in result_lines[1:]:
        detail_re_result = detail_prog.match(a_line)
        if detail_re_result:
            file_system = detail_re_result.group(1)

            mb_blocks = detail_re_result.group(2)
            if mb_blocks.isdigit():
                mb_blocks = locale.atoi(mb_blocks)

            free_disk_space = detail_re_result.group(3)
            if free_disk_space.isdigit():
                free_disk_space = locale.atoi(free_disk_space)

            space_used_percent = detail_re_result.group(4)
            if space_used_percent[-1] == '%':
                space_used_percent = space_used_percent[:-1]

            inode_used = detail_re_result.group(5)
            if inode_used.isdigit():
                inode_used = locale.atoi(inode_used)

            inode_used_percent = detail_re_result.group(6)
            if inode_used_percent[-1] == '%':
                inode_used_percent = inode_used_percent[:-1]

            mounted_on = detail_re_result.group(7)

            current_file_system = {
                'file_system': file_system,
                'gb_blocks': mb_blocks / 1000.0,
                'free_space': free_disk_space,
                'space_used_percent': space_used_percent,
                'inode_used': inode_used,
                'inode_used_percent': inode_used_percent,
                'mounted_on': mounted_on
            }

            file_system_list.append(current_file_system)

    disk_space_result['file_systems'] = file_system_list
    return disk_space_result
