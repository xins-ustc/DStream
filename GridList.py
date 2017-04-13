from Grid import *
from Helper import *
import logging
#用于管理包含数据的Grid
class GridList:
    __grid_list={}
    def __init__(self):
        self.__grid_list={}

    def size(self):
        return len(self.__grid_list)

    def getGrid(self,grid_key):
        #注意！：若grid被remove，因为算法原因并没有从dic中删除，所以之前被删除的grid也会存在于
        if not grid_key in self.__grid_list:
            raise KeyError
        grid=self.__grid_list[grid_key]
        if grid.time_remove()!=0 and grid.density()==0:
            raise KeyError("grid has been remove though it still exist in grid_list")
        return self.__grid_list[grid_key]

    #返回这个Grid的所有neighborGrid的数组
    def getNeighborGrids(self,grid_key):
        if not grid_key in self.__grid_list :
            raise KeyError
        grid=self.__grid_list[grid_key]
        if grid.time_remove()!=0 and grid.density()==0:
            raise KeyError("grid has been remove though it still exist in grid_list")

        #注意neighbor就是临近但是cluster不一样或者没有cluster的grid
        ret=[]
        keys=Helper.getNeighborKeys(grid_key)
        for key in keys:
            if key in self.__grid_list:
                gird=self.__grid_list[key]
                if not (grid.density()==0 and grid.time_remove()!=0):
                    ret.append(self.__grid_list[key])
        return ret

    #传入一个RawData类型的数据,然后将它放入对应Grid中并更新Grid的状态
    def addNewData(self,rawData,time):
        logging.debug("Pw:" + str(rawData.PW) + " RF:" + str(rawData.RF) + " DOA:" + str(rawData.DOA)+" time:"+str(time))
        key=Helper().getKeyFromRawData(rawData)
        if not key in self.__grid_list:
            grid_object=Grid()
            grid_object.addData(rawData,time)
            self.__grid_list[key]=grid_object
        else:
            self.__grid_list[key].addData(rawData,time)

    #返回一个包含dense的grid数组
    def getDenseGrids(self):
        ret=[]
        for k in self.__grid_list:
            grid=self.__grid_list[k]
            if DensityStatus.DENSE==grid.densityStatus():
                ret.append(grid)
        return ret

    def getSparseGrids(self):
        ret=[]
        for k in self.__grid_list:
            grid=self.__grid_list[k]
            if DensityStatus.SPARSE==grid.densityStatus():
                ret.append(grid)
        return ret


    #拿到标记change的grid
    def getChangeGrids(self):
        ret=[]
        for k in self.__grid_list:
            grid_object=self.__grid_list[k]
            if 1==grid_object.change():
                ret.append(grid_object)

        return ret


    #!!!!注意!!!!这个操作并不会真正把grid从grid_list中删除(paper里表示因为tm参数的存在,如果删除了,tm怎么标记呢?)
    def delGrid(self,grid_key,time):
        if not grid_key in self.__grid_list:
            raise KeyError("grid_list没有这个key,删除失败")
        else:
            logging.debug("grid "+grid_key+"is deleted(actually this grid is clear but not removed from gridList)")
            # 删除(由于paper中提到保留tg即time_remove，所以不从grid_list中删除，而是只清空数据，并记录time_remove)
            #清空密度信息,只记录__time_remove
            grid_object=self.__grid_list[grid_key]
            grid_object.clear()
            grid_object.setRemoveTime(time)

    #所有change置0
    def clearChangeFlag(self):
        for k in self.__grid_list:
            grid_object=self.__grid_list[k]
            grid_object.resetChangeFlag()




