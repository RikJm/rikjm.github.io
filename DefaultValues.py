import maya.cmds as cmds

ctrls=cmds.ls( selection=True)

def zeroSelected(ctrls):
    for ctrl in ctrls:
        attrs=cmds.listAttr(ctrl,u=True, k=True)
        for attr in attrs:
            default=cmds.attributeQuery(attr,node=ctrl, ld=True)
            cmds.setAttr(ctrl+'.'+attr,default[0])

zeroSelected(ctrls)