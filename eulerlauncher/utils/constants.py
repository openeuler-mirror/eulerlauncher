IMAGE_LOCATION_REMOTE = 'Remote'
IMAGE_LOCATION_LOCAL = 'Local'

INSTANCE_STATE_MAP = {
    0: 'N/A',
    1: 'Running',
    2: 'Blocked',
    3: 'Paused',
    4: 'Shutdown',
    5: 'Shutoff',
    6: 'Crashed',
    7: 'Suspended',
    99: 'N/A'
}

IMAGE_STATE_MAP = {
    0: 'N/A',
    1: 'Downloadable',
    2: 'Downloading',
    3: 'Loading',
    4: 'Ready'
}

IMAGE_LOAD_SUPPORTED_TYPES = ['qcow2.xz', 'qcow2']

ARCH_MAP = {
    'AMD64': 'x86_64',
    'arm64': 'aarch64',
    'x86_64': 'x86_64'
}

OS_MAP = {
    'Darwin': 'MacOS',
    'Windows': 'Win'
}