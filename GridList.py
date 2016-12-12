import Grid
#用于管理包含数据的Grid
class GridList:
    #TODO:返回一个neighborKey数组
    def getNeighborKeys(self,grid_key):
        #三维空间有6个neighbor
        retArray=[]



    #TODO:返回这个Grid的所有neighborGrid
    def getNeighborGrids(self,grid_key):
        #注意neighbor就是临近但是cluster不一样或者没有cluster的grid

    #TODO:传入一个RawData类型的数据,然后将它放入对应Grid中并更新Grid的状态
    def addNewData(self,rawData):

    #拿到标记change的grid
    def getChangeGrids(self):

    def delGrid(self,grid_key):

    #所有change置0
    def clearChangeFlag(self):

    #进入sporadic删除判定逻辑
    def removeSporadic(self):