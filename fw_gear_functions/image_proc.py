import logging
log = logging.getLogger(__name__)

import nibabel as nib
import numpy as np
import cv2

def load_nifti_file(file_path):
    """Load a NIfTI file and return its image object and data."""
    im = nib.load(file_path)
    mask = im.get_fdata()
    return im,mask

def get_voxel_volume(im):
    """Get the volume of a single voxel in mm³."""
    # Calculate the volume of a single voxel
    sx, sy, sz = im.header.get_zooms()[:3] # in mm's
    log.info(f"Voxel dimensions: x={sx}mm, y={sy}mm, z={sz}mm")
    voxel_volume = sx * sy * sz
    log.info(f"Volume of a single voxel: {voxel_volume:.2f} mm³")
    return voxel_volume

def calculate_3d_volumes(mask, voxel_volume, label_mapping):
    """Calculate the volumes of different tumor components in a 3D segmentation mask."""
    mask = np.rint(mask)

    # get volumes for the separate ROIs
    output_dict = {}
    max_seg_value = np.max(mask) # maximum value in the segmentation
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
        output_dict[label] = volume
        log.info(f'Found 3D volume {volume:.2f} mm³ for label {label} (value={voxel_value})')

    return output_dict

def find_largest_tumor_slice(volume):
    """Find the largest tumor slice in a 3D volume."""
    combined_tumor = np.where(np.isin(volume, [1, 2, 3, 4]), 1, 0)
    slice_areas = np.sum(combined_tumor, axis=(0, 1))
    largest_slice_index = np.argmax(slice_areas)
    log.info(f"Largest 2D Tumor Slice Index: {largest_slice_index}")
    return largest_slice_index, combined_tumor[:, :, largest_slice_index]

def find_major_minor_axes(slice):
    """Find the major and minor axes of the largest contour in a 2D slice."""
    contours, _ = cv2.findContours(slice.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    ellipse = cv2.fitEllipse(largest_contour)
    return ellipse

def calculate_cross_section_area_approx(diameter1, diameter2):
  """
  Calculates the approximate cross-sectional area using the product of two perpendicular diameters.

  Args:
    diameter1: The length of the first largest diameter.
    diameter2: The length of the second largest diameter, perpendicular to the first.

  Returns:
    The approximate cross-sectional area.
  """
  return diameter1 * diameter2
