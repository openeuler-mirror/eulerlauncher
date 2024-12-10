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

IMAGE_LOAD_SUPPORTED_TYPES = ['qcow2', 'raw', 'vmdk', 'vhd', 'vhdx', 'qcow', 'vdi']
IMAGE_LOAD_SUPPORTED_TYPES_COMPRESSED = ['qcow2.xz', 'raw.xz', 'vmdk.xz', 'vhd.xz', 'vhdx.xz', 'qcow.xz', 'vdi.xz']

ARCH_MAP = {
    'AMD64': 'x86_64',
    'arm64': 'aarch64',
    'x86_64': 'x86_64'
}

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

OS_MAP = {
    'Darwin': 'MacOS',
    'Windows': 'Win'
}