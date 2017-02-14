import unittest
import sys
sys.path.append("..")

from  Cluster import *
from Grid import *
class TestCluster(unittest.TestCase):
    def test_init(self):
        #测试是否初始化后各成员正确
        cluster=Cluster(345)
        self.assertEqual(cluster._Cluster__key,345)
        self.assertEqual(len(cluster._Cluster__grid_dic),0)
    def test_getGrid(self):

        #case1:key不存在，抛出异常
        cluster=Cluster(1)
        with self.assertRaises(KeyError):
            cluster.getGrid(1)
        #case2：grid存在得到对应的Grid
        grid=Grid()
        cluster.addGrid(grid)
        g=cluster.getGrid(grid.key())
        self.assertEqual(grid.key(),g.key())
    def test_key(self):
        cluster=Cluster(234235)
        self.assertEqual(cluster.key(),234235)

    def test_isGridExist(self):

        #case1:存在返回False
        cluster=Cluster(1)
        grid=Grid()
        grid._Grid__key=342
        self.assertFalse(cluster.isGridExist(grid))
        #case2：不存在返回True
        cluster.addGrid(grid)
        self.assertTrue(cluster.isGridExist(grid))

    def test_isGridExistWithKey(self):
        # case1:存在返回True
        cluster=Cluster(1)
        self.assertFalse(cluster.isGridExistWithKey(1))
        # case2：不存在返回false
        grid=Grid()
        grid._Grid__key=1
        cluster.addGrid(grid)
        self.assertTrue(cluster.isGridExistWithKey(1))

    def test_addGrid(self):
        #case1:grid key<0抛出异常
        cluster=Cluster(1)
        grid=Grid()
        grid._Grid__key=-234
        with self.assertRaises(KeyError):
            cluster.addGrid(grid)
        #case2:grid已存在加入抛出异常
        grid=Grid()
        grid._Grid__key=1
        cluster.addGrid(grid)
        with self.assertRaisesRegex(Exception,"存在"):
            cluster.addGrid(grid)
        #case3:grid正确加入
        self.assertEqual(cluster.size(),1)
        gird=cluster.getGrid(1)
        self.assertEqual(grid._Grid__key,1)






    def test_delGrid(self):
        #case1:key不存在，抛出异常
        cluster=Cluster(1)
        with self.assertRaises(KeyError):
            grid=Grid()
            grid._Grid__key=23
            cluster.delGrid(grid)
        #case2：key存在，正确删除
        grid=Grid()
        grid._Grid__key=343
        cluster.addGrid(grid)
        cluster.delGrid(grid)
        self.assertEqual(0,cluster.size())
    def test_isOutsideGrid(self):
        #case1:grid不在cluster里，抛出异常
        cluster=Cluster(1)
        g=Grid()
        with self.assertRaises(KeyError):
            cluster.isOutsideGrid(g)
        #case2：grid在cluster里，但不是Outside，返回false
        cluster = Cluster(1)
        g = Grid()
        g.addData(HelperForTest.randomLegalRawData(),1)
        neighbors_key=Helper.getNeighborKeys(g.key())
        cluster.addGrid(g)
        for key in neighbors_key:
            item = Grid()
            item._Grid__key=key
            cluster.addGrid(item)
        self.assertFalse(cluster.isOutsideGrid(g))
        #case3：grid在cluster里且是Outside，返回true
        cluster = Cluster(1)
        g = Grid()
        g.addData(HelperForTest.randomLegalRawData(),1)
        neighbors_key=Helper.getNeighborKeys(g.key())
        cluster.addGrid(g)
        count=0
        for key in neighbors_key:
            item = Grid()
            item._Grid__key=key
            cluster.addGrid(item)
            count+=1
            if count==3:
                break
        self.assertTrue(cluster.isOutsideGrid(g))


    def test_size(self):
        #case1:返回正确的size
        cluster=Cluster(1)
        self.assertEqual(len(cluster._Cluster__grid_dic),cluster.size())
        for i in range(1,10):
            grid=Grid()
            grid._Grid__key=i
            cluster.addGrid(grid)
        self.assertEqual(len(cluster._Cluster__grid_dic), cluster.size())

    def test_isOutsideIfAdd(self):
        #case0:grid已存在，抛出异常
        cluster=Cluster(1)
        g=Grid()
        raw=HelperForTest.randomLegalRawData()
        g.addData(raw,1)
        cluster.addGrid(g)
        with self.assertRaises(KeyError):
            cluster.isOutsideIfAdd(g)
        #case1:加入后是OutSide，返回True
            cluster = Cluster(1)
            g = Grid()
            g.addData(HelperForTest.randomLegalRawData(), 1)
            neighbors_key = Helper.getNeighborKeys(g.key())
            count = 0
            for key in neighbors_key:
                item = Grid()
                item._Grid__key = key
                cluster.addGrid(item)
                count += 1
                if count == 3:
                    break
            self.assertTrue(cluster.isOutsideIfAdd(g))
        #case2：加入后不是OutSide，返回False
        cluster = Cluster(1)
        g = Grid()
        g.addData(HelperForTest.randomLegalRawData(), 1)
        neighbors_key = Helper.getNeighborKeys(g.key())
        for key in neighbors_key:
            item = Grid()
            item._Grid__key = key
            cluster.addGrid(item)
        self.assertFalse(cluster.isOutsideIfAdd(g))

    def test_isClusterSingle(self):
        #case1：构造单一Cluster，返回True
        cluster = Cluster(1)
        raw=HelperForTest.randomLegalRawData()
        g=Grid()
        g.addData(raw,1)
        cluster.addGrid(g)
        key=Helper.getKeyFromRawData(raw)
        keys=Helper.getNeighborKeys(key)
        for k in keys:
            g=Grid()
            g._Grid__key=k
            cluster.addGrid(g)
        self.assertTrue(cluster.isClusterSingle())

        #case2：构造分离Cluster，返回False
            #构造4个远离的点，填充其neighbor
        cluster = Cluster(2)
        fourPoints=[(1,1,1),(60,3,30),(90,6,60),(180,9,90)]
        for tu in fourPoints:
            grid=Grid()
            grid._Grid__key=Helper.getKey(pw=tu[0],rf=tu[1],doa=tu[2])
            cluster.addGrid(grid)
            neiborkey=Helper.getNeighborKeys(Helper.getKey(pw=tu[0],rf=tu[1],doa=tu[2]))
            for k in neiborkey:
                g=Grid()
                g._Grid__key=k
                cluster.addGrid(g)

        self.assertFalse(cluster.isClusterSingle())







    def test_getAllGrids(self):
        #case1：返回本Cluster的所有Grids
        cluster=Cluster(1)
        grid_dic=cluster.getAllGrids()
        self.assertEqual(len(grid_dic),len(cluster._Cluster__grid_dic))
        for i in range(1,10):
            grid=Grid()
            grid._Grid__key=i
            cluster.addGrid(grid)
        grid_dic = cluster.getAllGrids()
        self.assertEqual(len(grid_dic), len(cluster._Cluster__grid_dic))


if __name__ =="__main__":
    unittest.main()
