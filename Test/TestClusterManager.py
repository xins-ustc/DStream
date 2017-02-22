import sys
sys.path.append("..")

from ClusterManager import *
import unittest


from Grid import *
from Cluster import *
from HelperForTest import *

class TestClusterManager(unittest.TestCase):
    def test_init(self):
        #检查初始值是否正确
        manager=ClusterManager()
        self.assertEqual(len(manager._ClusterManager__cluster_dic),0)
        self.assertEqual(manager._ClusterManager__cluster_key_index,0)


    def test_getCluster(self):
        #Tcluster不存在，抛出异常
        manager = ClusterManager()
        with self.assertRaises(KeyError):
            manager.getCluster(1)
        #cluster存在，获取正确
        grid=Grid()
        grid._Grid__key=345
        manager.addNewCluster(grid)
        clus=manager.getCluster(1)
        grids=clus.getAllGrids()
        self.assertEqual(len(grids),1)
        self.assertEqual(grids[345]._Grid__key,345)

    def test_addNewCluster(self):
        #添加成功且能找到该新cluster包含这枚grid
        manager=ClusterManager()
        grid1=Grid()
        grid2=Grid()
        grid1._Grid__key=123
        grid2._Grid__key=456
        manager.addNewCluster(grid1)
        manager.addNewCluster(grid2)
        self.assertEqual(manager._ClusterManager__cluster_key_index,2)
        clusters=manager.getAllCluster()
        self.assertEqual(len(clusters),2)
        self.assertEqual(1,grid1.clusterKey())
        self.assertEqual(2,grid2.clusterKey())


    def test_getNeighborClusters(self):
        #将一个grid的neighbor的cluster的数组返回
            #一个grid，其周围的grid都属于其他cluster
        raw=HelperForTest.randomLegalRawData()
        key=Helper.getKeyFromRawData(raw)
        grid=Grid()
        grid.addData(raw,1)
        keys=Helper.getNeighborKeys(key)
        manager=ClusterManager()
        manager.addNewCluster(grid)
        for k in keys:
            g=Grid()
            g._Grid__key=k
            manager.addNewCluster(grid)
        #====#获取该grid周围的cluster
        clusters=manager.getNeighborClusters(grid)
        for cluster in clusters:
            grids=cluster.getAllGrids()
            grid=grids[0]
            self.assertIn(grid.key(),keys)



        #添加一个grid，grid属于本cluster，不会get到自己
        manager = ClusterManager()
        g=Grid()
        g._Grid__key='1001100100'
        manager.addNewCluster(g)
        cluster=manager.getCluster(1)
        g1=Grid()
        g1._Grid__key="1002100100"
        cluster.addGrid(g1)
        clusters=manager.getNeighborClusters(g)
        self.assertEqual(0,len(clusters))


    def test_getAllCluster(self):
        #TODO:检查cluster是否完整
        manager=ClusterManager()
        a=manager.getAllCluster()
        self.assertEqual(0,len(a))

        grid=Grid()
        grid._Grid__key=123
        manager.addNewCluster(grid)
        clusters=manager.getAllCluster()
        self.assertEqual(1,len(clusters))
        cluster=clusters[1]
        grids=cluster.getAllGrids()
        grid=grids[123]
        self.assertEqual(grid.key(),123)


    def test_mergeCluster(self):
        manager = ClusterManager()
        cluster1 = Cluster(1)
        manager._ClusterManager__cluster_key_index+=1
        manager._ClusterManager__cluster_dic[1]=cluster1

        self.assertEqual(-1,manager.mergeCluster(1,1))
        #检查merge是否正确
            #建3个cluster。然后调用函数。源cluster包含全部grid，目标cluster不存在
        manager=ClusterManager()
        cluster1=Cluster(1)
        grid=Grid()
        grid._Grid__key=1
        cluster1.addGrid(grid)
        cluster2=Cluster(2)
        grid2=Grid()
        grid2._Grid__key=2
        cluster2.addGrid(grid2)
        cluster3=Cluster(3)
        grid3=Grid()
        grid3._Grid__key=3
        cluster3.addGrid(grid3)
        manager._ClusterManager__cluster_dic[1]=cluster1
        manager._ClusterManager__cluster_dic[2]=cluster2
        manager._ClusterManager__cluster_dic[3]=cluster3
        manager._ClusterManager__cluster_key_index=3
        manager.mergeCluster(1,2)
        with self.assertRaises(KeyError):
            manager.getCluster(2)
        cluster1=manager.getCluster(1)
        self.assertEqual(2,cluster1.size())
        grids=cluster1.getAllGrids()
        for k in grids:
            grid = grids[k]
            self.assertIn(grid.key(),[1,2])
        cluster3=manager.getCluster(3)
        cluster3.getGrid(3)
        self.assertEqual(2,len(manager.getAllCluster()))

    def test_splitCluster(self):
        #TODO:检查切割是否正确
        manager=ClusterManager()
        grid=Grid()
        grid._Grid__key=Helper.getKey(1,1,1)
        manager.addNewCluster(grid)

        cluster1=manager.getCluster(1)
        grid2=Grid()
        grid2._Grid__key=Helper.getKey(60,3,30)
        cluster1.addGrid(grid2)
        #
        # grid3=Grid()
        # grid3._Grid__key=Helper.getKey(90,6,60)
        # cluster1.addGrid(grid3)
        #
        # grid4=Grid()
        # grid4._Grid__key=Helper.getKey(180,9,90)
        # cluster1.addGrid(grid4)

        manager.splitCluster(1)



        self.assertEqual(2,len(manager._ClusterManager__cluster_dic))

    # def test_clearEmptyCluster(self):
    #     manager=ClusterManager()
    #     manager._ClusterManager.__cluster_dic[1]=Cluster()
    #     c=Cluster(2)
    #     g=Grid()
    #     c.addGrid(g)
    #     manager._ClusterManager.__cluster_dic[2]=c
    #     self.assertEqual(2,len(manager.getAllCluster()))
    #     manager.clearEmptyCluseter()
    #     self.assertEqual(1,len(manager.getAllCluster()))

if __name__ =="__main__":
    unittest.main()


