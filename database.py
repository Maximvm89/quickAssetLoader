'''
Name: quickAssetLoader.database
Author: Marco Parisi 
Date: 04/13/2019
Version: 0.0


DESCRIPTION
---------------
This class is used to generate the database from qCompleter
in order to have a fast and reliable User Experience when
typing in the qLineEdit Field

'''


class AssetDB(object):
    assetsDb = []
    filename = None

    def __init__(self, filename):

        self.filename = filename

    def update_asset_db(self):
        """
        This is the method that should connect to the Company DB and create a txt file with all the asset list to
        use the autocompletion feature
        :return:
        :rtype:
        """
        pass

if __name__ == "__main__":
    # Used for testing purpose only
    aLoader = AssetDB("H:/db_assets.txt")
    aLoader.update_asset_db()
