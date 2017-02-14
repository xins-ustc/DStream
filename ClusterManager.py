from Cluster import *
from Helper import  *
#用于对类簇进行管理和操作
class ClusterManager:
    __cluster_dic={}
    __cluster_key_index=0#用于区分不同的cluster,每有一个新cluster，+1
    #根据制定key获取cluster对象,否则返回null

    def __init__(self):
        self.__cluster_dic={}
        self.__cluster_key_index=0

    def getCluster(self,cluster_key):
        if not cluster_key in self.__cluster_dic:
            raise KeyError
        else:
            return self.__cluster_dic[cluster_key]

    #将grid加入为一个新的cluster
    #该函数不检查其他cluster是否已经有该grid
    def addNewCluster(self,grid_object):
        self.__cluster_key_index+=1
        cluster=Cluster(self.__cluster_key_index)
        cluster.addGrid(grid_object)
        self.__cluster_dic[self.__cluster_key_index]=cluster

    #返回某grid的neighboring的cluster数组
    def getNeighborClusters(self,grid_object):
        ret_clusters=[]
        keys=Helper.getNeighborKeys(grid_object.key())
        for k in self.__cluster_dic:
            cluster=self.__cluster_dic[k]
            for k in keys:
                if cluster.isGridExistWithKey(k):
                    ret_clusters.append(cluster)
                    continue
        return ret_clusters


    #一个cluster数组
    def getAllCluster(self):
        return self.__cluster_dic

    #把target并入source
    def mergeCluster(self,source_key,target_key):
        if not source_key in self.__cluster_dic:
            raise Exception("ClusterManager mergeCluster:source_key不存在",source_key)
        if not target_key in self.__cluster_dic:
            raise Exception("ClusterManager mergeCluster:target_key不存在", target_key)

        source_cluster=  self.__cluster_dic[source_key]
        target_cluster = self.__cluster_dic[target_key]

        #迁移grid
        target_grids = target_cluster.getAllGrids()
        for k in target_grids:
            grid_object=target_grids[k]
            source_cluster.addGrid(grid_object)

        #删除cluster
        self.__cluster_dic.pop(target_key)


    #切分cluster
    def splitCluster(self,cluster_key):
        if not cluster_key in self.__cluster_dic:
            raise Exception("ClusterManager splitCluster：cluster不存在")

        cluster=self.__cluster_dic[cluster_key]
        grids=cluster.getAllGrids()

        keys=[]
        for k in grids:
            g=grids[k]
            keys.append(g.key())
       #！！！这里的处理流程和isSingle重复了，但是为了保证函数的不变，只能复制一遍
        stop = 0
        # 初始化flag_dic
        flag_dic = {}
        #keys = self.__grid_dic.keys()
        for k in keys:
            flag_dic[k] = 0
        # 将第一个key对应的flag设置为1
        flag_dic[keys[0]] = 1

        while not stop:
            # 1、删除标记为2的key
            keys_todelete = []
            for k in flag_dic:
                if 2 == flag_dic[k]:
                    keys_todelete.append(k)
            for k in keys_todelete:
                flag_dic.pop(k)

            # 2、将标记为1的key的neighbor标记为1，然后把自己标记为2

            for k in flag_dic:
                item = flag_dic[k]
                if 1 == item:
                    neighbor_keys = Helper.getNeighborKeys(k)
                    for neighbor_key in neighbor_keys:
                        if neighbor_key in flag_dic:
                            flag_dic[neighbor_key] = 1
                    flag_dic[k] = 2

            # 3、若dic为空或全部标记都是0，循环结束
            stop = 1
            for k in flag_dic:
                item = flag_dic[k]
                if not 0 == item:
                    stop = 0
        # 循环结束后，判断flag_dic的长度，若为0，则是single
        if not 0 == len(flag_dic):
            #这部分就是被分割的部分
            #将这些grid移动到新的cluster中
            self.__cluster_key_index+=1
            new_cluster=Cluster(self.__cluster_key_index)
            self.__cluster_dic[self.__cluster_key_index]=new_cluster
            for k in flag_dic:
                moving_grid=cluster.getGrid(k)
                cluster.delGrid(moving_grid)
                new_cluster.addGrid(moving_grid)



