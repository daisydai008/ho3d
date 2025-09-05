# compare_manual_anno.py Usage Guide

## Purpose
This script compares the automatic annotations (from HOnnotate method) with manual ground-truth annotations to measure the accuracy of the automatic annotation pipeline. It specifically evaluates fingertip locations.

## Prerequisites
1. HO-3D v3 dataset must be downloaded and properly structured
2. The dataset must include the `manual_annotations` folder containing .npy files
3. The corresponding training sequences must be present

## How to Run

```bash
python compare_manual_anno.py ${DB_PATH}
```

Where `${DB_PATH}` is the path to the HO-3D dataset root directory (containing train/, evaluation/, manual_annotations/ folders)

Example:
```bash
python compare_manual_anno.py /path/to/HO3D_dataset/HO3D
```

## What it Does

1. **Loads manual annotations**: Reads .npy files from `${DB_PATH}/manual_annotations/`
   - These contain manually annotated 3D positions of 5 fingertips
   - 53 frames were manually annotated using point clouds from all cameras

2. **Loads automatic annotations**: For each manual annotation, loads the corresponding automatic annotation from:
   - `${DB_PATH}/train/{sequence}1/meta/{frame_id}.pkl`
   - Extracts fingertip joints (indices 16-20 in MANO order)

3. **Calculates Mean Squared Error (MSE)**: 
   - Computes Euclidean distance between manual and automatic fingertip positions
   - Averages across all 5 fingertips per frame

4. **Reports statistics**:
   - Number of valid samples processed
   - Average MSE in millimeters
   - Standard deviation in millimeters

## Expected Output

```
Number of samples = 53
Average MSE - X.XXmm, Standard Deviation - Y.YYmm
```

This provides a quantitative measure of the automatic annotation accuracy. Lower MSE values indicate better automatic annotation quality.

## Notes
- Only works with HO-3D v3 (which includes manual annotations)
- Skips test set sequences (only evaluates training sequences)
- Uses fingertip IDs: [20, 19, 18, 17, 16] corresponding to thumb to pinky tips