from Helper import *
import logging

class Cluster:
    __grid_dic = {}
    __key = -1
    #记录当前cluster的key

    def __init__(self,cluster_key):
        self.__key=cluster_key
        self.__grid_dic={}

    def getGrid(self,grid_key):
        if not grid_key in self.__grid_dic:
            raise KeyError("Cluster getGrid:没有这个grid")
        else:
            return self.__grid_dic[grid_key]

    def key(self):
        return self.__key

    def isGridExist(self,grid_object):
        if grid_object.key() in self.__grid_dic:
            return True
        return False

    def isGridExistWithKey(self,grid_key):
        if grid_key in self.__grid_dic:
            return True
        return False

    #往当前cluster中加入grid
    def addGrid(self,grid_object):
        key=grid_object.key()
        if int(key) <0:
            raise KeyError("key不能小于0")
        if key in self.__grid_dic:
            raise Exception("Cluster addGrid：该Cluster已存在这个grid")
        else:
            self.__grid_dic[key]=grid_object
            grid_object.setClusterKey(self.__key)
            logging.debug("cluster "+str(self.__key)+" add grid "+str(grid_object.key()))

    #从cluster中删除grid(这个操作不理会grid_list)
    def delGrid(self,grid_object):
        if not grid_object.key() in self.__grid_dic:
            raise KeyError("Cluster delGrid:这个Cluster中不存在这个grid")
        else:
            grid_object.setClusterKey(-1)
            self.__grid_dic.pop(grid_object.key())


    #判断某grid是否为该cluster的outside_grid
    def isOutsideGrid(self,grid_object):
        if not grid_object.key() in self.__grid_dic:
            raise KeyError("Cluster isOutsideGrid:这个grid不在该Cluster",grid_object.key(),self.__key)
        else:
            #判断grid的位置(判断它的方块的6个面，若6个面的grid都在cluster里，说明是inside)
            neighbor_keys=Helper.getNeighborKeys(grid_object.key())
            for k in neighbor_keys:
                #如果这个key不存在，说明就是outside了
                if not k in self.__grid_dic:
                    return True
            return False




    #返回cluster的size
    def size(self):
        return len(self.__grid_dic)

    # 判断如果加入指定cluster是不是它的outside
    def isOutsideIfAdd(self, grid_object):
        if grid_object.key() in self.__grid_dic:
            raise KeyError("Cluster isOutsiedIfAdd：该grid已经在本Cluster里",grid_object.key(),self.__key)
        else:
            #判断outside（）
            neighbor_keys = Helper.getNeighborKeys(grid_object.key())
            for k in neighbor_keys:
                if not k in self.__grid_dic:
                    return True
            return False


    #获取cluster里的所有outside的grid
    def getOutsideGrids(self):
        ret=[]
        for k in self.__grid_dic:
            grid_object=self.__grid_dic[k]
            if self.isOutsideGrid(grid_object):
                ret.append(grid_object)
        return ret

    def isClusterSingle(self):
        #判断该cluster是不是单一cluster，还是已经分成两半了
        #用燃烧法判断，就像火焰烧东西一样，完全隔绝的东西烧不到
        #（从第一个grid开始染色，染他的neighbor，然后删除它本身，过程结束后若存在未染色的点，则是single。
        #这其实是广度优先算法的一种
        #这里需要一个dic结构叫flag_dic，key是cluster_key value是0 1 2 ，0表示未染色，1表示已经染色，用作下一步处理，2表示需要删除
        stop=0
        #初始化flag_dic
        flag_dic={}
        keys=list(self.__grid_dic.keys())
        for k in keys:
            flag_dic[k]=0
        #将第一个key对应的flag设置为1
        flag_dic[keys[0]]=1

        while not stop:
            #1、删除标记为2的key
            keys_todelete=[]
            for k in flag_dic:
                if 2==flag_dic[k]:
                    keys_todelete.append(k)
            for k in keys_todelete:
                flag_dic.pop(k)

            #2、将标记为1的key的neighbor标记为1，然后把自己标记为2

            for k in flag_dic:
                item = flag_dic[k]
                if 1==item:
                    neighbor_keys=Helper.getNeighborKeys(k)
                    for neighbor_key in neighbor_keys:
                        if neighbor_key in  flag_dic:
                            flag_dic[neighbor_key]=1
                    flag_dic[k]=2

            #3、若dic为空或全部标记都是0，循环结束
            stop=1
            for k in flag_dic:
                item = flag_dic[k]
                if not 0 == item:
                    stop=0
        #循环结束后，判断flag_dic的长度，若为0，则是single
        if 0==len(flag_dic):
            return True
        else :
            return False




    def getAllGrids(self):
        return self.__grid_dic