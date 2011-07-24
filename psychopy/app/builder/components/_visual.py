# Part of the PsychoPy library
# Copyright (C) 2011 Jonathan Peirce
# Distributed under the terms of the GNU General Public License (GPL).

import _base
from os import path
from psychopy.app.builder.experiment import Param

class VisualComponent(_base.BaseComponent):
    """Base class for most visual stimuli
    """
    def __init__(self, parentName, name='', units='window units', color='$[1,1,1]',
        pos=[0,0], size=[0,0], ori=0 , colorSpace='rgb',
        startType='time (s)',startVal='',stopType='duration (s)', stopVal=''):
        self.psychopyLibs=['visual']#needs this psychopy lib to operate
        self.order=[]#make sure these are at top (after name and time params)
        self.params={}
        self.params['startType']=Param(startType, valType='str', 
            allowedVals=['time (s)', 'frame N', 'condition'],
            hint="How do you want to define your start point?")
        self.params['stopType']=Param(stopType, valType='str', 
            allowedVals=['duration (s)', 'duration (frames)', 'time (s)', 'frame N', 'condition'],
            hint="How do you want to define your end point?")
        self.params['startVal']=Param(startVal, valType='code', allowedTypes=[],
            hint="When does the stimulus start?")
        self.params['stopVal']=Param(stopVal, valType='code', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint="When does the stimulus end?")
        self.params['name']=Param(name,  valType='code', updates='constant', 
            hint="Name of this stimulus")
        self.params['units']=Param(units, valType='str', allowedVals=['window units', 'deg', 'cm', 'pix', 'norm'],
            hint="Units of dimensions for this stimulus")
        self.params['color']=Param(color, valType='str', allowedTypes=[],
            updates='constant', allowedUpdates=['constant','set every repeat','set every frame'],
            hint="Color of this stimulus (e.g. $[1,1,0], red ); Right-click to bring up a color-picker (rgb only)")
        self.params['colorSpace']=Param(colorSpace, valType='str', allowedVals=['rgb','dkl','lms'],
            updates='constant', allowedUpdates=['constant'],
            hint="Choice of color space for the color (rgb, dkl, lms)")
        self.params['pos']=Param(pos, valType='code', allowedTypes=[],
            updates='constant', allowedUpdates=['constant','set every repeat','set every frame'],
            hint="Position of this stimulus (e.g. [1,2] ")
        self.params['size']=Param(size, valType='code', allowedTypes=[],
            updates='constant', allowedUpdates=['constant','set every repeat','set every frame'],
            hint="Size of this stimulus (either a single value or x,y pair, e.g. 2.5, [1,2] ")
        self.params['ori']=Param(ori, valType='code', allowedTypes=[],
            updates='constant', allowedUpdates=['constant','set every repeat','set every frame'],
            hint="Orientation of this stimulus (in deg)")
    def writeFrameCode(self,buff):
        """Write the code that will be called every frame
        """
        self.writeStartTestCode(buff)#writes an if statement to determine whether to draw etc
        buff.writeIndented("%(name)s.autoDraw(True)\n" %(self.params))
        buff.setIndentLevel(-1, relative=True)#to get out of the if statement
        self.writeStopTestCode(buff)#writes an if statement to determine whether to draw etc
        buff.writeIndented("%(name)s.autoDraw(False)\n" %(self.params))
        buff.setIndentLevel(-1, relative=True)#to get out of the if statement
        #set parameters that need updating every frame
        if checkNeedToUpdate('set every frame'):#this method inherited from _base
            buff.writeIndented("if %(name)s.status==STARTED:#only update if being drawn\n" %(self.params))
            buff.setIndentLevel(+1, relative=True)#to enter the if block
            self.writeParamUpdates(buff, 'set every frame')
            buff.setIndentLevel(+1, relative=True)#to exit the if block
    def writeParamUpdates(self, buff, updateType):
        """Write updates to the buffer for each parameter that needs it
        updateType can be 'experiment', 'routine' or 'frame'
        """
        for thisParamName in self.params.keys():
            thisParam=self.params[thisParamName]
            #capitalise params
            if thisParamName=='advancedParams':
                continue
            elif thisParamName=='letterHeight':
                paramCaps='Height' #setHeight for TextStim
            elif thisParamName=='image':
                paramCaps='Tex' #setTex for PatchStim
            elif thisParamName=='sf':
                paramCaps='SF' #setSF, not SetSf
            else:
                paramCaps = thisParamName.capitalize()
            #color is slightly special
            if thisParam.updates==updateType:
                if thisParamName=='color':
                    buff.writeIndented("%(name)s.setColor(%(color)s, colorSpace=%(colorSpace)s)\n" %(self.params))
                else: buff.writeIndented("%s.set%s(%s)\n" %(self.params['name'], paramCaps, thisParam)) 

