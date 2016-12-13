from Grid import *
from Helper import *
#用于管理包含数据的Grid
class GridList:
    grid_list={}

    #返回一个neighborKey数组
    def getNeighborKeys(self,grid_key):
        return Helper().getNeighborKeys(grid_key)



    #返回这个Grid的所有neighborGrid的数组
    def getNeighborGrids(self,grid_key):
        #注意neighbor就是临近但是cluster不一样或者没有cluster的grid
        ret=[]
        keys=self.getNeighborKeys(grid_key)
        for key in keys:
            ret.append(self.grid_list[key])
        return ret

    #传入一个RawData类型的数据,然后将它放入对应Grid中并更新Grid的状态
    def addNewData(self,rawData,time):
        key=Helper().getKeyFromRawData(rawData)
        if not self.grid_list.has_key(key):
            grid_object=Grid()
            grid_object.addData(rawData,time)
            self.grid_list[key]=grid_object
        else:
            self.grid_list[key].addData(rawData,time)

    #返回一个包含dense的grid数组
    def getDenseGrids(self):
        ret=[]
        for k in self.grid_list:
            grid=self.grid_list[k]
            if DensityStatus.DENSE==grid.densityStatus():
                ret.append(grid)
        return ret
    #拿到标记change的grid
    def getChangeGrids(self):
        ret=[]
        for k in self.grid_list:
            grid_object=self.grid_list[k]
            if 1==grid_object.change():
                ret.append(grid_object)

        return ret


    #!!!!注意!!!!这个操作并不会真正把grid从grid_list中删除(paper里表示因为tm参数的存在,如果删除了,tm怎么标记呢?)
    def delGrid(self,grid_key,time):
        if not self.grid_list.has_key(grid_key):
            raise Exception("grid_list没有这个key,删除失败")
        else:
            #清空密度信息,只记录__time_remove
            grid_object=self.grid_list[grid_key]
            grid_object.clear()
            grid_object.setRemoveTime(time)

    #所有change置0
    def clearChangeFlag(self):
        for k in self.grid_list:
            grid_object=self.grid_list[k]
            grid_object.resetChangeFlag()


    #进入sporadic删除判定逻辑,处理所有grid
    def judgeAndremoveSporadic(self,current_time):
        for k in self.grid_list:
            grid_object = self.grid_list[k]
            if DensityStatus.SPARSE==grid_object.densityStatus():
                if SparseStatus.TODELETE==grid_object.sparseStatus():
                    #删除(由于paper中提到保留tg即time_remove，所以不从grid_list中删除，而是只清空数据，并记录time_remove)
                    grid_object.clear()
                    grid_object.setRemoveTime(current_time)
                elif SparseStatus.TEMP==grid_object.sparseStatus() or SparseStatus.NORMAL==grid_object.sparseStatus():
                    #判断s1和s2
                    if grid_object.densityThreshold()>grid_object.density(current_time) and current_time>=(1+Helper().beta)*grid_object.time_remove():
                        #符合s1,s2 放给TODELETE
                        grid_object.setSparseStatus(SparseStatus.TODELETE)
                    else:
                        #回NORMAL
                        grid_object.setSparseStatus(SparseStatus.NORMAL)


