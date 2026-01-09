import maya.cmds as cmds

class ArmModule:
    def __init__(self, side = "L"):
        self.side = side

        self.shoulder_guide = f"shoulder_{self.side}_GUIDE"
        self.elbow_guide = f"elbow_{self.side}_GUIDE"
        self.wrist_guide = f"wrist_{self.side}_GUIDE"



    def create_guides(self):
        """
        Generate guides for arm.
        :return:
        """

        #Set Location
        if self.side == "L":
            multiplier = 1
        else:
            multiplier = -1

        #Standard Positions
        shoulder_pos = (15 * multiplier, 150, 0)
        elbow_pos = (40 * multiplier, 150, -5) #For IK, placed a little bit back
        wrist_pos = (65 * multiplier, 150, 0)

        #Generate Locator
        #If it already exists, delete and make a new one
        for g in [self.shoulder_guide, self.elbow_guide, self.wrist_guide]:
            if cmds.objExists(g):
                cmds.delete(g)

        guides = [self.shoulder_guide, self.elbow_guide, self.wrist_guide]
        positions = [shoulder_pos, elbow_pos, wrist_pos]

        for g,p in zip(guides, positions):
            cmds.spaceLocator(n=g)
            cmds.xform(g, t=p)

        #Connect Hierarchy
        cmds.parent(self.wrist_guide, self.elbow_guide)
        cmds.parent(self.elbow_guide, self.shoulder_guide)

        print(f"--- {self.side} Arm Guides created successfully ---")



    def mirror_guides(self):
        """
        Mirror guides for arm. (L guides -> R guides)
        """

        l_guides = [f"shoulder_L_GUIDE", f"elbow_L_GUIDE", f"wrist_L_GUIDE"]
        r_guides = [f"shoulder_R_GUIDE", f"elbow_R_GUIDE", f"wrist_R_GUIDE"]

        for l_g, r_g in zip(l_guides, r_guides):
            if cmds.objExists(l_g) and cmds.objExists(r_g):
                pos = cmds.xform(l_g, q=True, t=True, ws=True)
                mirrored_pos = [pos[0] * -1, pos[1], pos[2]]
                cmds.xform(r_g, ws=True, t=True, p=mirrored_pos)

        print(f"--- Left to Right Guides mirrored successfully ---")


    def create_joints(self):
        """
        Bring current location of guides and Generate joints.
        """

        # 1. Check if guides or joints are already exist
        guides = [self.shoulder_guide, self.elbow_guide, self.wrist_guide]
        for g in guides:
            if not cmds.objExists(g):
                cmds.error(f"Guide {g} does not exist")
                return

        jnt_names = [f"shoulder_{self.side}_JNT", f"elbow_{self.side}_JNT", f"wrist_{self.side}_JNT"]
        for j in jnt_names:
            if not cmds.objExists(j):
                cmds.delete(j)

        # 2. Read realtime world coordinates of guides
        shoulder_pos = cmds.xform(self.shoulder_guide, q=True, t=True, ws=True)
        elbow_pos = cmds.xform(self.elbow_guide, q=True, t=True, ws=True)
        wrist_pos = cmds.xform(self.wrist_guide, q=True, t=True, ws=True)

        # 3. Generate joints
        cmds.select(cl=True)
        shoulder_jnt = cmds.joint(p=shoulder_pos, n=f"shoulder_{self.side}_JNT", rad=2)
        elbow_jnt = cmds.joint(p=elbow_pos, n=f"elbow_{self.side}_JNT", rad=2)
        wrist_jnt = cmds.joint(p=wrist_pos, n=f"wrist_{self.side}_JNT", rad=2)

        # 4. Joint Orient line up (important)
        cmds.joint(shoulder_jnt, e=True, zso=True, oj="xyz", secondaryAxisOrient="yup")
        cmds.joint(elbow_jnt, e=True, zso=True, oj="xyz", secondaryAxisOrient="yup")
        # wrist joint(end joint) has to follow parent's orient or set as 0
        cmds.setAttr(f"{wrist_jnt}.jointOrient", 0, 0, 0)

        # 5. Set preferred angle
        cmds.joint(elbow_jnt, e=True, pa=True)

        print(f"--- {self.side} Arm Joints created successfully ---")

if __name__ == "__main__":
    left_Arm = ArmModule(side = "L")
    left_Arm.create_guides()

    right_Arm = ArmModule(side = "R")
    right_Arm.create_guides()