import sys
sys.path.append("..")

import unittest
from GridList import *
from Grid import *
class TestGridList(unittest.TestCase):

    def test_getGrid(self):
        gridList=GridList()
        #case1:key不存在，抛出KeyError
        rawData=HelperForTest.randomLegalRawData()
        gridList.addNewData(rawData,1)
        raw=HelperForTest.anotherKeyRawdataFromKey(rawData)
        k=Helper.getKeyFromRawData(raw)
        with self.assertRaises(KeyError):
            gridList.getGrid(k)
        k = Helper.getKeyFromRawData(rawData)
        gridList.addNewData(raw,4)
        gridList.delGrid(k,8)
        with self.assertRaisesRegex(KeyError,"still exist"):
            gridList.getGrid(k)
        #case2：key存在，得到正确的Grid
        gridList.addNewData(raw,48)
        grid=gridList.getGrid(k)
        self.assertEqual(grid.key(),k)


    def test_gridList(self):
        #测试gridlist存在且初始为空
        newGridList=GridList()
        self.assertEqual(0,len(newGridList._GridList__grid_list))

    def test_getNeighborGrids(self):
        gridList=GridList()
        #case1:gridKey不存在时的异常抛出
        raw=HelperForTest.randomLegalRawData()
        key=Helper.getKeyFromRawData(raw)
        with self.assertRaises(KeyError):
            gridList.getNeighborGrids(key)
        #case1-1:gridKeys存在但刚被删除
        gridList.addNewData(rawData=raw,time=1)
        gridList.delGrid(key,2)
        with self.assertRaisesRegex(KeyError,"still exist"):
            gridList.getNeighborGrids(key)
        #case2:gridKey存在但当前没有其他Neighbor时返回的空值
        gridList.addNewData(rawData=raw,time=4)
        ret=gridList.getNeighborGrids(key)
        self.assertListEqual(ret,[])
        #case3:gridKey存在且Neighbor也存在但是不满时
        neighbor_keys=Helper.getNeighborKeys(key)
        count=0
        for k in neighbor_keys:
            g=Grid()
            g._Grid__key=k
            gridList._GridList__grid_list[k]=g
            count+=1
            if 3==count:
                break
        grids=gridList.getNeighborGrids(key)
        self.assertEqual(len(grids),3)
        for grid in grids:
            self.assertTrue(grid.key() in neighbor_keys)
        #case4:gridKey存在且Neighbor也存在且有6个
        neighbor_keys = Helper.getNeighborKeys(key)
        for k in neighbor_keys:
            g = Grid()
            g._Grid__key = k
            gridList._GridList__grid_list[k] = g
        grids = gridList.getNeighborGrids(key)
        self.assertEqual(len(grids), 6)
        for grid in grids:
            self.assertTrue(grid.key() in neighbor_keys)
    def test_addNewData(self):
        #case1：对应grid不存在，添加data
        gridList=GridList()
        raw=HelperForTest.randomLegalRawData()
        key=Helper.getKeyFromRawData(raw)
        gridList.addNewData(raw,1)
        grid=gridList.getGrid(key)
        self.assertEqual(key,grid.key())


    def test_getDenseGrids(self):
        #case1:list中没有dense的grid，但有其他两种grid。返回空值
        gridList=GridList()
        raw1=HelperForTest.randomLegalRawData()
        g1=Grid()
        g1.addData(raw1,1)
        g1._Grid__densityStatus=DensityStatus.TRANSITIONAL
        raw2=HelperForTest.anotherKeyRawdataFromKey(rawData=raw1)
        k1=Helper.getKeyFromRawData(raw1)
        g2=Grid()
        g2.addData(raw2,8)
        g2._Grid__densityStatus=DensityStatus.SPARSE
        k2=Helper.getKeyFromRawData(raw2)
        gridList._GridList__grid_list[k1]=g1
        gridList._GridList__grid_list[k2]=g2
        ret=gridList.getDenseGrids()
        self.assertListEqual(ret,[])

        #case2：list中有Dense，且有其他两种grid，返回正确的grid
        raw3 = HelperForTest.randomLegalRawData()
        g3 = Grid()
        g3.addData(raw1,16)
        g3._Grid__densityStatus = DensityStatus.DENSE
        k3 = Helper.getKeyFromRawData(raw1)
        raw4 = HelperForTest.randomLegalRawData()
        g4 = Grid()
        g4.addData(raw4,32)
        g4._Grid__densityStatus = DensityStatus.DENSE
        k4 = Helper.getKeyFromRawData(raw4)
        gridList._GridList__grid_list[k3] = g3
        gridList._GridList__grid_list[k4] = g4
        #case3：list中全是dense，返回整个list
        ret=gridList.getDenseGrids()
        self.assertEqual(len(ret),2)
        for grid in ret:
            self.assertIn(grid.key(),[k3,k4])

    def test_getChangeGrids(self):
        #case1：list中没有change的grid，返回空值
        gridList=GridList()
        ret=gridList.getChangeGrids()
        self.assertListEqual(ret,[])
        #case2：list中有change，返回对应change，检查数量是否正确
        time=1
        for i in range(1,100):
            raw=HelperForTest.randomLegalRawData()
            gridList.addNewData(raw,time)
            time+=random.randint(1,1000)
        count = 0
        gridList.clearChangeFlag()
        for k in gridList._GridList__grid_list:
            grid=gridList._GridList__grid_list[k]
            grid._Grid__change=1
            count+=1
            if count == 5:
                break
        change_grids=gridList.getChangeGrids()
        self.assertEqual(5,len(change_grids))
        for grid in change_grids:
            self.assertEqual(grid.change(),1)


    def test_delGrid(self):
        gridList=GridList()
        #case1:list中不存在对应grid，抛出异常
        raw=HelperForTest.randomLegalRawData()
        key=Helper.getKeyFromRawData(raw)
        with self.assertRaises(KeyError):
            gridList.delGrid(key,1)
        #case2：list中有目标grid，检查调用函数后grid是否数据被清空且remove_time是否正确
        gridList.addNewData(raw,2)
        gridList.delGrid(key,3)
        with self.assertRaisesRegex(KeyError,"still exist"):
            gridList.getGrid(key)

    def test_clearChangeFlag(self):
        gridList=GridList()
        #case1:list为空，调用
        gridList.clearChangeFlag()
        #case2:list不为空，但change全为0，调用
        time=1
        for i in range(1,1000):
            raw=HelperForTest.randomLegalRawData()
            gridList.addNewData(raw,time)
            time+=random.randint(1,1000)
        gridList.clearChangeFlag()
        for k in gridList._GridList__grid_list:
            grid=gridList._GridList__grid_list[k]
            self.assertEqual(0,grid._Grid__change)
        #case3:list的change为1
        time=1
        for i in range(1,1000):
            raw=HelperForTest.randomLegalRawData()
            gridList.addNewData(raw,time)
            time+=random.randint(1,1000)
        gridList.clearChangeFlag()
        for k in gridList._GridList__grid_list:
            grid=gridList._GridList__grid_list[k]
            grid._Grid__change=1
        gridList.clearChangeFlag()
        for k in gridList._GridList__grid_list:
            grid=gridList._GridList__grid_list[k]
            self.assertEqual(0,grid._Grid__change)

    def test_judgeAndremoveSporadic(self):
        #case1:list中没有Sparse的grid，调用后检查各个grid的状态的remove_time，没有变化且gird的数量没有变化
        gridList=GridList()
        self.assertEqual(0,len(gridList._GridList__grid_list))
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
        for k in gridList._GridList__grid_list:
            grid=gridList._GridList__grid_list[k]
            self.assertEqual(grid._Grid__time_remove,0)
            self.assertEqual(len(gridList._GridList__grid_list),length)

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
        length=len(gridList._GridList__grid_list)
        keys=list(gridList._GridList__grid_list.keys())
        #3 TODELETE
        for i in range(0,3):
            k=keys[i]
            grid=gridList.getGrid(k)
            grid._Grid__densityStatus=DensityStatus.SPARSE
            grid._Grid__sparseStatus=SparseStatus.TODELETE
        #===============3 s1 not s2 NORMAL====================
        #s1:grid_object.densityThreshold()>grid_object.density(current_time)
        #s2:current_time>=(1+Helper().beta)*grid_object.time_remove()
        for i in range(3, 6):
            k = keys[i]

            grid = gridList.getGrid(k)
            grid._Grid__densityStatus = DensityStatus.SPARSE
            grid._Grid__sparseStatus = SparseStatus.NORMAL
            # 使不符合s2，公式同上（s2需要修改time_remove,而s1中的Th需要用到time_remove,顾先改s2）
            grid._Grid__time_remove=time/(1+Helper().beta)+i
            #使符合s1，公式是自己推导出来的
            if not Helper().lamb**(time-grid._Grid__time_update)==0:
                grid._Grid_density=grid.densityThreshold(time)/(Helper().lamb**(time-grid._Grid__time_update))-i


        for i in range(6, 9):
            k = keys[i]
            grid = gridList.getGrid(k)
            grid._Grid__densityStatus = DensityStatus.SPARSE
            grid._Grid__sparseStatus = SparseStatus.TEMP
            # 使不符合s2，公式同上（s2需要修改time_remove,而s1中的Th需要用到time_remove,顾先改s2）
            grid._Grid__time_remove=time/(1+Helper().beta)+i
            #使符合s1，公式是自己推导出来的
            if not Helper().lamb**(time-grid._Grid__time_update)==0:
                grid._Grid_density=grid.densityThreshold(time)/(Helper().lamb**(time-grid._Grid__time_update))-i
        #=================s2 not s1===================
        for i in range(9, 12):
            k = keys[i]
            grid = gridList.getGrid(k)
            grid._Grid__densityStatus = DensityStatus.SPARSE
            grid._Grid__sparseStatus = SparseStatus.NORMAL
            # 使符合s2，公式同上（s2需要修改time_remove,而s1中的Th需要用到time_remove,顾先改s2）
            grid._Grid__time_remove=time/(1+Helper().beta)-i
            #使不符合s1，公式是自己推导出来的
            grid._Grid__time_update = time
            grid._Grid__density = (grid.densityThreshold(time) / (Helper().lamb)) * Helper().lamb
            grid._Grid__density += i

            assert grid.densityThreshold(time) < grid.densityWithTime(time)
        for i in range(12, 15):
            k = keys[i]
            grid = gridList.getGrid(k)
            grid._Grid__densityStatus = DensityStatus.SPARSE
            grid._Grid__sparseStatus = SparseStatus.TEMP
            # 使符合s2，公式同上（s2需要修改time_remove,而s1中的Th需要用到time_remove,顾先改s2）
            grid._Grid__time_remove=time/(1+Helper().beta)-i
            #使不符合s1，公式是自己推导出来的
            grid._Grid__time_update=time
            grid._Grid__density=(grid.densityThreshold(time)/(Helper().lamb))*Helper().lamb
            grid._Grid__density+=i

            assert grid.densityThreshold(time) < grid.densityWithTime(time)
        #======s1 and s2===============
        for i in range(15, 18):
            k = keys[i]
            grid = gridList.getGrid(k)
            grid._Grid__densityStatus = DensityStatus.SPARSE
            grid._Grid__sparseStatus = SparseStatus.TEMP
            # 使符合s2，公式同上（s2需要修改time_remove,而s1中的Th需要用到time_remove,顾先改s2）
            grid._Grid__time_remove=time/(1+Helper().beta)-i

            assert time >= (1 + Helper().beta) * grid.time_remove()
            #使符合s1，公式是自己推导出来的

            grid._Grid__time_update = time
            grid._Grid__density = (grid.densityThreshold(time) / (Helper().lamb)) / 2
            assert grid.densityThreshold(time) > grid.densityWithTime(time)
        for i in range(18, 21):
            k = keys[i]
            grid = gridList.getGrid(k)
            grid._Grid__densityStatus = DensityStatus.SPARSE
            grid._Grid__sparseStatus = SparseStatus.NORMAL
            # 使符合s2，公式同上（s2需要修改time_remove,而s1中的Th需要用到time_remove,顾先改s2）
            grid._Grid__time_remove=time/(1+Helper().beta)-i
            assert time >= (1 + Helper().beta) * grid.time_remove()
            #使符合s1，公式是自己推导出来的

            grid._Grid__time_update = time
            grid._Grid__density = (grid.densityThreshold(time) / (Helper().lamb)) / 2
            assert grid.densityThreshold(time) > grid.densityWithTime(time)
        #被归入
        gridList.judgeAndremoveSporadic(time)
        #case1：3个TODELTE被删除
        for i in range(0,3):
            key=keys[i]
            grid=gridList._GridList__grid_list[key]
            self.assertEqual(grid.sparseStatus(),SparseStatus.NORMAL)
            self.assertEqual(grid.time_remove(),time)
            self.assertEqual(grid.density(),0)
            self.assertEqual(grid.clusterKey(),-1)
            self.assertEqual(grid._Grid__change,0)
        #case2:3-15的grid依然是NORMAL
        for i in range(3,15):
            key = keys[i]
            grid = gridList.getGrid(key)
            self.assertGreater(grid.density(),0)
            self.assertEqual(grid.sparseStatus(),SparseStatus.NORMAL)
            self.assertEqual(grid.densityStatus(),DensityStatus.SPARSE)
        for i in range(15,21):
            key = keys[i]
            grid = gridList.getGrid(key)
            self.assertEqual(grid.sparseStatus(),SparseStatus.TODELETE)
            self.assertEqual(grid.densityStatus(),DensityStatus.SPARSE)
            self.assertNotEqual(grid.density(),0)
            self.assertNotEqual(grid.time_remove(),time)


if __name__=="__main__":
    unittest.main()


