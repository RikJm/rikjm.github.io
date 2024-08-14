import maya.cmds as cmds
import maya.mel

playing=False

if (cmds.play( q=True, state=True )) :
    cmds.playbackOptions( loop='continuous' )
    cmds.playbackOptions( minTime=min, maxTime=max )
    cmds.play( state=False )
    
else:
    min=(cmds.playbackOptions(q=True, min=True))
    max=(cmds.playbackOptions(q=True, max=True))
    
    playbackSlider=maya.mel.eval('$tmpVar=$gPlayBackSlider')
    range=str(cmds.timeControl(playbackSlider,q=True,rng=True))
    
    strings =range.partition(':')
    
    print strings
    print strings[0]
    print type(strings[0])
    
    start=strings[0].split('"')
    end=strings[2].split('"')
    print start
    firstFrame = float (start[1])
    lastFrame = float(end[0])
    print firstFrame
    print lastFrame
    a = (lastFrame-firstFrame)
    print a
    
    
    if (a>1):
        cmds.playbackOptions( loop='continuous' )
        cmds.playbackOptions( minTime=firstFrame, maxTime=lastFrame )
        playing=1
        cmds.play( forward=True )
    else:
        cmds.play( forward=True )
        