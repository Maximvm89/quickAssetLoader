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


# SG Imports
import shotgun_api3
#Helper method to find assets
import sg_utils.sg_query as sgq

class ShotgunDB(object):
    
    
    assetsDb = []    
    filename = None
    
    def __init__(self, filename):

        
        #sg = shotgun_api3.Shotgun() #In here all the data to connect to your studio shotgun in order to access data
        self.filename = filename
        
        

    def updateAssetDB(self):
        
        # Main procedure
        allAssetsInfo = sgq.get_all_assets_info()
 
        
        
        for assetsInfo in allAssetsInfo:
            nameShotgun = assetsInfo['code']
            self.assetsDb.append(nameShotgun)
            
        self.assetsDb = list(dict.fromkeys(self.assetsDb))
        self.assetsDb.sort()
        f=open(self.filename,"w+")
        for i in range(len(self.assetsDb)):
            f.write(self.assetsDb[i]+"\n" )
   
        f.close()
            
            
if __name__ == "__main__":

    #Used for testing purpose only
    aLoader = ShotgunDB("H:/db_assets.txt")
    aLoader.updateAssetDB()
