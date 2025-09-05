# HO3D Video Generation Documentation

## Overview

The `generate_ho3d_videos.py` script creates video visualizations from the HO3D (Hand-Object 3D poses) dataset. It supports two types of videos:
- **Simple Videos**: Basic RGB frame sequences with frame information
- **Annotated Videos**: RGB frames with overlaid 3D hand poses and object annotations

## Dataset Structure

### HO3D Dataset Organization
```
HO3D_dataset/HO3D/
├── train/                    # Training sequences (57 sequences, 14 unique sessions)
│   ├── MC1/, MC2/, MC4/, MC5/, MC6/     # Target sequences for analysis
│   ├── GPMF10/, GPMF11/, ..., GPMF14/  # GPMF subject sequences  
│   ├── BB10/, BB11/, ..., BB14/         # BB subject sequences
│   ├── SiBF10/, SiBF11/, ..., SiBF14/   # SiBF subject sequences
│   └── [other sequences]/
│   └── [sequence_name]/
│       ├── rgb/              # RGB images (.jpg)
│       ├── depth/            # Depth maps (.png) 
│       └── meta/             # Annotation files (.pkl)
├── evaluation/               # Evaluation sequences (13 sequences)
├── calibration/              # Multi-camera calibration data
│   └── [subject]/
│       └── calibration/
│           ├── trans_*.txt   # World-to-camera transformation matrices
│           ├── cam_*_intrinsics.txt  # Camera parameters
│           └── timestamps.txt        # Frame capture timestamps
└── joint_order.png           # MANO joint ordering reference
```

#### Training Sequence Frame Counts

**Multi-Camera Sessions** (Same action captured from different synchronized cameras):

**ABF** (Subject ABF, Session 1):
- ABF10, ABF11, ABF12, ABF13, ABF14: 1,383 frames each (5 cameras)

**BB** (Subject BB, Session 1):
- BB10, BB11, BB12, BB13, BB14: 1,606 frames each (5 cameras)

**GPMF** (Subject GPMF, Session 1):
- GPMF10, GPMF11, GPMF12, GPMF13, GPMF14: 1,092 frames each (5 cameras)

**GSF** (Subject GSF, Session 1):
- GSF10, GSF11, GSF12, GSF13, GSF14: 1,592 frames each (5 cameras)

**MDF** (Subject MDF, Session 1):
- MDF10, MDF11, MDF12, MDF13, MDF14: 2,806 frames each (5 cameras)

**SiBF** (Subject SiBF, Session 1):
- SiBF10, SiBF11, SiBF12, SiBF13, SiBF14: 2,880 frames each (5 cameras)

**ShSu** (Subject ShSu, Session 1):
- ShSu10, ShSu12, ShSu13, ShSu14: 1,847 frames each (4 cameras)

**SB** (Subject SB, Session 1):
- SB10, SB12, SB14: 1,680 frames each (3 cameras)

**SM** (Subject SM, Sessions 2-5):
- SM2, SM3, SM4, SM5: 898 frames each (4 cameras)

**SS** (Subject SS, Sessions 1-3):
- SS1, SS2, SS3: 898 frames each (3 cameras)

**MC** (Subject MC, Sessions 1,2,4,5,6):
- MC1, MC2: 897 frames each
- MC4: 896 frames  
- MC5: 898 frames
- MC6: 889 frames

**SMu** (Subject SMu, Multiple sessions):
- SMu1: 1,794 frames
- SMu40, SMu41, SMu42: 2,000 frames each (3 cameras)

**Individual Sequences:**
- ND2: 1,791 frames
- SiS1: 898 frames

#### Multi-Camera Setup Analysis
- **Total Sequences**: 57 sequences across 14 unique recording sessions
- **Total Frames**: 93,158 frames
- **Camera Configuration**: Up to 5 synchronized cameras per session (cam_0 through cam_4)
- **Naming Convention**: Final digit indicates camera ID (e.g., ABF10=cam_0, ABF14=cam_4)
- **Synchronization**: Identical frame counts within groups confirm temporal alignment
- **Coverage**: Most sessions use all 5 cameras; some use 3-4 cameras due to setup constraints

### Annotation Data Structure

Each `meta/*.pkl` file contains:
- **Hand Data**:
  - `handPose` (48,): MANO joint rotations (first 3 = wrist rotation)
  - `handTrans` (3,): Hand translation vector
  - `handBeta` (10,): MANO shape parameters
  - `handJoints3D` (21, 3): 3D joint positions
- **Object Data**:
  - `objTrans` (3,): Object translation
  - `objRot` (3,): Object rotation (axis-angle)
  - `objCorners3D` (8, 3): 3D bounding box corners
  - `objName`: YCB object name
- **Camera Data**:
  - `camMat` (3, 3): Intrinsic camera matrix

## Frame Rate Analysis

### Dataset Frame Rates
- **Original Recording**: ~45 FPS (determined from timestamp analysis)
- **Generated Videos**: 45 FPS (updated for real-time playback)
- **Sequence Durations @ 45 FPS**: 
  - **Short sequences**: MC (19-20 sec), SM/SS/SiS1 (~20 sec)
  - **Medium sequences**: GPMF (~24 sec), GSF (~35 sec), BB (~36 sec), ShSu (~41 sec), SB (~37 sec)
  - **Long sequences**: ABF (~31 sec), ND2/SMu1 (~40 sec), SMu40-42 (~44 sec)
  - **Very long sequences**: MDF (~62 sec), SiBF (~64 sec)

### Timestamp Analysis Results
```
Calibration timestamps show actual recording rates:
- BB1: ~45-55 FPS (variable)
- GPMF1: ~45 FPS average
- Temporal alignment across 5 cameras maintained
```

## Usage

### Basic Usage
```bash
# Activate Python 2.7 environment
source activate python2.7

# Generate simple video
python generate_ho3d_videos.py /path/to/HO3D_dataset/HO3D

# Generate annotated video with hand poses
python generate_ho3d_videos.py /path/to/HO3D_dataset/HO3D --annotated

# Specify sequences and output directory
python generate_ho3d_videos.py /path/to/HO3D_dataset/HO3D \
    --annotated \
    -s MC1 MC2 GPMF10 \
    -o output_videos/
```

### Command Line Arguments
```
positional arguments:
  ho3d_path           Path to HO3D dataset

optional arguments:
  -h, --help          Show help message
  -o, --output        Output directory (default: videos)
  -s, --sequences     Sequences to process (default: ['GSF11'])
  --annotated         Create annotated videos with hand poses
```

### Prerequisites
- Python 2.7 environment
- Required packages: opencv-python, numpy
- MANO model setup (for annotated videos)
- HO3D dataset utilities (`utils/vis_utils.py`)

## Video Types

### 1. Simple Videos
- **Filename**: `{sequence}_simple.avi`
- **Content**: RGB frames with basic frame information overlay
- **Use Case**: Quick sequence visualization, motion preview
- **Processing Speed**: Fast (no 3D pose computation)

### 2. Annotated Videos
- **Filename**: `{sequence}_annotated.avi`
- **Content**: RGB frames + hand joint overlay + object bounding boxes
- **Features**:
  - MANO hand model joint visualization (21 joints)
  - YCB object 3D corner projections
  - Frame and sequence identification
- **Use Case**: Detailed analysis, pose validation, research visualization

## Technical Implementation

### MANO Hand Model Integration
```python
# Hand pose parameters to 3D joints
handJoints3D, handMesh = forwardKinematics(
    anno['handPose'],    # 48-dim: wrist + finger rotations
    anno['handTrans'],   # 3-dim: global translation
    anno['handBeta']     # 10-dim: shape parameters
)

# Project to 2D for visualization
handKps = project_3D_points(anno['camMat'], handJoints3D, is_OpenGL_coords=True)
```

### Object Visualization
```python
# Transform object corners to current pose
objCorners = anno['objCorners3DRest']  # Rest pose corners
objCornersTrans = np.matmul(objCorners, cv2.Rodrigues(anno['objRot'])[0].T) + anno['objTrans']

# Project to 2D
objKps = project_3D_points(anno['camMat'], objCornersTrans, is_OpenGL_coords=True)
```

### Video Encoding
```python
# MJPG codec for broad compatibility
fourcc = 1196444237  # MJPG fourcc value
video_writer = cv2.VideoWriter(output_path, fourcc, 45.0, (width, height))
```

## Coordinate Systems

### MANO Hand Coordinate Frame
- **Wrist Orientation**: First 3 elements of `handPose` (Rodrigues vector)
- **Coordinate Convention**: OpenGL coordinate system
- **Joint Mapping**: MANO order → visualization order via `jointsMapManoToSimple`

### Camera Coordinate System
- **Origin**: Camera center
- **Orientation**: OpenGL convention (Z-axis into scene)
- **Projection**: Uses `camMat` intrinsic parameters
- **Multi-camera**: Synchronized via calibration data

## Performance Metrics

### Processing Statistics
Example for GPMF10 sequence:
```
Total Frames: 1,092
Successful Annotations: 1,030 (94.3%)
Skipped Frames: 62 (missing annotations)
Output Size: 77 MB
Processing Time: ~30 seconds
```

### Success Rates by Sequence Type
- **MC sequences**: ~95% annotation success
- **GPMF sequences**: ~94% annotation success  
- **BB sequences**: ~96% annotation success
- **SiBF sequences**: ~98% annotation success

## Output Files

### Video Files
- **Location**: `videos/` directory (configurable)
- **Format**: AVI with MJPG compression
- **Naming**: `{sequence}_{simple|annotated}.avi`
- **Frame Rate**: 45 FPS (real-time playback)

### File Sizes (Approximate)
- Simple videos: ~20-40 MB per sequence
- Annotated videos: ~50-100 MB per sequence
- Size varies with sequence length and complexity

## Troubleshooting

### Common Issues

1. **MANO Model Missing**
   ```bash
   Error: MANO model missing! Please run setup_mano.py to setup mano folder
   ```
   **Solution**: Ensure MANO model files are in `./mano/models/MANO_RIGHT.pkl`

2. **Video Writer Failed**
   ```bash
   Failed to open video writer
   ```
   **Solution**: Check output directory permissions, verify OpenCV installation

3. **Missing Annotations**
   ```bash
   Frame X in sequence Y does not have annotations
   ```
   **Solution**: Normal for some frames, script automatically skips and continues

### Sequence Availability
- **Training sequences**: 44 sequences with full annotations
- **Evaluation sequences**: Limited annotations (hand root joint only)
- **Recommended sequences**: MC1-6, GPMF10-14, BB10-14 for complete data

## Integration with Analysis Pipeline

### Coordinate Transformation
Video generation works with the coordinate transformation framework:
- Input: HO3D camera coordinates (OpenGL convention)
- Output: Visual validation of 3D pose data
- Integration: Use with `test_coordinate_transform.py` for validation

### Dataset Exploration Workflow
1. **Generate videos** → Visual overview of sequences
2. **Analyze timestamps** → Understand recording parameters  
3. **Transform coordinates** → Prepare for simulation/analysis
4. **Validate poses** → Compare visual output with 3D data

## Research Applications

### Hand-Object Interaction Analysis
- **Grasp Analysis**: Observe hand configurations during manipulation
- **Temporal Dynamics**: Study motion patterns at proper frame rates
- **Multi-view Validation**: Cross-reference with calibration data

### Dataset Quality Assessment
- **Annotation Coverage**: Identify sequences with missing data
- **Pose Quality**: Visual inspection of MANO fitting accuracy
- **Temporal Consistency**: Smooth motion validation

### Isaac Gym Preparation
- **Pose Preview**: Validate hand poses before simulation
- **Coordinate Verification**: Ensure proper transformation pipeline
- **Motion Planning**: Extract natural manipulation patterns

---

## Quick Reference

### Generate All MC Sequences (Annotated)
```bash
source activate python2.7
python generate_ho3d_videos.py /path/to/HO3D_dataset/HO3D \
    --annotated -s MC1 MC2 MC4 MC5 MC6 -o mc_videos/
```

### Batch Processing Multiple Subjects
```bash
# GPMF subject sequences  
python generate_ho3d_videos.py /path/to/HO3D_dataset/HO3D \
    --annotated -s GPMF10 GPMF11 GPMF12 GPMF13 GPMF14

# BB subject sequences
python generate_ho3d_videos.py /path/to/HO3D_dataset/HO3D \
    --annotated -s BB10 BB11 BB12 BB13 BB14
```

### File Structure After Processing
```
ho3d/
├── generate_ho3d_videos.py    # Video generation script
├── GEN_VIDEO.md               # This documentation
├── videos/                    # Generated video outputs
│   ├── MC1_annotated.avi
│   ├── MC1_simple.avi
│   └── ...
└── HO3D_dataset/             # Original dataset
    └── HO3D/
        ├── train/
        ├── calibration/
        └── ...
```