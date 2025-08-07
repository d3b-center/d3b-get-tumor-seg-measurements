"""Parser module."""
from fw_core_client import CoreClient

from . import __version__, pkg_name

def parse_config(context):
    """Parses config.json."""
    file_type = context.get_input("input-file")["object"]["type"]
    file_path = context.get_input("input-file")["location"]["path"]
    config = context.config
    api_key_in = context.get_input("api-key")
    fw = CoreClient(
        api_key=api_key_in.get("key"), client_name=pkg_name, client_version=__version__
    )

    return fw, file_path, file_type, config
