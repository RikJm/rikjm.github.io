import maya.cmds as cmds

ctrls=cmds.ls( selection=True)

def zeroRotTrans(ctrls):
    for ctrl in ctrls:
        attrs=['tx','ty', 'tz', 'rx', 'ry', 'rz']
        for attr in attrs:
            default=cmds.attributeQuery(attr,node=ctrl, ld=True)
            try:
                cmds.setAttr(ctrl+'.'+attr,default[0])
            except:
                pass

zeroRotTrans(ctrls)