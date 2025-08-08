#!/usr/bin/env python
"""The run script."""
import logging
import sys
import typing as t
import os

from flywheel_gear_toolkit import GearToolkitContext

from fw_gear_functions.main import run
from fw_gear_functions.parser import parse_config
from fw_gear_functions.util import create_metadata

log = logging.getLogger(__name__)

def main(context: GearToolkitContext) -> None:  # pragma: no cover
    """Parse config and run."""
    fw, file_path, file_type, config = parse_config(context)
    file_ = context.get_input("input-file")

    # get parent
    acquisition = context.client.get_acquisition(file_["hierarchy"]["id"])
    session = context.client.get(acquisition.parents.session)
    # project = context.client.get(acquisition.parents.project)

    # get the segmentation type either from file-name
    # or user-input (optional config parameter)
    if config['segmentation_type'] == 0:
        file_name = os.path.basename(file_path)
        file_name = file_name.lower()
        if 'manual' in file_name:
            seg_type = 'manual'
        elif 'pred' in file_name:
            seg_type = 'model_predicted'
    elif config['segmentation_type'] == 1:
        seg_type = 'manual'
    elif config['segmentation_type'] == 2:
        seg_type = 'model_predicted'    
    
    # process
    fe = run( 
        file_path,
    )

    # add measurements to session metadata
    session = session.reload()
    session.update_info({'measurements': {f'3d_{seg_type}' : fe}})
    log.info(f"Updated session {session.label} metadata")

    return 0

if __name__ == "__main__":
    with GearToolkitContext(fail_on_validation=False) as context:
        try:
            context.init_logging()
            status = main(context)
        except Exception as exc:
            log.exception(exc)
            status = 1

    sys.exit(status)
