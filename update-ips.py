import ipaddress
import socket
import subprocess
from typing import Iterator, AnyStr, Iterable

import click

ITEM_FORMAT = 'allow {};'
COMMENT_FORMAT = '# {}'


def resolve_ip(domain: str) -> str:
    return socket.gethostbyname(domain)


def validate_ip(address: str) -> bool:
    try:
        ipaddress.ip_network(address)
    except ValueError:
        return False
    else:
        return True


def read_input_file(file: str) -> Iterator[AnyStr]:
    with open(file, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            yield line.rstrip('\n')


def read_file(file: str) -> str:
    with open(file, 'r') as f:
        yield from f.read()


def write_file(file: str, data: str):
    with open(file, 'w') as f:
        f.write(data)


def read_input_files(files: Iterable[str]) -> Iterator[AnyStr]:
    for file in files:
        yield from read_input_file(file)


def get_ip(line: str) -> str:
    output = ''
    parts = line.split('#', 1)
    item = parts[0].strip(' ').rstrip(';')
    comment = parts[1] if len(parts) > 1 else ''
    if item and not validate_ip(item):
        try:
            item = resolve_ip(item)
        except (socket.gaierror, UnicodeError) as e:
            comment = '{} -- Error: {}'.format(item, e)
            item = ''
    if item:
        output += ITEM_FORMAT.format(item)
    if item and comment:
        output += '  '
    if comment:
        output += COMMENT_FORMAT.format(comment.lstrip(' '))
    return output


def get_ips(files: Iterable[str]) -> Iterator[str]:
    for line in read_input_files(files):
        yield get_ip(line)


@click.command()
@click.argument('src', nargs=-1)
@click.option('-o', '--output-file', type=click.Path(writable=True))
@click.option('-r', '--run', type=click.Path(exists=True))
def update_ips(src, output_file=None, run=None):
    """Read domain and ip files and generate an output compatible with Nginx
    """
    last_out = ''
    exit_code = 0
    ips = get_ips(src)
    out = '\n'.join(ips)
    if not output_file:
        print(out)
    if run and not output_file:
        raise click.BadParameter('output-file parameter is required for run.')
    if output_file:
        # Read last output and write new output
        last_out = read_file(output_file)
        write_file(output_file, out)
    if output_file and out != last_out and run:
        # Output changed and run is defined
        subprocess.check_call([run])
    elif output_file and out != last_out and not run:
        # Output changed and run is undefined
        exit_code = 1
    exit(exit_code)


if __name__ == '__main__':
    update_ips()
