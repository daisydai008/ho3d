# Project Structure

## Root Directory Files
- **vis_HO3D.py**: Main visualization script for HO-3D dataset
- **vis_H2O3D.py**: Visualization script for H2O-3D dataset (two hands)
- **eval.py**: Evaluation script for computing metrics
- **pred.py**: Generate predictions for evaluation
- **setup_mano.py**: Setup script for MANO hand model
- **vis_pcl_all_cameras.py**: Visualize point clouds from multiple cameras
- **compare_manual_anno.py**: Compare automatic vs manual annotations
- **generate_ho3d_videos.py**: Generate video outputs from sequences

## Utils Directory
- **eval_util.py**: EvalUtil class for evaluation metrics
- **vis_utils.py**: Visualization utility functions
- **fh_utils.py**: Additional utility functions

## Data Directories (gitignored)
- **HO3D_dataset/**: Main dataset directory
  - HO3D/train/: Training sequences
  - HO3D/evaluation/: Evaluation sequences
  - HO3D/calibration/: Camera calibration data
  - HO3D/manual_annotations/: Manual GT annotations
  - YCB_Video_Models/: YCB object 3D models
  - mano_v1_2/: MANO hand model files

## Configuration
- **.gitignore**: Python project gitignore
- **README.md**: Comprehensive documentation
- **GEN_VIDEO.md**: Video generation documentation