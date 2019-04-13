'''
Name: quickAssetLoader.main
Author: Marco Parisi 
Date: 04/13/2019
Version: 0.0


DESCRIPTION
---------------
Main script to launch the UI Interface in Maya

'''
import quickAssetLoader.quickAssetLoaderUI as quickAssets

reload(quickAssets)

#If another window is opened, close it and delete Later
try:
    QtDesignerUI.close()
    QtDesignerUI.deleteLater()
except:
    pass
    
QtDesignerUI = quickAssets.QuickAssetLoaderUI()
QtDesignerUI.show()

