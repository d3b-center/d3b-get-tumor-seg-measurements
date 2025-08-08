# Flywheel SDK gear to extract 3D and 2D measurements from a tumor segmentation file

_Author: Ariana Familiar_  
_Maintainer: D3b-TIRU_ (<flywheel@d3b.center>)

This gear extracts tumor measurements from an input segmentation image and injects the results as session-level metadata on Flywheel.

## :floppy_disk: Usage

_Category:_ Utility

_Gear Level:_

- [ ] Project
- [ ] Subject
- [ ] Session
- [ ] Acquisition
- [X] File

## :mag: Overview

The gear will take a 3D segmentation and calculate the total volume (mm³) for tumor regions. The resulting measurements are added to the session metadata (for the session that the segmentation file is stored within), as described below.

### Inputs

* __input-file:__ Segmentation image to process (nifti).
* __label-mapping:__ Mapping between voxel values and tumor components.   
    Default:  
        1 = Enhancing  
        2 = Non-enhancing  
        3 = Cystic  
        4 = Edema  

### Configuration

* __segmentation_type__ (number, default 0): Whether the input segmentation was created manually or model-predicted. 0=get from file-name, 1=manual, 2=model-predicted. If 0, relies on "manual" or "pred" in the file name to determine the output metadata.
* __debug__ (boolean, default False): Include debug statements in output.

### Outputs

Session metadata updated with measurements: `session.info.measurements.tumor_segm.[model_prediction/manual].[3d/2d].[measurement]`

Such as (default):

- session.info.measurements.tumor_segm.[model_prediction/manual].3d.whole_tumor
- session.info.measurements.tumor_segm.[model_prediction/manual].3d.enhancing
- session.info.measurements.tumor_segm.[model_prediction/manual].3d.non_enhancing
- session.info.measurements.tumor_segm.[model_prediction/manual].3d.cystic
- session.info.measurements.tumor_segm.[model_prediction/manual].3d.edema

- session.info.measurements.tumor_segm.[model_prediction/manual].2d.major_axis
- session.info.measurements.tumor_segm.[model_prediction/manual].2d.minor_axis
- session.info.measurements.tumor_segm.[model_prediction/manual].2d.largest_slice_index
- session.info.measurements.tumor_segm.[model_prediction/manual].2d.cross_sectional_area

Where, for 3D:
- Whole tumor = total volume of all non-zero voxels
- Enhancing = total volume of all voxels with value of 1
- Non-enhancing = total volume of all voxels with value of 2
- Cystic = total volume of all voxels with value of 3
- Edema = total volume of all voxels with value of 4

For 2D:
CSA = 2D cross-sectional area by bidirectional measurements at slice with greatest 3D width


## :exclamation: Limitations

- uses __all__ non-zero voxels to calculate whole-tumor
- support for alternative label mappings not implemented yet
- 2D measurements may error with multi-focal tumors, will result in 'None' measurements
