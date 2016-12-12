class Cluster:
    #TODO:记录当前cluster的key
    def key(self):
    #TODO:往当前cluster中加入grid
    def addGrid(self,grid_object):
    #TODO：从cluster中删除grid
    def delGrid(self,grid_object):
    #TODO:判断某grid是否为该cluster的grid
    def isOutsideGrid(self,grid_object):
    #TODO：返回cluster的size
    def size(self):
    # TODO:判断如果加入指定cluster是不是它的outside
    def isOutsideIfAdd(self, grid_key):

    #TODO:获取cluster里的所有outside的grid
    def getOutsideGrids(self):

    def isClusterSingle(self):