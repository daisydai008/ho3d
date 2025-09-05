# Code Style and Conventions

## Python Version Compatibility
- Supports both Python 2.7 and 3.x
- Uses `from __future__ import print_function, unicode_literals` for compatibility

## Code Organization
- Main scripts at root level (vis_HO3D.py, eval.py, pred.py, etc.)
- Utility functions in `utils/` directory
- Dataset stored in `HO3D_dataset/` (gitignored)

## Naming Conventions
- **Functions**: camelCase (e.g., `forwardKinematics`, `jointsMapManoToSimple`)
- **Variables**: camelCase for most variables (e.g., `baseDir`, `seqName`)
- **Constants**: UPPER_CASE (e.g., `MANO_MODEL_PATH`)
- **Classes**: PascalCase (e.g., `EvalUtil`)

## Documentation Style
- Triple-quoted docstrings for functions
- Brief parameter descriptions using `:param` notation
- Command-line tools use argparse with description strings

## File Structure
- Each main script is self-contained with `if __name__ == '__main__':` blocks
- Shared utilities abstracted to utils/ directory
- No apparent use of type hints (compatible with Python 2.7)