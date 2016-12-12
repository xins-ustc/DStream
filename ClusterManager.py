import Cluster

#用于对类簇进行管理和操作
class ClusterManager:
    #TODO:返回grid的cluster，若没有则返回-1
    def getClusterNo(self,grid_key):

    #TODO:根据制定key获取cluster对象,否则返回null
    def getCluster(self,cluster_key):
        return None

    #TODO:返回某grid的neighboring的cluster数组
    def getNeighborClusters(self,grid_key):

    #TODO:一个dic，key是cluster的编号，value是cluster的集合
    def getAllCluster(self):

    #把target并如source
    def mergeCluster(self,source_key,target_key):


    #切分cluster(只针对已经不是一个整体的cluster),如果cluster依然是一个整体,返回-1
    def splitCluster(self,cluster_key):