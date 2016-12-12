import Header
#Characteristic Vector 保存每个grid的信息
class Grid:
    #"the last time when g is update" 即grid最近更新的时间点
    time_update=0
    #"the last time when g is removed from grid_list as a sporadic(if ever)" 即上次被以sporadic移出grid_list的时间点
    time_remove=0
    #the grid density at the last update
    density=0
    #the class label of the grid
    cluster_key=0
    #densityStatus:dense/sparse/transitional
    densityStatus=DensityStatus.SPARSE
    #sparse的子状态，当用以标记SPORADIC，和NORMAL,默认是NORMAL
    sparseStatus=SparseStatus.NORMAL
    #change.用来标记DensityStatus是否有过修改
    change=0

    key=0
    def key(self):
        return self.key
    def densityStatus(self):


    def clusterKey(self):

    #TODO:每调用一次这个函数认为当前grid来了一个新数据点
    def addData(self,rawData):
        if not self.grid_list.has_key(key):
            return -1
        #TODO:更新密度
        #TODO:判断密度变更与否和标记change
        return 0




