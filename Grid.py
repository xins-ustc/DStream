from Header import *
from Helper import *

from HelperForTest import *

import unittest

#Characteristic Vector 保存每个grid的信息
class Grid:
    #"the last time when g is update" 即grid最近更新的时间点
    __time_update=0
    #"the last time when g is removed from grid_list as a sporadic(if ever)" 即上次被以sporadic移出grid_list的时间点
    __time_remove=0
    #the grid density at the last update
    __density=0
    #the class label of the grid
    __cluster_key=-1
    #densityStatus:dense/sparse/transitional
    __densityStatus=DensityStatus.SPARSE
    #sparse的子状态，当用以标记SPORADIC，和NORMAL,默认是NORMAL
    __sparseStatus=SparseStatus.NORMAL
    #change.用来标记DensityStatus是否有过修改
    __change=0
    __key=0

    def __init__(self):
        __time_update = 0
        __time_remove = 0
        __density = 0
        __cluster_key = -1
        __densityStatus = DensityStatus.SPARSE
        __sparseStatus = SparseStatus.NORMAL
        __change = 0
        __key = 0



    #tested
    def key(self):
        return self.__key
    #test
    def time_remove(self):
        return self.__time_remove

    #test
    def isNoCluster(self):
        if -1==self.__cluster_key:
            return True
        return False
    #test
    def setClusterKey(self,key):
        self.__cluster_key=key

    #这个值有些诡异，从测试来看，它永远是一个1e-10 左右的数。从测试来看，这个指标是用来衡量grid在两个新数据点之间时间间隔的度量，但是这个度量
    #也太离谱了吧？
    #test
    def densityThreshold(self,time):
        return (Helper().Cl * (1 - (Helper().lamb ** (time - self.__time_update + 1)))) / (Helper().N * (1 - Helper().lamb))
    #test
    def setSparseStatus(self,status):
        self.__sparseStatus=status
    #test
    def density(self):
        return self.__density

    #根据时间来得到当前grid的density
    #test
    def densityWithTime(self,current_time):
        #根据公式是1+（last_density*lamb**(current_time-time_update)
        #又这个公式的证明过程和意义可知，当前时间的密度是lamb**(current_time-time_update)*last_density
        return self.__density*(Helper().lamb**(current_time-self.__time_update))

    #test
    def sparseStatus(self):
        return self.__sparseStatus

    #test
    def densityStatus(self):
        return self.__densityStatus
        #!!!!!!!!!!!!!!!!!!!考虑可以直接返回成员变量，因为每次addData都会更新这个值!!!!!!!
        #============下面代码保留，虽然没用
        ret=None
        if self.__densityStatus>=Helper().Dm:
            return DensityStatus.DENSE
        elif self.__densityStatus<=Helper().Dl:
            return DensityStatus.SPARSE
        else:
            #注意：paper里说这个应该是闭区间，但是我觉得开区间比较准确
            return DensityStatus.TRANSITIONAL
    #test
    def clusterKey(self):#test
        return self.__cluster_key


    #每调用一次这个函数认为当前grid来了一个新数据点
    # test
    def addData(self,rawData,time):
        if time<=self.__time_update:
            raise ValueError("addData:time cannot less then time_update")

        if not 0==self.__key:
            if not Helper.getKeyFromRawData(rawData)==self.__key:
                raise ValueError
        #设置key
        self.__key=Helper.getKeyFromRawData(rawData)


        #更新密度 D(g,tn)=λ**(tn-tl)*D(g,tl)+1 其中tn是当前时间，tl是前一个更新时间
        self.__density=self.__density*(Helper().lamb**(time-self.__time_update))+1
        #判断密度变更与否和标记change
        if not Helper().getDensityStatus(self.__density)==self.__densityStatus:
            self.__change=1
            self.__densityStatus=Helper().getDensityStatus(self.__density)

        #若处于TODELETE状态，转为TEMP
        if SparseStatus.TODELETE==self.__sparseStatus:
            self.__sparseStatus=SparseStatus.TEMP

        #更改更新时间
        self.__time_update=time
        #print("grid_key:\t",self.__key,"\tgrid_density:\t",self.__density)
    #清空数据
    #test
    def clear(self):
        self.__cluster_key=-1
        self.__density=0
        self.__change=0
        self.__densityStatus=DensityStatus.SPARSE
        self.__sparseStatus=SparseStatus.NORMAL
        self.__time_remove=0
        self.__time_update=0

    #test
    def setRemoveTime(self,time):
        self.__time_remove=time
    #test
    def resetChangeFlag(self):
        self.__change=0

    #test
    def change(self):
        return self.__change

