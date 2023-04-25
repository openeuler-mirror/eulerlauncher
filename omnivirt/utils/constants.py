STORAGE_PROTOCOL_ISCSI = 'iscsi'
STORAGE_PROTOCOL_FC = 'fibre_channel'
STORAGE_PROTOCOL_SMBFS = 'smbfs'
STORAGE_PROTOCOL_RBD = 'rbd'

DISK = "VHD"

IMAGE_LOCATION_REMOTE = 'Remote'
IMAGE_LOCATION_LOCAL = 'Local'

IMAGE_STATUS_INIT = 'N/A'
IMAGE_STATUS_DOWLOADABLE = 'Downloadable'
IMAGE_STATUS_DOWNLOADING = 'Downloading'
IMAGE_STATUS_LOADING = 'Loading'
IMAGE_STATUS_READY = 'Ready'

IMAGE_LOAD_SUPPORTED_TYPES = ['qcow2.xz', 'qcow2']

ARCH_MAP = {
    'AMD64': 'x86_64',
    'arm64': 'aarch64',
    'x86_64': 'x86_64'
}

VM_STATE_MAP = {
    2: 'Running',
    3: 'Stopped',
    10: 'Rebooting',
    32768: 'Paused',
    32769: 'Suspended',
    99: 'N/A'
    }

OS_MAP = {
    'Darwin': 'MacOS',
    'Windows': 'Win'
}