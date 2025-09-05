# HO-3D/H2O-3D Project Overview

## Purpose
This is a Python project for working with the HO-3D (Hand-Object 3D) and H2O-3D (Two Hands-Object 3D) datasets. These datasets contain 3D pose annotations for hands and objects under severe occlusions.

- **HO-3D**: Right hand interacting with objects (103,462 annotated images)
- **H2O-3D**: Two hands interacting with objects (76,340 annotated images)

## Main Features
1. Visualization of hand-object interactions in 2D and 3D
2. Evaluation scripts for pose estimation algorithms
3. Dataset preprocessing and setup utilities
4. Support for MANO hand model integration
5. Point cloud visualization from multiple cameras

## Tech Stack
- **Python**: 2.7 and 3.x compatible (uses `__future__` imports)
- **Core Libraries**: 
  - numpy, matplotlib (visualization)
  - opencv-python (image processing)
  - open3d (3D visualization)
  - scikit-image, transforms3d
  - cython, tqdm
- **3D Models**: 
  - MANO hand model
  - YCB object models

## Academic Context
Used for research in computer vision, specifically 3D hand-object pose estimation. Associated with papers:
- HOnnotate (CVPR 2020)
- Keypoint Transformer (CVPR 2022)