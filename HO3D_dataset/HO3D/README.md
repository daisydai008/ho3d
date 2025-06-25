# HO-3D Dataset v3

## Description
HO-3D_v3 is a dataset with 3D pose annotations for hand-objects interactions. It contains **103,462** hand-object 3D pose annotated RGB images and their corresponding depth maps. The dataset features:

- **10 different human subjects** (3 female and 7 male)
- **10 different objects** from the YCB dataset
- **MANO hand model** for hand pose estimation

## Dataset Structure

```
HO3D/
├── train/                  # 55 training sequences
│   ├── ABF10/
│   │   ├── rgb/           # RGB images (.jpg format)
│   │   ├── depth/         # 16-bit depth maps (.png format)
│   │   └── meta/          # Annotation files (.pkl format)
│   └── ...
├── evaluation/             # 13 evaluation sequences
│   └── ...
├── calibration/           # Multi-camera calibration parameters
├── manual_annotations/    # Manual fingertip annotations (53 frames)
├── train.txt             # List of training images (sequence/frame format)
├── evaluation.txt        # List of evaluation images (sequence/frame format)
└── joint_order.png       # MANO joint ordering visualization
```

## Annotation Format

### Training Data Annotations
Each `meta/*.pkl` file contains a dictionary with the following keys:

| Field | Shape | Description |
|-------|-------|-------------|
| `objTrans` | (3,) | Object translation vector |
| `objRot` | (3,) | Object rotation in axis-angle representation |
| `handPose` | (48,) | 3D rotation of 16 hand joints in axis-angle (MANO format) |
| `handTrans` | (3,) | Hand translation vector |
| `handBeta` | (10,) | MANO hand shape parameters |
| `handJoints3D` | (21, 3) | 21 3D hand joint locations |
| `objCorners3D` | (8, 3) | 3D bounding box corners of the object |
| `objCorners3DRest` | (8, 3) | 3D bounding box corners before transformation |
| `objName` | str | Object name from YCB dataset |
| `objLabel` | int | Object label from YCB dataset |
| `camMat` | (3, 3) | Intrinsic camera parameters |
| `handVertContact` | (778,) | Boolean mask: MANO vertex contact with object (<4mm) |
| `handVertDist` | (778,) | Distance of MANO vertices to object surface |
| `handVertIntersec` | (778,) | Boolean mask: MANO vertices inside object surface |
| `handVertObjSurfProj` | (778, 3) | Projection of MANO vertices on object surface |

### MANO Joint Hierarchy

The 16 joints in handPose follow MANO convention:

| Index | Joint Name | Description             |
|-------|------------|-------------------------|
| 0     | Wrist/Root | Global hand orientation |
| 1-3   | Thumb      | CMC, MCP, IP joints     |
| 4-6   | Index      | MCP, PIP, DIP joints    |
| 7-9   | Middle     | MCP, PIP, DIP joints    |
| 10-12 | Ring       | MCP, PIP, DIP joints    |
| 13-15 | Pinky      | MCP, PIP, DIP joints    |

Relationship to handJoints3D

- handPose (48,): Joint rotations (how joints are oriented)
- handJoints3D (21, 3): Joint positions (where joints are located in 3D)
- handTrans (3,): Global hand translation

The MANO model uses handPose + handBeta + handTrans to generate the full hand mesh and compute handJoints3D.
![mano order](/joint_order.png)

### Evaluation Data Annotations
Evaluation pickle files contain limited information:

| Field | Shape | Description |
|-------|-------|-------------|
| `objTrans` | (3,) | Object translation |
| `objRot` | (3,) | Object rotation in Rodrigues representation |
| `handJoints3D` | (3,) | 3D location of root joint only |
| `handBoundingBox` | (4,) | 2D bounding box [topLeftX, topLeftY, bottomRightX, bottomRightY] |

## Data Loading

### Reading RGB Images
```python
from utils.vis_utils import read_RGB_img
img = read_RGB_img(base_dir, seq_name, file_id, split)
```

### Reading Depth Images
```python
from utils.vis_utils import read_depth_img
depth = read_depth_img(base_dir, seq_name, file_id, split)
```

### Reading Annotations
```python
from utils.vis_utils import read_annotation
annotation = read_annotation(base_dir, seq_name, file_id, split)
```

## Important Notes

⚠️ **Missing Annotations**: Some frames in train/evaluation folders do NOT contain annotations (fields set to 'None'). Only use frames listed in `train.txt` and `evaluation.txt`.

⚠️ **Coordinate System**: All annotations assume **OpenGL coordinate system** (hand/objects along negative z-axis in right-handed coordinate system with origin at camera center).

⚠️ **Image Format**: RGB images are in JPG format (changed from PNG in v2 due to storage constraints).

⚠️ **Depth Format**: 16-bit depth maps are stored in RGB format with LSB in red channel and MSB in green channel. Use `read_depth_img()` for proper decoding.

## Object Models
Download YCB object models from [PoseCNN project](https://rse-lab.cs.washington.edu/projects/posecnn/) and place in a `models/` folder.

## Multi-Camera Data (v3 only)
- Extrinsic camera parameters provided in `calibration/` folder
- Use `vis_pcl_all_cameras.py` to visualize point clouds from multiple cameras
- Manual annotations for 53 frames available in `manual_annotations/` folder

## File Lists
- **train.txt**: Contains paths to all training images in `<sequence_name>/<file_id>` format
- **evaluation.txt**: Contains paths to all evaluation images in `<sequence_name>/<file_id>` format

## Usage Example

```python
# Load a sequence
sequence_name = "ABF10"
frame_id = "0000"
split = "train"

# Read data
img = read_RGB_img(".", sequence_name, frame_id, split)
depth = read_depth_img(".", sequence_name, frame_id, split)
annotation = read_annotation(".", sequence_name, frame_id, split)

# Extract hand joints and object pose
hand_joints_3d = annotation['handJoints3D']  # (21, 3)
obj_translation = annotation['objTrans']      # (3,)
obj_rotation = annotation['objRot']          # (3,)
contact_mask = annotation['handVertContact'] # (778,)
```

## Citation
If using this dataset, please cite:

```bibtex
@INPROCEEDINGS{hampali2019honnotate,
    title={HOnnotate: A method for 3D Annotation of Hand and Object Poses},
    author={Shreyas Hampali and Mahdi Rad and Markus Oberweger and Vincent Lepetit},
    booktitle = {Proc. Computer Vision and Pattern Recognition (CVPR), IEEE},
    year={2020}
}
```

## License
The download and use of this dataset is for **academic research only**. It is free for researchers from educational or research institutes for non-commercial purposes. You agree not to redistribute, modify, or use commercially without express permission.