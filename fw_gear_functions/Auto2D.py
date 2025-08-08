import cv2
import nibabel as nib
import numpy as np
import os
import csv


def load_nifti_file(file_path):
    return nib.load(file_path).get_fdata()


def find_largest_tumor_slice(volume):
    combined_tumor = np.where(np.isin(volume, [1, 2, 3, 4]), 1, 0)
    slice_areas = np.sum(combined_tumor, axis=(0, 1))
    largest_slice_index = np.argmax(slice_areas)
    return largest_slice_index, combined_tumor[:, :, largest_slice_index]


def find_major_minor_axes(slice):
    contours, _ = cv2.findContours(slice.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    ellipse = cv2.fitEllipse(largest_contour)
    return ellipse


def visualize_ellipse_on_slice(slice, ellipse):
    slice_rgb = cv2.cvtColor(slice.astype(np.uint8) * 255, cv2.COLOR_GRAY2RGB)
    cv2.ellipse(slice_rgb, ellipse, (0, 255, 0), 2)
    cv2.imshow('Fitted Ellipse', slice_rgb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main(folder_path, output_csv):
    # Get all NIfTI files in the folder
    nifti_files = [file for file in os.listdir(folder_path) if file.endswith('.nii.gz')]

    # Write CSV header
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Nifti file name', 'major_axis', 'minor_axis', 'largest slice index']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Process each NIfTI file
        for nifti_file in nifti_files:
            file_path = os.path.join(folder_path, nifti_file)
            volume = load_nifti_file(file_path)
            largest_slice_index, largest_tumor_slice = find_largest_tumor_slice(volume)
            ellipse = find_major_minor_axes(largest_tumor_slice)
            # visualize_ellipse_on_slice(largest_tumor_slice, ellipse)

            (center, axes, orientation) = ellipse
            major_axis, minor_axis = max(axes), min(axes)
            print(f"Largest Tumor Slice Index: {largest_slice_index}")
            print(f"Major Axis: {major_axis}, Minor Axis: {minor_axis}")

            if major_axis is not None and minor_axis is not None:
                # Write to CSV
                writer.writerow({
                    'Nifti file name': nifti_file,
                    'major_axis': major_axis,
                    'minor_axis': minor_axis,
                    'largest slice index': largest_slice_index
                })


if __name__ == "__main__":
    folder_path = "./ManualSegmentations_DIPG"
    output_csv = "./Auto2D_DIPG.csv"

    main(folder_path, output_csv)

