'''
Name: quickAssetLoader.assetToPath
Author: Marco Parisi 
Date: 04/13/2019
Version: 0.1


DESCRIPTION
---------------
The point of this class is to gather the asset name from quickAssetLoaderUI
and get the file path to where this asset lives on disk.
This class will be pretty much with placeholder methods to be implemented based on the company's pipeline

'''
import maya.cmds as cmds
import os

class AssetEntity:

    def __init__(self, asset_name, namespace=None):
        """
        Init method
        :param str asset_name: the string version of the asset name
        """

        self.asset_name = asset_name
        self.asset_path = self.get_asset_path()
        self.namespace = namespace

    @staticmethod
    def get_asset_path():
        """
        This method should be used to retrieve the asset_path whether we use Company's API, Sgtk templates,
        or simple os.walk on disk

        """
        return ""

    def open_asset(self):

        """
        Open the file in maya
       
        """
        if os.path.isfile(self.asset_path):
            cmds.file(self.asset_path, o=True)

    def import_asset(self):
        """
        Reference the file into the current scene
       
        """
        if not self.namespace:
            ass_namespace = self.asset_name
        else:
            ass_namespace = self.namespace
        cmds.file( self.asset_path, r=True, ns=ass_namespace )



if __name__ == "__main__":
    # Testing Purpose
    asset_entity = AssetEntity(asset_name="prop_chair_base", namespace="prop_chair_base_RIG")
    # import asset into the current opened scene
    asset_entity.import_asset()
