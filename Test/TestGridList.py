import unittest
from GridList import *
from Grid import *
class TestGridList(unittest.TestCase):

    def test_getGrid(self):
        #case1:key不存在，抛出KeyError
        #case2：key存在，得到正确的Grid

    def test_gridList(self):
        #测试gridlist存在且初始为空
    def test_getNeighborKey(self):

    def test_getNeighborGrids(self):
        #case1:gridKey不存在时的异常抛出
        #case2:gridKey存在但当前没有其他Neighbor时返回的空值
        #case3:gridKey存在且Neighbor也存在但是不满时
        #case4:gridKey存在且Neighbor也存在且有6个

    def test_addNewData(self):
        #case1：对应grid不存在，添加data
        #case2:对应grid存在，添加data，判断添加后的数值是否正确

    def test_getDenseGrids(self):
        #case1:list中没有dense的grid，但有其他两种grid返回空值
        #case2：list中有Dense，且有其他两种grid，返回正确的grid
        #case3：list中全是dense，返回整个list

    def test_getChangeGrids(self):
        #case1：list中没有change的grid，返回空值
        #case2：list中有change，返回对应change，检查数量是否正确
        #case3：list中全是change

    def test_delGrid(self):
        #case1:list中不存在对应grid，抛出异常
        #case2：list中有目标grid，检查调用函数后grid是否数据被清空且remove_time是否正确

    def test_clearChangeFlag(self):
        #case1:list为空，调用
        #case2:list不为空，但change全为0，调用
        #case3:list部分change为1，
        #case4：list中change全为1

    def test_judgeAndremoveSporadic(self):
        #case1:list中没有Sparse的grid，调用后检查各个grid的状态的remove_time，没有变化且gird的数量没有变化
        gridList=GridList()
        time=0
        for i in range(1,100):
            time+=random.randint(1,10000)
            raw=HelperForTest.randomLegalRawData()
            key=Helper.getKeyFromRawData(raw)
            g=Grid()
            g.addData(raw,time)
            g._Grid__densityStatus=DensityStatus.DENSE
            gridList._GridList__grid_list[key]=g
        gridList.judgeAndremoveSporadic(time+random.randint(1,10000))
        length=len(gridList._GridList__grid_list)
        for grid in gridList._GridList_grid_list:
            self.assertEqual(grid._Grid__time_remove,0)
            self.assertEqual(len(gridList._GridList_grid_list),length)

        #case2：list中有Sparse，Dense和Transitional，调用后，Dense和Transitional的数量不变，
                # Sparse的数量也不变，且Sparse中TODELETE的状态全部被处理
                # 3个3个TODELETE，3个符合s1但不符合s2的NORMAL和3个同类TEMP，3个符合s2但不符合s1的NORMAL和同类TEMP,3个符合s1和s2的TEMP，3个符合s1和s2的NORMAL
        gridList = GridList()
        for i in range(1, 1000):
            time += random.randint(1, 10000)
            raw = HelperForTest.randomLegalRawData()
            key = Helper.getKeyFromRawData(raw)
            g = Grid()
            g.addData(raw, time)
            g._Grid__densityStatus = DensityStatus.DENSE
            gridList._GridList__grid_list[key] = g
        #由于是随机生成的，有可能重复，所以未必就是1000个
        time+=1
        length=len(gridList._Grid__grid_list)
        keys=gridList(gridList._Grid__grid_list.keys())
        #3 TODELETE
        for i in range(0,3):
            k=keys[i]
            grid=gridList.getGrid(k)
            grid._Grid__denistyStatus=DensityStatus.SPARSE
            grid._Grid__sparseStatus=SparseStatus.TODELETE
        #===============3 s1 not s2 NORMAL====================
        #s1:grid_object.densityThreshold()>grid_object.density(current_time)
        #s2:current_time>=(1+Helper().beta)*grid_object.time_remove()
        for i in range(3, 6):
            k = keys[i]
            grid = gridList.getGrid(k)
            grid._Grid__denistyStatus = DensityStatus.SPARSE
            grid._Grid__sparseStatus = SparseStatus.NORMAL
            # 使不符合s2，公式同上（s2需要修改time_remove,而s1中的Th需要用到time_remove,顾先改s2）
            grid._Grid__time_remove=time/(1+Helper().lamb)+i
            #使符合s1，公式是自己推导出来的
            grid._Grid_density=grid.densityThreshold(time)/(Helper().lamb**(time-grid._Grid__time_update))-i

        for i in range(6, 9):
            k = keys[i]
            grid = gridList.getGrid(k)
            grid._Grid__denistyStatus = DensityStatus.SPARSE
            grid._Grid__sparseStatus = SparseStatus.TEMP
            # 使不符合s2，公式同上（s2需要修改time_remove,而s1中的Th需要用到time_remove,顾先改s2）
            grid._Grid__time_remove=time/(1+Helper().lamb)+i
            #使符合s1，公式是自己推导出来的
            grid._Grid_density=grid.densityThreshold(time)/(Helper().lamb**(time-grid._Grid__time_update))-i
        #=================s2 not s1===================
        for i in range(9, 12):
            k = keys[i]
            grid = gridList.getGrid(k)
            grid._Grid__denistyStatus = DensityStatus.SPARSE
            grid._Grid__sparseStatus = SparseStatus.NORMAL
            # 使符合s2，公式同上（s2需要修改time_remove,而s1中的Th需要用到time_remove,顾先改s2）
            grid._Grid__time_remove=time/(1+Helper().lamb)-i
            #使不符合s1，公式是自己推导出来的
            grid._Grid_density=grid.densityThreshold(time)/(Helper().lamb**(time-grid._Grid__time_update))+i
        for i in range(12, 15):
            k = keys[i]
            grid = gridList.getGrid(k)
            grid._Grid__denistyStatus = DensityStatus.SPARSE
            grid._Grid__sparseStatus = SparseStatus.TEMP
            # 使符合s2，公式同上（s2需要修改time_remove,而s1中的Th需要用到time_remove,顾先改s2）
            grid._Grid__time_remove=time/(1+Helper().lamb)-i
            #使不符合s1，公式是自己推导出来的
            grid._Grid_density=grid.densityThreshold(time)/(Helper().lamb**(time-grid._Grid__time_update))+i
        #======s1 and s2===============
        for i in range(15, 18):
            k = keys[i]
            grid = gridList.getGrid(k)
            grid._Grid__denistyStatus = DensityStatus.SPARSE
            grid._Grid__sparseStatus = SparseStatus.TEMP
            # 使符合s2，公式同上（s2需要修改time_remove,而s1中的Th需要用到time_remove,顾先改s2）
            grid._Grid__time_remove=time/(1+Helper().lamb)-i
            #使符合s1，公式是自己推导出来的
            grid._Grid_density=grid.densityThreshold(time)/(Helper().lamb**(time-grid._Grid__time_update))-i
        for i in range(18, 21):
            k = keys[i]
            grid = gridList.getGrid(k)
            grid._Grid__denistyStatus = DensityStatus.SPARSE
            grid._Grid__sparseStatus = SparseStatus.NORMAL
            # 使符合s2，公式同上（s2需要修改time_remove,而s1中的Th需要用到time_remove,顾先改s2）
            grid._Grid__time_remove=time/(1+Helper().lamb)-i
            #使符合s1，公式是自己推导出来的
            grid._Grid_density=grid.densityThreshold(time)/(Helper().lamb**(time-grid._Grid__time_update))-i
        #被归入
        gridList.judgeAndremoveSporadic(time)
        #case1：3个TODELTE被删除
        for i in range(0,3):
            key=keys[i]
            grid=gridList.getGrid(key)
            self.assertEqual(grid.sparseStatus(),SparseStatus.NORMAL)
            self.assertEqual(grid.time_remove(),time)
            self.assertEqual(grid.density(),0)
            self.assertEqual(grid.clusterKey(),-1)
            self.assertEqual(grid._Grid__change,0)
        #case2:3-15的grid依然是NORMAL
        for i in range(3,15):
            key = keys[i]
            grid = gridList.getGrid(key)
            self.assertGreater(grid._Grid_density,0)
            self.assertEqual(grid.sparseStatus(),SparseStatus.NORMAL)
            self.assertEqual(grid.densityStatus(),DensityStatus.SPARSE)
        for i in range(15,21):
            key = keys[i]
            grid = gridList.getGrid(key)
            self.assertEqual(grid.sparseStatus,SparseStatus.TODELETE)
            self.assertEqual(grid.densityStatus(),DensityStatus.SPARSE)
            self.assertNotEqual(grid.density(),0)
            self.assertNotEqual(grid.time_remove(),time)





