# SDK gear to extract 3D and 2D measurements from a tumor segmentation

This gear extracts tumor measurements from an input image and injects the results as file-level metadata on Flywheel.

## Usage

Run at the file-level.

### Inputs

* input-file: Image to process. * Must have "manual" or "pred" in the file name according to how the segmentation was created *
* label-mapping: Mapping between voxel values and tumor components
    Default:
        1 = Enhancing
        2 = Non-enhancing
        3 = Cystic
        4 = Edema

### Outputs

Whole tumor volume & subcomponent volumes
- 3D volume
- 2D volume by bidirectional measurements at slice with greatest 3D width

Session metadata updated with measurements for each label, such as:
- session.info.measurements.[3d/2d].[model_prediction/manual].whole_tumor
- session.info.measurements.[3d/2d].[model_prediction/manual].enhancing
- session.info.measurements.[3d/2d].[model_prediction/manual].non_enhancing
- session.info.measurements.[3d/2d].[model_prediction/manual].cystic
- session.info.measurements.[3d/2d].[model_prediction/manual].edema

### Configuration

* __debug__ (boolean, default False): Include debug statements in output.

### Limitations

Relies on "manual" or "pred" in the file name to determine the output metadata.
