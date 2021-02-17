'''
Name: quickAssetLoader.quickAssetLoaderUI
Author: Marco Parisi 
Date: 04/13/2019
Version: 0.0


DESCRIPTION
---------------
Open any asset introducing the Shotgun style name 

'''


#IMPORT UI MODULES
from PySide2 import QtCore ,  QtGui
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from PySide2.QtWidgets import QCompleter 
from PySide2.QtWidgets import QTableWidgetItem
from PySide2.QtGui import QStringListModel
from shiboken2 import wrapInstance
from datetime import datetime
import os

#IMPORT CUSTOM MODULES
import database as shAssets
import AssetEntity as aPath


reload(shAssets)
reload(aPath)

#IMPORT MAYA MODULES
import maya.cmds as cmds
import maya.OpenMayaUI as omui

#UTILITY FUNCTION TO PUT THE WINDOW ALWAYS ON TOP
def maya_main_window():
    
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class QuickAssetLoaderUI(QtWidgets.QDialog):
    

    completer = None
    assetToPath = None
    
    
    def __init__(self, ui_path=None, parent=maya_main_window()):
        
        super(QuickAssetLoaderUI, self).__init__(parent)
        self.setWindowTitle("Quick Asset Loader")
        self.setFixedSize(600,523)
        
        #Remove the weird question Mark on the dialog window
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        
        self.assetsSH = shAssets.ShotgunDB("{0}/resource/dbAssets.txt".format(os.path.dirname(__file__)))
        self.init_ui(ui_path)
        self.create_layout()
        self.create_connections()
        
    def init_ui(self, ui_path=None):


        if not ui_path:
            ui_path="{0}/resource/qDesignerUI.ui".format(os.path.dirname(__file__))
            
            
        #IF A DB OF ASSETS DOES NOT EXIST CREATE IT
        if not os.path.isfile("{0}/resource/dbAssets.txt".format(os.path.dirname(__file__))):
            self.assetsSH.updateAssetDB()
            
        #SETTING UP THE QCOMPLETER FOR FASTER INTERACTIONS
        file = open("{0}/resource/dbAssets.txt".format(os.path.dirname(__file__)), "r")
        assets = file.readlines()
        
        for i in range(len(assets)):
            assets[i] = assets[i].rstrip('\n')
            
        self.assetToPath = aPath.AssetEntity()
        self.completer = QCompleter()
        model = QtGui.QStringListModel()
        self.completer.setModel(model)
        model.setStringList(assets)

        f = QtCore.QFile(ui_path) 
        f.open(QtCore.QFile.ReadOnly)

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(f, parentWidget=self)

        f.close()    
        
    def create_layout(self):
        self.ui.layout().setContentsMargins(6, 6, 6, 6)

    def create_connections(self):


        self.ui.inputText.textChanged.connect(self.populateSuggestions)
        self.ui.charmainButton.clicked.connect(self.charmainButtonClicked)
        #Setting up the QCompleter to work with inputField
        self.ui.inputText.setCompleter(self.completer)
        
        #Connecting Buttons
        self.ui.charsecButton.clicked.connect(self.charsecButtonClicked)
        self.ui.vehButton.clicked.connect(self.vehButtonClicked)
        self.ui.envintButton.clicked.connect(self.envintButtonClicked)
        self.ui.envextButton.clicked.connect(self.envextButtonClicked)
        self.ui.propButton.clicked.connect(self.propButtonClicked)
        self.ui.referenceButton.clicked.connect(self.referenceButton)
        self.ui.importButton.clicked.connect(self.importButton)
        self.ui.tableWidget.itemDoubleClicked.connect(self.cellDoubleClicked)
        self.ui.char1Button.clicked.connect(self.char1ButtonClicked)
        self.ui.char2Button.clicked.connect(self.char2ButtonClicked)
        self.ui.char3Button.clicked.connect(self.char3ButtonClicked)
        self.ui.char4Button.clicked.connect(self.char4ButtonClicked)
        self.ui.updateDBButton.clicked.connect(self.updateDb)
        
    def updateDb(self):
        self.assetsSH.updateAssetDB()


    def char1ButtonClicked(self):
        self.assetToPath.char1Button()
    def char2ButtonClicked(self):
        self.assetToPath.char2Button()
    def char3ButtonClicked(self):
        self.assetToPath.char3Button()
    def char4ButtonClicked(self):
        self.assetToPath.char4Button()
                                      
        
    def cellDoubleClicked(self,item):
        
        if 'ma' in item.text():
            path="{}\{}".format( self.assetToPath.get_asset_path(), item.text() )
            self.assetToPath.reference(path) 
        else:
            print 'You selected a date, please select the asset Name'
        

    def charmainButtonClicked(self):
        self.ui.inputText.clear()
        self.ui.inputText.insert("charmain_")

    def charsecButtonClicked(self):
        self.ui.inputText.clear()
        self.ui.inputText.insert("charsec_")
        
    def vehButtonClicked(self):
        self.ui.inputText.clear()
        self.ui.inputText.insert("veh_")
        
    def envintButtonClicked(self):
        self.ui.inputText.clear()
        self.ui.inputText.insert("envint_")
        
    def envextButtonClicked(self):
        self.ui.inputText.clear()
        self.ui.inputText.insert("envext_")
        
    def propButtonClicked(self):
        self.ui.inputText.clear()
        self.ui.inputText.insert("prop_")
        
        
    #Reference The Asset
    def referenceButton(self):
        assetName = self.ui.inputText.text()
        self.assetToPath.setTheAsset(assetName)
        self.assetToPath.referenceIt()
    #Import The Asset in Maya
    def importButton(self):
        assetName = self.ui.inputText.text()
        self.assetToPath.setTheAsset(assetName)
        self.assetToPath.openIt()

    def populateSuggestions(self , text):
        
        
        #For Design purpose we want to input always lowercase
        self.ui.inputText.setText(text.lower())
        
        #Clean the table everytime something is typed in the inputField
        self.ui.tableWidget.setRowCount(0)
        
        fullPath = self.assetToPath.setTheAsset(text.lower())
        if fullPath is not None:
            
            path, fileName = os.path.split(fullPath[0])
            self.ui.labelAsset.setText(str(fileName))
            if self.assetToPath.setTheAsset(text) is not None:
                files =  self.assetToPath.get_files_in_asset_dir()
        

            self.ui.tableWidget.setRowCount(len(files))
            for i in range(0, len(files)):
                
                fullPath[0] = files[i]
                path, fileName = os.path.split(fullPath[0])
                fileNameItem = QTableWidgetItem(fileName)
                fileNameItem.setFlags(QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidget.setItem(i,0,fileNameItem)
                modTime =  datetime.fromtimestamp(os.path.getmtime(files[i]))
                modTimeItem = QTableWidgetItem(str(modTime))
                modTimeItem.setFlags(QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidget.setItem(i,1,modTimeItem)

            self.ui.tableWidget.resizeColumnsToContents()
        
        
        