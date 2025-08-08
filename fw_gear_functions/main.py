"""Main module."""
import logging
import os

from fw_core_client import CoreClient
from flywheel_gear_toolkit import GearToolkitContext
import flywheel

from .run_level import get_analysis_run_level_and_hierarchy
from .image_proc import *

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

    # load input file
    im,mask = load_nifti_file(seg_filename)

    # calculate 3D volumes
    voxel_volume = get_voxel_volume(im)
    measure_dictionary = calculate_3d_volumes(mask, voxel_volume, label_mapping)

    threeD_dictionary = {'3d': measure_dictionary}

    # calculate CSA using largest 2D diameters of whole tumor
    largest_slice_index, largest_tumor_slice = find_largest_tumor_slice(mask)
    ellipse = find_major_minor_axes(largest_tumor_slice)
    (center, axes, orientation) = ellipse
    major_axis, minor_axis = max(axes), min(axes)
    csa = calculate_cross_section_area_ellipse(major_axis, minor_axis)

    twoD_dictionary = {'2d': {'major_axis': major_axis,
                              'minor_axis': minor_axis,
                              'largest_slice_index': largest_slice_index,
                              'cross_sectional_area': csa,
                              }}

    return threeD_dictionary,twoD_dictionary

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
