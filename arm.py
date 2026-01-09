import maya.cmds as cmds

class ArmModule:
    def __init__(self, side = "L"):
        self.side = side

        self.shoulder_guide = f"shoulder_{self.side}_GUIDE"
        self.elbow_guide = f"elbow_{self.side}_GUIDE"
        self.wrist_guide = f"wrist_{self.side}_GUIDE"


    def create_guides(self):

        #Set Location
        if self.side == "L":
            multiplier = 1
        else:
            multiplier = -1

        #Standard Positions
        shoulder_pos = (2 * multiplier, 15, 0)
        elbow_pos = (5 * multiplier, 15, -0.5) #For IK, placed a little bit back
        wrist_pos = (8 * multiplier, 15, 0)

        #Generate Locator
        #If it already exists, delete and make a new one
        for g in [self.shoulder_guide, self.elbow_guide, self.wrist_guide]:
            if cmds.objExists(g):
                cmds.delets(g)

        cmds.spaceLocator(n=self.shoulder_guide)
        cmds.xform(self.shoulder_guide, t=shoulder_pos)

        cmds.spaceLocator(n=self.elbow_guide)
        cmds.xform(self.elbow_guid, t=elbow_pos)

        cmds.spaceLocator(n=self.wrist_guide)
        cmds.xform(self.wrist_guide, t=wrist_pos)

        #Connect Hierarchy
        cmds.parent(self.wrist_guide, self.elbow_guide)
        cmds.parent(self.elbow_guide, self.shoulder_guide)

        print(f"--- {self.side} Arm Guides created successfully ---")



if __name__ == "__main__":
    left_Arm = ArmModule(side = "L")
    left_Arm.create_guides()

    right_Arm = ArmModule(side = "R")
    right_Arm.create_guides()