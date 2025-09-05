# MANO Parameters Explanation

## What is MANO?
MANO (hand Model with Articulated and Non-rigid defOrmations) is a parametric 3D hand model that represents hand shape and pose. It's based on the SMPL body model technology and is used to generate realistic 3D hand meshes.

## MANO Parameters

### 1. **fullpose** (shape: 48)
- Full hand pose parameters
- 48-dimensional vector representing:
  - Global rotation (3 params) 
  - 15 joints × 3 rotation parameters each = 45 params
  - Total: 3 + 45 = 48 parameters
- Controls the articulation/pose of all hand joints

### 2. **trans** (shape: 3)
- 3D translation vector [x, y, z]
- Positions the hand in 3D space
- Represents the global position of the hand root

### 3. **beta** (shape: 10)
- Hand shape parameters
- 10 PCA components controlling hand morphology
- Captures person-specific hand characteristics:
  - Hand size
  - Finger lengths
  - Palm width
  - Overall hand proportions

## Usage in the Code

The `forwardKinematics` function converts MANO parameters to:
1. **3D joint locations** (21 joints in hand skeleton)
2. **Hand mesh** (778 vertices forming the hand surface)

```python
def forwardKinematics(fullpose, trans, beta):
    m = load_model(MANO_MODEL_PATH, ncomps=6, flat_hand_mean=True)
    m.fullpose[:] = fullpose  # Set pose
    m.trans[:] = trans        # Set translation
    m.betas[:] = beta         # Set shape
    return m.J_transformed.r, m  # Returns joints and mesh
```

## Joint Mapping
The code uses `jointsMapManoToSimple` to reorder MANO joints from model order to a simple thumb-to-pinky order:
- Index 0: Wrist
- Indices 1-4: Thumb joints
- Indices 5-8: Index finger
- Indices 9-12: Middle finger  
- Indices 13-16: Ring finger
- Indices 17-20: Pinky finger

## Models
- **MANO_RIGHT.pkl**: Right hand model
- **MANO_LEFT.pkl**: Left hand model (with mirrored shape directions)