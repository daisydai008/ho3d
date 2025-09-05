# Suggested Commands

## Setup Commands
```bash
# Create conda environment
conda create -n python2.7 python=2.7
source activate python2.7

# Install dependencies
pip install numpy matplotlib scikit-image transforms3d tqdm opencv-python cython open3d

# Setup MANO model (after downloading from http://mano.is.tue.mpg.de)
python setup_mano.py ${MANO_PATH}
```

## Dataset Visualization
```bash
# Visualize HO-3D dataset (matplotlib)
python vis_HO3D.py ${DB_PATH} ${YCB_PATH}
python vis_HO3D.py ${DB_PATH} ${YCB_PATH} -split 'evaluation'

# Visualize HO-3D dataset (open3d 3D viewer)
python vis_HO3D.py ${DB_PATH} ${YCB_PATH} -visType 'open3d'

# Visualize specific sequence and frame
python vis_HO3D.py ${DB_PATH} ${YCB_PATH} -split train -seq MC1 -id 0000 -visType open3d

# Visualize H2O-3D dataset
python vis_H2O3D.py ${DB_PATH} ${YCB_PATH}
python vis_H2O3D.py ${DB_PATH} ${YCB_PATH} -visType 'open3d'

# Visualize point cloud from all cameras (HO-3D v3 only)
python vis_pcl_all_cameras.py ${DB_PATH} --seq SEQ --fid FID
```

## Evaluation
```bash
# Generate predictions (creates pred.json)
python pred.py ${DB_PATH} --version v2  # or v3

# Run evaluation locally (after downloading GT)
python eval.py <input_dir_with_pred_and_gt> <output_dir_for_results> --version v2
python eval.py <input_dir_with_pred_and_gt> <output_dir_for_results> --version v3

# Compare automatic annotations with manual ground truth (HO-3D v3 only)
python compare_manual_anno.py ${DB_PATH}
# This compares fingertip positions between automatic and manual annotations
# Outputs: Average MSE and standard deviation in millimeters

# Create submission for Codalab
zip -j pred.zip pred.json
```

## System Commands (Linux)
- git, ls, cd, grep, find (standard Linux commands)
- rg (ripgrep) for fast searching