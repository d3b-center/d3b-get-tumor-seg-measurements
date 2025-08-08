"""Main module."""
import logging
import os
from collections import Counter

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

    label_mapping = {
        0: 'background',
        1: 'enhancing',
        2: 'nonenhancing',
        3: 'cyst',
        4: 'edema'
    }

    # load the input segmentation
    im = nib.load(seg_filename)
    mask = im.get_fdata()
    mask = np.rint(mask)
    max_seg_value = np.max(mask) # maximum value in the segmentation

    # Calculate the volume of a single voxel
    sx, sy, sz = im.header.get_zooms()[:3] # in mm's
    log.info(f"Voxel dimensions: x={sx}mm, y={sy}mm, z={sz}mm")
    voxel_volume = sx * sy * sz
    log.info(f"Volume of a single voxel: {voxel_volume:.2f} mm³")

    # get volumes for the separate ROIs
    file_dictionary = {}
    for voxel_value,label in label_mapping.items():
        # Count the number of non-zero voxels (representing the mask)
        if voxel_value == 0:
            wt_mask  = np.logical_and(mask >= 1, mask <= max_seg_value)
            n_voxels = np.sum(wt_mask)
            label = 'whole_tumor'
            voxel_value = 'non-zero'
        else:
            n_voxels = np.sum(mask == voxel_value)
        # total volume is number of voxels * volume of a single voxel
        volume = n_voxels * voxel_volume
        file_dictionary[label] = volume
        log.info(f'Found volume {volume:.2f} mm³ for label {label} (value={voxel_value})')

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
