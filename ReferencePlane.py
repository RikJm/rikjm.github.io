import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel

# Loads the sequence function
def loadFile():
    textureFile = cmds.fileDialog2(cap='Select the first sequence file', fm=1)
    return textureFile

def checkUnits(units):
    
    cu=cmds.currentUnit( query=True, linear=True )
    if cu!=units :
        cmds.currentUnit( linear=units )
    else:
        pass
    return cu
    
# Checks if we already have a refPlane
def create():
       
    if cmds.objExists("RefShader"):       
        cmds.warning( "A reference already exists, deleting..." )
        cmds.delete("RefPlane_grp")
        cmds.delete("RefShader")
        cmds.delete("ReferenceFile")
        cmds.delete("RefFilePlacement")
        cmds.delete("RefShaderSG")
     
    else:        
        cu=checkUnits('cm')
        pyMaterial, pyShadingGroup, pyTexture = createRefShader()
        refPlane, refPlaneOffset =createPlane()
        KeysCTRL, LinearCTRL, refPlaneCTRL, refPlan_grp = createCTRLs()
        pyCondition=createCondition()
        cmds.parent(refPlaneOffset,refPlan_grp.name())
        cmds.sets(refPlane, e=True, forceElement= pyShadingGroup )
        pm.connectAttr(pyMaterial.outColor, pyShadingGroup +".surfaceShader")

        createConnections(refPlaneCTRL, refPlaneOffset, 't', 't')
        createConnections(refPlaneCTRL, refPlaneOffset, 'r', 'r')
        createConnections(refPlaneCTRL, refPlaneOffset, 's', 's')
        createConnections(refPlaneCTRL, refPlaneOffset, 'Visibility','visibility')
        createConnections(refPlaneCTRL, KeysCTRL, 'Visibility','visibility')
        createConnections(refPlaneCTRL, LinearCTRL, 'Visibility','visibility')
        createConnections(LinearCTRL, refPlaneCTRL, 'Frame','Frame')
        createConnections(KeysCTRL, refPlaneCTRL, 'Keys','Keys')
        pyCondition.setAttr('firstTerm',1)
        createConnections(refPlaneCTRL, pyCondition, 'Mode','secondTerm')
        createConnections(refPlaneCTRL, pyCondition, 'Frame','colorIfFalseR')
        createConnections(refPlaneCTRL, pyCondition, 'Keys','colorIfTrueR')
        createConnections(pyCondition, pyTexture, 'outColorR','frameExtension')

        pm.select (pyTexture, r=1)
        checkUnits(cu)

# Shader creator function #
def createRefShader():
    ## It will load the file and place it as a texture ##
    ## Will also make the file use frameExtension ## 
    textureFile=loadFile()
    cmds.warning( "Reference Plane Created.")
    pyRefPlane = pm.shadingNode("lambert", asShader=True, name="RefShader")
    pyTexture = pm.shadingNode("file", asTexture=True, name="ReferenceFile")
    pyPlace2D = pm.shadingNode ("place2dTexture", asUtility=True, name="RefFilePlacement")
    pyShadingGroup = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name= pyRefPlane + 'SG' )
    pm.connectAttr (pyTexture.outColor, pyRefPlane.color)
    pm.connectAttr (pyPlace2D.coverage, pyTexture.coverage)
    pm.connectAttr (pyPlace2D.translateFrame, pyTexture.translateFrame)
    pm.connectAttr (pyPlace2D.rotateFrame, pyTexture.rotateFrame)
    pm.connectAttr (pyPlace2D.mirrorU, pyTexture.mirrorU)
    pm.connectAttr (pyPlace2D.mirrorV, pyTexture.mirrorV)
    pm.connectAttr (pyPlace2D.stagger, pyTexture.stagger)
    pm.connectAttr (pyPlace2D.wrapU, pyTexture.wrapU)
    pm.connectAttr (pyPlace2D.wrapV, pyTexture.wrapV)
    pm.connectAttr (pyPlace2D.repeatUV, pyTexture.repeatUV)
    pm.connectAttr (pyPlace2D.offset, pyTexture.offset)
    pm.connectAttr (pyPlace2D.rotateUV, pyTexture.rotateUV)
    pm.connectAttr (pyPlace2D.noiseUV, pyTexture.noiseUV)
    pm.connectAttr (pyPlace2D.vertexUvOne, pyTexture.vertexUvOne)
    pm.connectAttr (pyPlace2D.vertexUvTwo, pyTexture.vertexUvTwo)
    pm.connectAttr (pyPlace2D.vertexUvThree, pyTexture.vertexUvThree)
    pm.connectAttr (pyPlace2D.vertexCameraOne, pyTexture.vertexCameraOne)
    cmds.setAttr(str(pyTexture.fileTextureName),textureFile[0], type="string")
    pm.setAttr (pyTexture.useFrameExtension, 1)
    return(pyRefPlane, pyShadingGroup,pyTexture)
    
# Create an empty Group
def createNull():
    pyNull = pm.nt.Transform()
    return pyNull

# Create a PolyPlane # 
def createPlane():
    
    pyPolyPlane = pm.polyPlane(name='RefPlane')
    pyPolyPlane[0].setAttr('rx', 90)
    pyPolyPlane[0].setAttr('sx', 128)
    pyPolyPlane[0].setAttr('sz', 72)
    cmds.makeIdentity(pyPolyPlane[0].name(),apply=True, t=1, r=1, s=1, n=0)
    nullOffset=createNull()
    nullOffset.rename('RefPlaneOffset')
    cmds.parent(pyPolyPlane[0].name(), nullOffset.name())
    
    return (pyPolyPlane[0].name(), nullOffset.name())

# Create the Controls
def createCTRLs():
    
    #Main Control
    RefPlaneCTRL=createNull()
    RefPlaneCTRL.rename('RefPlaneCTRL')
    RefPlan_grp=createNull()
    RefPlan_grp.rename('RefPlane_grp')
    cmds.parent(RefPlaneCTRL.name(), RefPlan_grp.name())
    createShape(RefPlaneCTRL,createCross(),17)
    RefPlaneCTRL.addAttr('Frame',defaultValue=0, minValue=0, attributeType='long', h=False, k=True)
    RefPlaneCTRL.addAttr('Keys',defaultValue=0, minValue=0, attributeType='long', h=False, k=True)  
    RefPlaneCTRL.addAttr('Mode',attributeType='enum', h=False, k=True, enumName=("Linear:Stepped"))
    lockChannel(RefPlaneCTRL,'visibility')
    RefPlaneCTRL.addAttr('Visibility',attributeType='bool', defaultValue=True, h=False, k=True)
    
    #Keys Control
    KeysCTRL=createNull()
    KeysCTRL.rename('KeysCTRL')
    KeysCTRL.setAttr('tx',72)
    KeysCTRL.setAttr('ty', 3)
    cmds.makeIdentity(KeysCTRL.name(),apply=True, t=1, r=1, s=1, n=0)
    cmds.parent(KeysCTRL.name(), RefPlaneCTRL.name())
    createShape(KeysCTRL,createBulb(),13)
    lockChannels(KeysCTRL)
    KeysCTRL.addAttr('Keys',defaultValue=0, minValue=0, attributeType='long', h=False, k=True)
    
    #Linear Control
    LinearCTRL=createNull()
    LinearCTRL.rename('LinearCTRL')
    LinearCTRL.setAttr('tx',-72)
    LinearCTRL.setAttr('ty', 3)
    cmds.makeIdentity(LinearCTRL.name(),apply=True, t=1, r=1, s=1, n=0)
    cmds.parent(LinearCTRL.name(), RefPlaneCTRL.name())
    createShape(LinearCTRL,createBulb(),14)
    lockChannels(LinearCTRL)
    LinearCTRL.addAttr('Frame',defaultValue=0, minValue=0, attributeType='long', h=False, k=True)   

    
    return (KeysCTRL,LinearCTRL,RefPlaneCTRL,RefPlan_grp)
    
# Parents a shape node to it's controller
def createShape(ctrl, shapeNodes,color):

    cmds.setAttr(str(shapeNodes[1][0])+".overrideEnabled",1)
    cmds.setAttr(str(shapeNodes[1][0])+".overrideColor",color)
    shapeNodes[0].attr('scaleX').set(5)
    shapeNodes[0].attr('scaleY').set(5)
    shapeNodes[0].attr('scaleZ').set(5)
    cmds.delete(cmds.pointConstraint( ctrl.name(), shapeNodes[0].name(), o=(0,0,0), w=.1 ))
    cmds.delete(cmds.orientConstraint( ctrl.name(), shapeNodes[0].name(), o=(0,0,0), w=.1 ))
    cmds.makeIdentity(shapeNodes[0].name(),apply=True, t=1, r=1, s=1, n=0)
    cmds.rename(shapeNodes[1], (ctrl.name()+'Shape'))
    cmds.parent((ctrl.name()+'Shape'), ctrl.name(),a=True, s=True)
    transform=cmds.listRelatives(ctrl.name()+'Shape', p=True)
    cmds.makeIdentity(transform[0],apply=True, t=1, r=1, s=1, n=0)
    cmds.parent((ctrl.name()+'Shape'),ctrl.name(),r=True, s=True)
    cmds.delete(transform[0])
    cmds.delete(str(shapeNodes[0]))
        
    
# Create a BulbShape #
def createBulb():
    
    ## Original code borrowed from the comet scripts, Michael B. Comet ##
    ## http://www.comet-cartoons.com/melscript.php ##
    
    pyCurve= pm.curve(p=[(0.139471,-0.798108,0),(-0.139471,-0.798108,0),(-0.139471,-0.798108,0),(-0.299681,-0.672294,0),(-0.299681,-0.672294,0),
            (-0.299681,-0.672294,0),(-0.121956,-0.578864,0),(-0.121956,-0.578864,0),(-0.121956,-0.578864,0),(-0.285304,-0.51952,0),(-0.285304,-0.51952,0),(-0.0744873,-0.442806,0),
            (-0.0744873,-0.442806,0),(-0.287769,-0.373086,0),(-0.287769,-0.373086,0),(-0.100386,-0.296549,0),(-0.100386,-0.296549,0),(-0.264344,-0.205725,0),(-0.264344,-0.205725,0),
            (-0.262544,-0.0993145,0),(-0.262544,-0.0993145,0),(-0.167051,-0.0613459,0),(-0.167051,-0.0613459,0),(-0.167051,-0.0613459,0),(-0.166024,0.0163458,0),(-0.157394,0.232092,0),
            (-0.367902,0.680843,0),(-0.96336,1.224522,0),(-1.006509,1.992577,0),(-0.316123,2.613925,0),(0.561786,2.548479,0),(1.094888,2.001207,0),(1.051638,1.166965,0),(0.436419,0.66543,0),
            (0.13283,0.232092,0),(0.15009,0.0163458,0),(0.15073,-0.046628,0),(0.15073,-0.046628,0),(0.270326,-0.0955798,0),(0.270326,-0.0955798,0),(0.267815,-0.208156,0),(0.267815,-0.208156,0),
            (0.0884224,-0.291145,0),(0.0884224,-0.291145,0),(0.292477,-0.366091,0),(0.292477,-0.366091,0),(0.0946189,-0.439723,0),(0.0946189,-0.439723,0),(0.306664,-0.508968,0),(0.306664,-0.508968,0),
            (0.112488,-0.57513,0),(0.112488,-0.57513,0),(0.323789,-0.674644,0),(0.323789,-0.674644,0),(0.152097,-0.794645,0),(0.152097,-0.794645,0),(0.152097,-0.794645,0),(0.106716,-0.907397,0),
            (0.0103741,-1.003739,0),(-0.0919896,-0.907397,0),(-0.139471,-0.798108,0),(-0.139471,-0.798108,0)], 
            k=[0,0,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,59,59])
    shape=cmds.listRelatives(pyCurve.name())
    
    return (pyCurve,shape)
    
# Create a CrossShape #
def createCross():
    ## Original code borrowed from the comet scripts, Michael B. Comet ##
    ## http://www.comet-cartoons.com/melscript.php ##    
    pyCurve=pm.curve(d=1,p=[(1,0,-1),(2,0,-1),(2,0,1),(1,0,1),(1,0,2),(-1,0,2),(-1,0,1),(-2,0,1),(-2,0,-1),(-1,0,-1),(-1,0,-2),(1,0,-2),(1,0,-1)],
                     k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    shape=cmds.listRelatives(pyCurve.name())
    pyCurve.setAttr('rx',90)
    pyCurve.attr('scaleX').set(.7)
    pyCurve.attr('scaleY').set(.7)
    pyCurve.attr('scaleZ').set(.7)
    pyCurve.setAttr('translateY',12)     
    cmds.move(0,0,0, pyCurve.name() + '.scalePivot', a=True)
    cmds.makeIdentity(pyCurve.name(),apply=True, t=1, r=1, s=1, n=0)

    return (pyCurve,shape)

# Create condition Node
def createCondition():
    pyCondition=pm.shadingNode("condition", asUtility=True, name="KeysOrLinear_Condition")
    return pyCondition
    
# LockAllChannels    
def lockChannels(node):
    channels=["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ", "scaleX", "scaleY", "scaleZ","visibility"]
    for channel in channels:
        node.setAttr(channel,keyable=False,lock=False)
        
# LockOneChannel            
def lockChannel(node,channel):
    node.setAttr(channel,keyable=False,lock=False)       

def createConnections(node1, node2, attribute1, attribute2):
    cmds.connectAttr( node1+'.'+attribute1, node2+'.'+attribute2)
                    


