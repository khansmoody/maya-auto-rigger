# Maya Auto-Rigger Project
Modular Auto-Rigging system to promote animation pipeline efficiency.

## Current Progress
- [x] **Guide System**: Real-time locator generation for joint positioning.
- [x] **Mirroring Logic**: Symmetrical guide placement using $x \to -x$ coordinate transformation.
- [x] **Skeleton Build**: Automated joint creation with standard orientation (XYZ) and preferred angle settings.
- [ ] **FK/IK Controller System**: NURBS-based control rig (Coming Soon).
- [ ] **UI Implementation**: PySide6/Qt-based user interface (Coming Soon).

## Usage (Pre-UI Phase)
Since the UI is currently in development, follow these steps in the Maya Script Editor (Python):

1. **Import and Initialize**: Run the script to load the `ArmModule` class.
2. **Generate Guides**: 
   ```python
   left_arm = ArmModule(side="L")
   left_arm.create_guides()
3. **Manual Adjustment**: Move the locators in the viewport to match the character's mesh.
4. **Mirroring**: Synchronize the right side based on the left side's position.
   ```python
   left_arm.mirror_guides()
5. **Build Skeleton**: Generate the final joint hierarchy.
   ```python
   left_arm.create_joints()
   right_arm.create_joints()

## Technical Challenges & Solutions
- Maya 2025 Compatibility: Fixed a TypeError by replacing the invalid pa flag with spa(setPreferredAngle) to ensure stability in Python 3.
- Dynamic Querying: Used cmds.xform in query mode to retrieve real-time world coordinates, allowing the script to build joints regardless of where the user moves the guides.
