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
    # acq = context.client.get_acquisition(file_["hierarchy"]["id"])
    session = context.client.get_session(file_["hierarchy"]["id"])
    # project = context.client.get(acquisition.parents.project)

    # process
    fe = run( 
        file_path,
    )

    # Update session metadata
    session = session.reload()
    file_name = os.path.basename(file_path)
    file_name = file_name.lower()
    if 'manual' in file_name:
        seg_type = 'manual'
    elif 'pred' in file_name:
        seg_type = 'model_predicted'
    
    for label,measurement in fe:
        session.update_info({f'measurements.3d.{seg_type}.{label}': measurement})

    # clean up temp files
    # os.remove(seg_filename)

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
