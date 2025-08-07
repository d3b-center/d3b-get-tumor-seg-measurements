"""Main module."""
import logging
import os

from fw_core_client import CoreClient
from flywheel_gear_toolkit import GearToolkitContext
import flywheel

from .run_level import get_analysis_run_level_and_hierarchy

import nibabel as nib
import numpy as np

log = logging.getLogger(__name__)

fw_context = flywheel.GearContext()
fw = fw_context.client

def process(seg_filename):
    """Process `file_path` and returns a `flywheel.FileEntry` and its corresponding meta.

    Args:
        seg_filename  (Path-like): Path to input-file.
    Returns:
        dict: Dictionary of file attributes to update.
        dict: Dictionary containing the file meta.
    """

    # initialize output
    file_dictionary = {'whole_tumor':0,
                       'enhancing':0,
                       'nonenhancing':0,
                       'cyst':0,
                       'edema':0,
                       }

    # load the input segmentation
    mask = nib.load(seg_filename).get_fdata()
    mask = np.rint(mask)

    # get the separate ROIs
    enhancing_mask = np.logical_and(mask >= 1, mask <= 1)
    nonenhancing_mask = np.logical_and(mask >= 2, mask <= 2)
    cyst_mask = np.logical_and(mask >= 3, mask <= 3)
    edema_mask = np.logical_and(mask >= 4, mask <= 4)
    wt_mask = np.logical_and(mask >= 1, mask <= 3)

    # calculate the number of voxels in each mask
    #   because we know the images are 1x1x1mm isotropic,
    #   we can just sum the voxels to get the volume in mm^3
    file_dictionary['enhancing'] = np.sum(enhancing_mask)
    log.info('Added ENHANCING tumor statistics')

    file_dictionary['nonenhancing'] = np.sum(nonenhancing_mask)
    log.info('Added NON-ENHANCING tumor statistics')

    file_dictionary['cyst'] = np.sum(cyst_mask)
    log.info('Added CYST statistics')

    file_dictionary['edema'] = np.sum(edema_mask)
    log.info('Added EDEMA statistics')

    file_dictionary['whole_tumor'] = np.sum(wt_mask)
    log.info('Added WHOLE TUMOR (enhance + non-enhance) statistics')

    return file_dictionary

def run(seg_filename):
    """Processes file at file_path.

    Args:
        file_type (str): String defining file type.
        file_path (AnyPath): A Path-like to file input.
        project (flywheel.Project): The flywheel project the file is originating
            (Default: None).

    Returns:
        dict: Dictionary of file attributes to update.
        dict: Dictionary containing the file meta.

    """
    fe = process(
        seg_filename
    )
    return fe