'''
Name: quickAssetLoader.quickAssetLoaderUI
Author: Marco Parisi 
Date: 04/13/2019
Version: 0.0


DESCRIPTION
---------------
Open any asset introducing the Shotgun style name 

'''

# IMPORT UI MODULES
from PySide2 import QtCore, QtGui
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from PySide2.QtWidgets import QCompleter
from PySide2.QtWidgets import QTableWidgetItem
from PySide2.QtGui import QStringListModel
from shiboken2 import wrapInstance
from datetime import datetime
import os

# IMPORT CUSTOM MODULES
import database as db
import AssetEntity as asset_entity

reload( db )
reload( asset_entity )

# IMPORT MAYA MODULES
import maya.cmds as cmds
import maya.OpenMayaUI as omui


# UTILITY FUNCTION TO PUT THE WINDOW ALWAYS ON TOP
def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance( long( main_window_ptr ), QtWidgets.QWidget )


class QuickAssetLoaderUI( QtWidgets.QDialog ):

    def __init__(self, ui_path=None, parent=maya_main_window()):

        super( QuickAssetLoaderUI, self ).__init__( parent )
        self.setWindowTitle( "Quick Asset Loader" )
        self.setFixedSize( 600, 523 )

        # Remove the weird question Mark on the dialog window
        self.setWindowFlags( self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint )

        self.assets_db = db.ShotgunDB( "{0}/resource/dbAssets.txt".format( os.path.dirname( __file__ ) ) )
        self.init_ui( ui_path )
        self.create_layout()
        self.create_connections()
        self.completer = None
        self.asset_to_path = None

    def init_ui(self, ui_path=None):

        if not ui_path:
            ui_path = "{0}/resource/qDesignerUI.ui".format( os.path.dirname( __file__ ) )

        # IF A DB OF ASSETS DOES NOT EXIST CREATE IT
        if not os.path.isfile( "{0}/resource/dbAssets.txt".format( os.path.dirname( __file__ ) ) ):
            self.assets_db.updateAssetDB()

        # SETTING UP THE QCOMPLETER FOR FASTER INTERACTIONS
        db_file = open( "{0}/resource/dbAssets.txt".format( os.path.dirname( __file__ ) ), "r" )
        assets = db_file.readlines()

        # Cleaning the line stripping out the end line character
        for i in range( len( assets ) ):
            assets[i] = assets[i].rstrip( '\n' )

        self.asset_to_path = asset_entity.AssetEntity()
        self.completer = QCompleter()
        model = QtGui.QStringListModel()
        self.completer.setModel( model )
        model.setStringList( assets )

        f = QtCore.QFile( ui_path )
        f.open( QtCore.QFile.ReadOnly )

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load( f, parentWidget=self )

        f.close()

    def create_layout(self):
        self.ui.layout().setContentsMargins( 6, 6, 6, 6 )

    def create_connections(self):

        self.ui.inputText.textChanged.connect( self.populate_suggestions )
        self.ui.charmainButton.clicked.connect( self.charmain_button_clicked )
        # Setting up the QCompleter to work with inputField
        self.ui.inputText.setCompleter( self.completer )

        # Connecting Buttons
        self.ui.charsecButton.clicked.connect( self.charsec_button_clicked )
        self.ui.vehButton.clicked.connect( self.veh_button_clicked )
        self.ui.envintButton.clicked.connect( self.envint_button_clicked )
        self.ui.envextButton.clicked.connect( self.envext_button_clicked )
        self.ui.propButton.clicked.connect( self.prop_button_clicked )
        self.ui.reference_button.clicked.connect( self.reference_button )
        self.ui.import_button.clicked.connect( self.import_button )
        self.ui.tableWidget.itemDoubleClicked.connect( self.cell_double_clicked )
        self.ui.char1Button.clicked.connect( self.char1ButtonClicked )
        self.ui.char2Button.clicked.connect( self.char2ButtonClicked )
        self.ui.char3Button.clicked.connect( self.char3ButtonClicked )
        self.ui.char4Button.clicked.connect( self.char4ButtonClicked )
        self.ui.updateDBButton.clicked.connect( self.update_db )

    def update_db(self):
        self.assets_db.updateAssetDB()

    # TODO define a config file to have presets for most used characters to load

    # def char1ButtonClicked(self):
    #     self.asset_to_path.char1Button()
    #
    # def char2ButtonClicked(self):
    #     self.asset_to_path.char2Button()
    #
    # def char3ButtonClicked(self):
    #     self.asset_to_path.char3Button()
    #
    # def char4ButtonClicked(self):
    #     self.asset_to_path.char4Button()

    def cell_double_clicked(self, item):
        """
        If an user double clicked on the asset name, it will automatically trying to import it into the scene
        :param item: the Item clicked in the UI

        """
        if item.text().endswith( ".ma" ):
            if os.path.isfile( self.asset_to_path.get_asset_path() ):
                self.asset_to_path.import_asset( self.asset_to_path.get_asset_path() )

    def charmain_button_clicked(self):
        self.ui.inputText.clear()
        self.ui.inputText.insert( "charmain_" )

    def charsec_button_clicked(self):
        self.ui.inputText.clear()
        self.ui.inputText.insert( "charsec_" )

    def veh_button_clicked(self):
        self.ui.inputText.clear()
        self.ui.inputText.insert( "veh_" )

    def envint_button_clicked(self):
        self.ui.inputText.clear()
        self.ui.inputText.insert( "envint_" )

    def envext_button_clicked(self):
        self.ui.inputText.clear()
        self.ui.inputText.insert( "envext_" )

    def prop_button_clicked(self):
        self.ui.inputText.clear()
        self.ui.inputText.insert( "prop_" )

    # Reference The Asset
    def reference_button(self):
        asset_name = self.ui.inputText.text()
        self.asset_to_path.setTheAsset( asset_name )
        self.asset_to_path.referenceIt()

    # Import The Asset in Maya
    def import_button(self):
        asset_name = self.ui.inputText.text()
        self.asset_to_path.setTheAsset( asset_name )
        self.asset_to_path.openIt()

    def populate_suggestions(self, text):

        # For Design purpose we want to input always lowercase
        self.ui.inputText.setText( text.lower() )

        # Clean the table everytime something is typed in the inputField
        self.ui.tableWidget.setRowCount( 0 )

        full_path = self.asset_to_path.get_asset_path( text.lower() )
        if full_path is not None:

            path, asset_file_name = os.path.split( full_path[0] )
            self.ui.labelAsset.setText( str( asset_file_name ) )
            if self.asset_to_path.setTheAsset( text ) is not None:
                files = self.asset_to_path.get_files_in_asset_dir()

            self.ui.tableWidget.setRowCount( len( files ) )
            for i in range( 0, len( files ) ):
                full_path[0] = files[i]
                path, asset_file_name = os.path.split( full_path[0] )
                file_name_item = QTableWidgetItem( asset_file_name )
                file_name_item.setFlags( QtCore.Qt.ItemIsEnabled )
                self.ui.tableWidget.setItem( i, 0, file_name_item )
                mod_time = datetime.fromtimestamp( os.path.getmtime( files[i] ) )
                mod_time_item = QTableWidgetItem( str( mod_time ) )
                mod_time_item.setFlags( QtCore.Qt.ItemIsEnabled )
                self.ui.tableWidget.setItem( i, 1, mod_time_item )

            self.ui.tableWidget.resizeColumnsToContents()
