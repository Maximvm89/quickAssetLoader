'''
Name: quickAssetLoader.assetToPath
Author: Marco Parisi 
Date: 04/13/2019
Version: 0.0


DESCRIPTION
---------------
The point of this class is to gather the asset name from quickAssetLoaderUI
and trasform it on the actual file system path
Due the fact those methods rely so much on the Naming Convetions that differs from studio to studio,
the methods are empty and need to be implemented in order to find the real assets in the file system.

'''
import maya.cmds as cmds
import maya.mel as mel

import os
import glob

import environment.environment as environment



class assetToPath(object):
    
    assetName = []
    assetPath = None
    filesInAssetPath = []

    def __init__(self):
        """
        Init method, use to initialize variables

        """
        
        pass


    def getAssetPath(self):
        """
        Return the path of the asset loaded

        :rtype: None
        """
        if self.assetPath is not None:
            return self.assetPath

    def getFilesInAssetDir(self):
        """
        Return the path of the asset loaded

        :rtype: None
        """
        if self.assetPath is not None:
            return self.filesInAssetPath

    
    def setTheAsset(self, assetName):
        """
        This method should be used to get the asset Name from quickAssetLoaderUI
        and try to find the actual file in the filesystem
        
        :type assetName: str
        :rtype: bool
        """
        pass

    def openIt(self):
        
        """
        Open the file in maya without reference it
       
        """
        pass

            
    def reference(self, path):
        """
        Helper method used to reference the current loaded asset using the given path
        :type path: str
        """
        pass
            
    def referenceIt(self):
        """
        Open the file in maya without reference it
       
        """
        pass


    
    #CHAR 1
    def char1Button(self):
        """
        Helper method used to load a specif asset frequently used
        """
        pass
    #CHAR 2
    def char2Button(self):
        """
        Helper method used to load a specif asset frequently used
        """
        pass
    #CHAR 3
    def char3Button(self):
        """
        Helper method used to load a specif asset frequently used
        """
        pass
    #CHAR 4
    def char4Button(self):
        """
        Helper method used to load a specif asset frequently used
        """
        pass




if __name__ == "__main__":
    
    #Testing Purpose
    aToP = assetToPath()
    aToP.getTheAsset("prop_chair_base")
    aToP.referenceIt()