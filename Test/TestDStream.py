from DStream import  *
from Helper import *
import unittest
import sys
sys.path.append("..")


class TestDStream(unittest.TestCase):
    def test_init(self):
        dstream=D_Stream()
        self.assertEqual(0,dstream.tc)
        self.assertEqual(Helper().gap(), dstream.gap)
        self.assertNotEqual(None,dstream.grid_list)
        self.assertNotEqual(None, dstream.cluster_manager)
    def test_adjust_sparse(self):
        #被删除的grid不存在
        dstream=D_Stream()
        grid=Grid()
        grid._Grid__key=1
        with self.assertRaises(KeyError):
            dstream._D_Stream__adjust_sparse(grid)
        #被删除的grid存在且其cluster是single
            #构造cluster
        cluster=Cluster(1)
        key=Helper.getKey(60,3,30)
        g=Grid()
        g._Grid__key=key
        cluster.addGrid(g)
        keys = Helper.getNeighborKeys(key)
        for k in keys:
            grid=Grid()
            grid._Grid__key=k
            cluster.addGrid(grid)
        manager=dstream._D_Stream__cluster_manager
        manager._ClusterManager__cluster_key_index=1
        manager._ClusterManager__cluster_dic[1]=cluster
        dstream._D_Stream__adjust_sparse(g)
        self.assertEqual(1,len(manager._ClusterManager__cluster_dic))
        #被删除的grid存在且删除grid后不是single
        cluster = Cluster(1)
        key = '1999232137'
        g = Grid()
        g._Grid__key = key
        cluster.addGrid(g)
        grid=Grid()
        grid._Grid__key='2000232137'
        cluster.addGrid(grid)
        grid = Grid()
        grid._Grid__key = '1998232137'
        cluster.addGrid(grid)
        manager = dstream._D_Stream__cluster_manager
        manager._ClusterManager__cluster_key_index = 1
        manager._ClusterManager__cluster_dic[1] = cluster
        dstream._D_Stream__adjust_sparse(g)
        self.assertEqual(2, len(manager._ClusterManager__cluster_dic))
    def test_adjust_dense_neighbor_dense(self):
        dstream = D_Stream()
        manager=dstream.cluster_manager
        #建立一个dense grid和一个邻居gird_h，grid_h是dense且grid的cluster不存在，验证是否g会在h的cluster里
        g=Grid()
        g._Grid__key='1001001001'
        h=Grid()
        h._Grid__key='1002001001'
        h._Grid__densityStatus=DensityStatus.DENSE
        manager.addNewCluster(h)
        dstream._D_Stream__adjust_dense_neighbor_dense(g,h)
        cluster=manager.getCluster(1)
        self.assertEqual(len(cluster.getAllGrids()),2)
        h1=cluster.getGrid('456')
        self.assertEqual(h1.key(),'456')
        #建立一个dense grid和一个邻居gird_h，g的cluster比h的大，验证h的cluster被g吞并
        dstream = D_Stream()
        manager = dstream.cluster_manager
        g=Grid()
        h=Grid()
        g._Grid__key='1002001001'
        h._Grid__key='1003001001'
        g._Grid__densityStatus=DensityStatus.DENSE
        manager.addNewCluster(g)
        manager.addNewCluster(h)
        cluster_g=manager.getCluster(1)
        g1=Grid()
        g1._Grid__key='1004001001'
        g2=Grid()
        g2._Grid__key='1003002001'
        cluster_g.addGrid(g1)
        cluster_g.addGrid(g2)
        dstream._D_Stream__adjust_dense_neighbor_dense(g, h)
        self.assertEqual(1,len(manager.getAllCluster()))
        clu=manager.getAllCluster()
        gs=clu.getAllGrids()
        for grid in gs:
            self.assertIn(grid.key(),['1002001001','1003001001','1004001001','1003002001'])
        #建立一个dense grid和一个邻居gird_h，h的cluster比g大，验证g的cluster 被h吞并
        dstream = D_Stream()
        manager = dstream.cluster_manager
        g = Grid()
        h = Grid()
        g._Grid__key = '1002001001'
        h._Grid__key = '1003001001'
        g._Grid__densityStatus = DensityStatus.DENSE
        manager.addNewCluster(g)
        manager.addNewCluster(h)
        cluster_h = manager.getCluster(2)
        h1 = Grid()
        h1._Grid__key = '1004001001'
        h2 = Grid()
        h2._Grid__key = '1003002001'
        cluster_h.addGrid(h1)
        cluster_h.addGrid(h2)
        dstream._D_Stream__adjust_dense_neighbor_dense(g, h)
        self.assertEqual(1, len(manager.getAllCluster()))
        clu = manager.getAllCluster()
        gs = clu.getAllGrids()
        for grid in gs:
            self.assertIn(grid.key(), ['1002001001', '1003001001', '1004001001', '1003002001'])

    def test_adjust_dense_neighbor_transitional(self):
        #另dense g没有cluster，且如果g加入到邻居h的cluster里，那么邻居h是一个outside，验证g在h的cluster里
        dstream = D_Stream()
        manager = dstream.cluster_manager
        g=Grid()
        g._Grid__key='1000100100'
        h=Grid()
        h._Grid__key='1001100100'
        manager.addNewCluster(h)
        h1=Grid()
        h1._Grid__key='1002100100'
        cluster=manager.getCluster(1)
        cluster.addGrid(h1)
        dstream._D_Stream__adjust_dense_neighbor_transitional(g,h)
        grids=cluster.getAllGrids()
        for grid in grids:
            self.assertIn(grid,['1000100100','1001100100','1002100100'])

        # TODO:另dense g没有cluster，且如果g加入到邻居h的cluster里，那么邻居h不是一个outside，验证g不在h的cluster里
        dstream = D_Stream()
        manager = dstream.cluster_manager
        g = Grid()
        g._Grid__key = '1000100100'
        h = Grid()
        h._Grid__key = '1001100100'
        manager.addNewCluster(h)
        h1 = Grid()
        h1._Grid__key = '1002100100'
        h2 = Grid()
        h2._Grid__key = '1001101100'
        h3 = Grid()
        h3._Grid__key = '1001099100'
        h4 = Grid()
        h4._Grid__key = '1001100099'
        h5 = Grid()
        h5._Grid__key = '1001100101'
        cluster = manager.getCluster(1)
        cluster.addGrid(h1)
        cluster.addGrid(h2)
        cluster.addGrid(h3)
        cluster.addGrid(h4)
        cluster.addGrid(h5)
        dstream._D_Stream__adjust_dense_neighbor_transitional(g, h)
        grids = cluster.getAllGrids()
        self.assertEqual(len(grids),6)
        for grid in grids:
            self.assertIn(grid, ['1001100100', '1002100100', '1001101100','1001099100','1001100099','1001100101'])
        self.assertEqual(-1,g._Grid__cluster_key)

                #TODO：另dense g有cluster且g的cluster比邻居h的cluster大

    def test_adjust_dense(self):
        #TODO:两个neighbor cluster，一大一小
        #TODO：不存在neighbor cluster

    def test_adjust_transitional(self):
        #TODO:transitional g，g没有neighbor cluster但有neighbor 验证g没变化
        #TODO:有neighbor cluster，但如果加入不是outside 验证g没被加入
        #TODO:有neighbor cluster，加入是outside，验证g被加入

    def test_initial_clustring(self):
        #TODO:1、布置100个不是neighbor的grid，运行函数不会报错
        #TODO:1-2、其中50个是dense，25个transitional，25个sparse，检查50个被分入各自cluster，但是其他50个没有cluster
        #TODO：2、10个互相隔离的cluster，运行函数后10个cluster没有变化
        #TODO：3、5个cluster，其中1和2接壤，1被2吞并，3和4接壤，4被3吞并、5的邻居有一个transitional的grid

    def test_do_DStream(self):
        #TODO:两个gap的数据量来做覆盖测试

