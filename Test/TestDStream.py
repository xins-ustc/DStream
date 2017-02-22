import sys
sys.path.append("..")
from DStream import  *
from Helper import *
import unittest
import logging
from HelperForTest import *



class TestDStream(unittest.TestCase):
    def test_init(self):
        logging.info("test_init")
        dstream=D_Stream()
        self.assertEqual(0,dstream.tc)
        self.assertEqual(Helper().gap(), dstream.gap)
        self.assertNotEqual(None,dstream.grid_list)
        self.assertNotEqual(None, dstream.cluster_manager)
    def test_adjust_sparse(self):
        logging.info("test_adjust_sparse")
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
        grid=None
        for k in keys:
            grid=Grid()
            grid._Grid__key=k
            cluster.addGrid(grid)
        manager=dstream.cluster_manager
        manager._ClusterManager__cluster_key_index=1
        manager._ClusterManager__cluster_dic[1]=cluster
        dstream._D_Stream__adjust_sparse(grid)
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
        manager = dstream.cluster_manager
        manager._ClusterManager__cluster_key_index = 1
        manager._ClusterManager__cluster_dic[1] = cluster
        dstream._D_Stream__adjust_sparse(g)
        self.assertEqual(2, len(manager._ClusterManager__cluster_dic))
    def test_adjust_dense_neighbor_dense(self):
        logging.info("test_adjust_dense_neighbor_dense")
        dstream = D_Stream()
        manager=dstream.cluster_manager
        #建立一个dense grid和一个邻居gird_h，grid_h是dense且grid的cluster不存在，验证g会在h的cluster里
        g=Grid()
        g._Grid__key='1001001001'
        g._Grid__densityStatus = DensityStatus.DENSE
        h=Grid()
        h._Grid__key='1002001001'
        h._Grid__densityStatus=DensityStatus.DENSE
        manager.addNewCluster(h)
        dstream._D_Stream__adjust_dense_neighbor_dense(g,h)
        cluster=manager.getCluster(1)
        self.assertEqual(len(cluster.getAllGrids()),2)
        h1=cluster.getGrid('1001001001')
        self.assertEqual(h1.key(),'1001001001')




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
        clu=manager.getCluster(1)
        gs=clu.getAllGrids()
        for k in gs:
            grid=gs[k]
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
        clu = manager.getCluster(2)
        gs = clu.getAllGrids()
        for k in gs:
            grid=gs[k]
            self.assertIn(grid.key(), ['1002001001', '1003001001', '1004001001', '1003002001'])

    def test_adjust_dense_neighbor_transitional(self):
        logging.info("test_adjust_dense_neighbor_transitional")
        #另dense g没有cluster，且如果g加入到邻居h的cluster里，那么邻居h是一个outside，验证g在h的cluster里
        dstream = D_Stream()
        manager = dstream.cluster_manager
        g=Grid()
        g._Grid__densityStatus=DensityStatus.DENSE
        g._Grid__key='1000100100'
        manager
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

        #另dense g没有cluster，且如果g加入到邻居h的cluster里，那么邻居h不是一个outside，验证g不在h的cluster里
        dstream = D_Stream()
        manager = dstream.cluster_manager
        g = Grid()
        g._Grid__densityStatus=DensityStatus.DENSE
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

        #另dense g有cluster且g的cluster比邻居h的cluster大
        dstream = D_Stream()
        manager = dstream.cluster_manager
        g = Grid()
        g._Grid__densityStatus = DensityStatus.DENSE
        g._Grid__key = '1000100100'
        dstream.grid_list._GridList__grid_list[g.key()]=g
        h = Grid()
        h._Grid__key = '1001100100'
        dstream.grid_list._GridList__grid_list[h.key()] = h
        manager.addNewCluster(g)
        manager.addNewCluster(h)
        cluster1=manager.getCluster(1)
        g1=Grid()
        g1._Grid__key='1241241'
        cluster1.addGrid(g1)
        dstream.grid_list._GridList__grid_list[g1.key()] = g1
        dstream._D_Stream__adjust_dense_neighbor_transitional(g, h)
        grids=cluster1.getAllGrids()
        for k in grids:
            g=grids[k]
            self.assertIn(g.key(),['1000100100','1001100100','1241241'])



    def test_adjust_dense(self):
        logging.info("test_adjust_dense")
        #两个neighbor cluster，一大一小,其中h是dense
        dstream = D_Stream()
        grid_list=dstream.grid_list
        manager=dstream.cluster_manager
        g=Grid()
        g._Grid__key='1000100100'
        grid_list._GridList__grid_list[g.key()] = g
        c11=Grid()
        c11._Grid__key='1001100100'
        c12=Grid()
        c12._Grid__key='1002100100'
        cluster1=Cluster(1)
        cluster1.addGrid(c11)
        cluster1.addGrid(c12)
        manager._ClusterManager__cluster_dic[1]=cluster1
        manager._ClusterManager__cluster_key_index+=1
        grid_list._GridList__grid_list[c11.key()]=c11
        grid_list._GridList__grid_list[c12.key()]=c12

        c21 = Grid()
        c21._Grid__key = '1000101100'
        c21._Grid__densityStatus=DensityStatus.DENSE
        c22 = Grid()
        c22._Grid__key = '1000009100'
        c23 = Grid()
        c23._Grid__key = '1000009101'
        cluster2 = Cluster(2)
        cluster2.addGrid(c21)
        cluster2.addGrid(c22)
        cluster2.addGrid(c23)
        manager._ClusterManager__cluster_dic[2] = cluster1
        manager._ClusterManager__cluster_key_index += 1
        grid_list._GridList__grid_list[c21.key()] = c21
        grid_list._GridList__grid_list[c22.key()] = c22
        grid_list._GridList__grid_list[c23.key()] = c23
        self.assertEqual(0,dstream._D_Stream__adjust_dense(g))

        #两个neighbor cluster，一大一小,其中h是transitional
        dstream = D_Stream()
        grid_list = dstream.grid_list
        manager = dstream.cluster_manager
        g = Grid()
        g._Grid__key = '1000100100'
        grid_list._GridList__grid_list[g.key()] = g
        c11 = Grid()
        c11._Grid__key = '1001100100'
        c12 = Grid()
        c12._Grid__key = '1002100100'
        cluster1 = Cluster(1)
        cluster1.addGrid(c11)
        cluster1.addGrid(c12)
        manager._ClusterManager__cluster_dic[1] = cluster1
        manager._ClusterManager__cluster_key_index += 1
        grid_list._GridList__grid_list[c11.key()] = c11
        grid_list._GridList__grid_list[c12.key()] = c12

        c21 = Grid()
        c21._Grid__key = '1000101100'
        c21._Grid__densityStatus = DensityStatus.TRANSITIONAL
        c22 = Grid()
        c22._Grid__key = '1000009100'
        c23 = Grid()
        c23._Grid__key = '1000009101'
        cluster2 = Cluster(2)
        cluster2.addGrid(c21)
        cluster2.addGrid(c22)
        cluster2.addGrid(c23)
        manager._ClusterManager__cluster_dic[2] = cluster1
        manager._ClusterManager__cluster_key_index += 1
        grid_list._GridList__grid_list[c21.key()] = c21
        grid_list._GridList__grid_list[c22.key()] = c22
        grid_list._GridList__grid_list[c23.key()] = c23
        self.assertEqual(0,dstream._D_Stream__adjust_dense(g))

        #不存在neighbor cluster
        dstream = D_Stream()
        raw = HelperForTest.randomLegalRawData()
        key = Helper.getKeyFromRawData(raw)
        dstream.do_DStream(raw)
        grid = dstream.grid_list._GridList__grid_list[key]
        dstream._D_Stream__adjust_dense(grid)
        self.assertEqual(-1,dstream._D_Stream__adjust_dense(grid))

        #有neighbor但师neighbor没有cluster
        dstream = D_Stream()
        raw = HelperForTest.randomLegalRawData()
        key = Helper.getKeyFromRawData(raw)
        dstream.do_DStream(raw)
        grid = dstream.grid_list._GridList__grid_list[key]
        keys=Helper.getNeighborKeys(key)
        for k in keys:
            g=Grid()
            g._Grid__key=k
            dstream.grid_list._GridList__grid_list[k]=g
            break
        dstream._D_Stream__adjust_dense(grid)
        self.assertEqual(-2,dstream._D_Stream__adjust_dense(grid))



    def test_adjust_transitional(self):
        logging.info("test_adjust_transitional")
        #transitional g，g没有neighbor cluster但有neighbor 验证g没变化
        dstream = D_Stream()
        g=Grid()
        g._Grid__densityStatus=DensityStatus.TRANSITIONAL
        g._Grid__key='1000100100'
        h=Grid()
        h._Grid__key='1001100100'
        dstream._D_Stream__adjust_transitional(g)

        self.assertEqual(-1,g._Grid__cluster_key)




        #有neighbor cluster，但如果加入不是outside 验证g没被加入
        dstream = D_Stream()
        g = Grid()
        g._Grid__densityStatus = DensityStatus.TRANSITIONAL
        g._Grid__key = '1000100100'
        keys=Helper.getNeighborKeys(g.key())
        cluster1=Cluster(1)
        dstream.cluster_manager._ClusterManager__cluster_dic[1]=cluster1
        dstream.cluster_manager._ClusterManager__cluster_key_index+=1
        for k in keys:
            h=Grid()
            h._Grid__key=k
            cluster1.addGrid(h)
            dstream.grid_list._GridList__grid_list[k]=h


        dstream._D_Stream__adjust_transitional(g)
        self.assertEqual(-1, g._Grid__cluster_key)

        #有neighbor cluster，加入是outside，验证g被加入
        dstream = D_Stream()

        #g
        g = Grid()
        g._Grid__densityStatus = DensityStatus.TRANSITIONAL
        g._Grid__key = '1000100100'
        cluster2 = Cluster(2)
        cluster2.addGrid(g)
        dstream.grid_list._GridList__grid_list[g.key()] = g
        dstream.cluster_manager._ClusterManager__cluster_dic[2] = cluster2

        #cluster1
        cluster1 = Cluster(1)
        keys = Helper.getNeighborKeys(g.key())
        dstream.cluster_manager._ClusterManager__cluster_dic[1] = cluster1

        #index
        dstream.cluster_manager._ClusterManager__cluster_key_index=2

        #for
        for k in keys:
            h = Grid()
            h._Grid__key = k
            cluster1.addGrid(h)
            dstream.grid_list._GridList__grid_list[k] = h
            break

        #test
        dstream._D_Stream__adjust_transitional(g)
        self.assertEqual(1, g._Grid__cluster_key)
        self.assertEqual(1,len(dstream.cluster_manager.getAllCluster()))



    def test_initial_clustring(self):
        logging.info("test_initial_clustring")
        #1、布置100个不是neighbor的grid，运行函数不会报错
        logging.debug("case1 begin")
        dstream=D_Stream()
        k='100100'
        for i in range(1,100):
            k=int(k)+3000000
            g=Grid()
            g._Grid__key=str(k)
            dstream.grid_list._GridList__grid_list[k]=g
        dstream._D_Stream__initial_clustring()
        k='100100'
        for i in range(1,100):
            k=int(k)+3000000
            grid=dstream.grid_list._GridList__grid_list[k]
            self.assertEqual(grid.clusterKey(),-1)
        logging.debug("case1 done")
        #1-2、其中50个是dense，25个transitional，25个sparse，检查50个被分入各自cluster，但是其他50个没有cluster
        logging.debug("case1-2 begin")
        dstream = D_Stream()
        k = '100100'
        for i in range(1, 100):
            k = str(int(k) + 3000000)
            g = Grid()
            g._Grid__key = k
            dstream.grid_list._GridList__grid_list[k] = g
            if i<50:
                g._Grid__densityStatus=DensityStatus.DENSE
            elif i<75:
                g._Grid__densityStatus = DensityStatus.TRANSITIONAL
            else:
                g._Grid__densityStatus = DensityStatus.SPARSE
        dstream._D_Stream__initial_clustring()
        k = '100100'
        for i in range(1, 100):
            k = str(int(k) + 3000000)
            grid=dstream.grid_list._GridList__grid_list[k]
            if i < 50:
                self.assertNotEqual(-1,grid.clusterKey())
            else:
                self.assertEqual(-1, grid.clusterKey())
        logging.debug("case1-2  done")

        #2、10个互相隔离的cluster，运行函数后10个cluster没有变化
        logging.debug("case2 begin")
        dstream = D_Stream()
        index=0
        key='100100'
        for i in range(0,10):
            index+=1
            key=str(int(key)+5000000)
            g=Grid()
            g._Grid__key=key
            g._Grid__densityStatus=DensityStatus.DENSE
            dstream.grid_list._GridList__grid_list[key]=g
            n_keys=Helper.getNeighborKeys(key)
            for n_key in n_keys:
                n_grid=Grid()
                n_grid._Grid__key=n_key
                n_grid._Grid__densityStatus=DensityStatus.TRANSITIONAL
                dstream.grid_list._GridList__grid_list[n_key]=n_grid
        dstream._D_Stream__initial_clustring()
        clusters=dstream.cluster_manager.getAllCluster()
        for k in clusters:
            cluster=clusters[k]
            self.assertEqual(7,cluster.size())
        self.assertEqual(10,len(clusters))

        logging.debug("case2 done")
        #3、5个cluster，其中1和2接壤，1被2吞并，3和4接壤，4被3吞并、4的邻居有一个transitional的grid 5 ，被4吞并
        logging.debug("case3 begin")

        dstream = D_Stream()

        g=Grid()
        g._Grid__key='100100'
        g._Grid__densityStatus=DensityStatus.DENSE

        dstream.grid_list._GridList__grid_list[g.key()]=g



        g=Grid()
        g._Grid__key='1100100'
        g._Grid__densityStatus=DensityStatus.DENSE

        g1=Grid()
        g1._Grid__key='1100101'
        g1._Grid__densityStatus=DensityStatus.TRANSITIONAL

        g2 = Grid()
        g2._Grid__key = '1100102'
        g2._Grid__densityStatus=DensityStatus.TRANSITIONAL

        g3 = Grid()
        g3._Grid__key = '1100103'
        g3._Grid__densityStatus = DensityStatus.TRANSITIONAL

        dstream.grid_list._GridList__grid_list[g.key()] = g
        dstream.grid_list._GridList__grid_list[g1.key()] = g1
        dstream.grid_list._GridList__grid_list[g2.key()] = g2
        dstream.grid_list._GridList__grid_list[g3.key()] = g3




        g = Grid()
        g._Grid__key = '1000100100'
        g._Grid__densityStatus=DensityStatus.DENSE

        g1 = Grid()
        g1._Grid__key = '1001100100'
        g1._Grid__densityStatus=DensityStatus.TRANSITIONAL

        dstream.grid_list._GridList__grid_list[g.key()] = g
        dstream.grid_list._GridList__grid_list[g1.key()] = g1





        g = Grid()
        g._Grid__key = '999100100'
        g._Grid__densityStatus=DensityStatus.DENSE

        dstream.grid_list._GridList__grid_list[g.key()] = g



        h=Grid()
        h._Grid__key='1002100100'
        h._Grid__densityStatus=DensityStatus.TRANSITIONAL
        dstream.grid_list._GridList__grid_list[h.key()] = h


        logging.debug("case3 init done and cluster_key_index is "+str(dstream.cluster_manager._ClusterManager__cluster_key_index)+" cluster num is "+str(len(dstream.cluster_manager.getAllCluster())))

        dstream._D_Stream__initial_clustring()
            #运行函数后，只剩下两个cluster
        clusters=dstream.cluster_manager.getAllCluster()
        self.assertEqual(2,len(clusters))

        cluster2=None
        cluster4=None
        for k in clusters:
            c=clusters[k]
            if c.size()==5:
                cluster2=c
            else :
                cluster4=c

        grids=cluster2.getAllGrids()
        for k in grids:
            self.assertIn(k,['100100','1100100','1100101','1100102','1100103'])
        grids=cluster4.getAllGrids()
        for k in grids:
            self.assertIn(k,['1000100100','1001100100','999100100','1002100100'])
        logging.debug("case3 done")
        logging.info("test_initial_clustring is done!")

    # def test_do_DStream(self):
    #     #两个gap的数据量来做覆盖测试
    #     dstream=D_Stream()
    #     gap=Helper().gap()
    #     for i in range(0,2*gap):
    #         raw=HelperForTest.randomLegalRawData()
    #         dstream.do_DStream(raw)
    #     self.assertEqual(2*gap,dstream.tc)


    def test_judgeAndremoveSporadic(self):
        logging.info("test_judgeAndremoveSporadic")
        #case1:list中没有Sparse的grid，调用后检查各个grid的状态的remove_time，没有变化且gird的数量没有变化
        logging.debug("case1")
        d=D_Stream()
        # gridList=GridList()
        self.assertEqual(0,len(d.grid_list._GridList__grid_list))
        time=0
        for i in range(1,100):
            time+=random.randint(1,10000)
            raw=HelperForTest.randomLegalRawData()
            key=Helper.getKeyFromRawData(raw)
            g=Grid()
            g.addData(raw,time)
            g._Grid__densityStatus=DensityStatus.DENSE
            d.grid_list._GridList__grid_list[key]=g
        d.judgeAndremoveSporadic(time+random.randint(1,10000))
        length=len(d.grid_list._GridList__grid_list)
        for k in d.grid_list._GridList__grid_list:
            grid=d.grid_list._GridList__grid_list[k]
            self.assertEqual(grid._Grid__time_remove,0)
            self.assertEqual(len(d.grid_list._GridList__grid_list),length)

        #case2：list中有Sparse，Dense和Transitional，调用后，Dense和Transitional的数量不变，
                # Sparse的数量也不变，且Sparse中TODELETE的状态全部被处理
                # 3个3个TODELETE，3个符合s1但不符合s2的NORMAL和3个同类TEMP，3个符合s2但不符合s1的NORMAL和同类TEMP,3个符合s1和s2的TEMP，3个符合s1和s2的NORMAL
        # d.grid_list = GridList()
        logging.debug("case2")
        d = D_Stream()
        for i in range(1, 1000):
            time += random.randint(1, 10000)
            raw = HelperForTest.randomLegalRawData()
            key = Helper.getKeyFromRawData(raw)
            g = Grid()
            g.addData(raw, time)
            g._Grid__densityStatus = DensityStatus.DENSE
            d.grid_list._GridList__grid_list[key] = g
        #由于是随机生成的，有可能重复，所以未必就是1000个
        time+=1
        length=len(d.grid_list._GridList__grid_list)
        keys=list(d.grid_list._GridList__grid_list.keys())
        #3 TODELETE
        for i in range(0,3):
            k=keys[i]
            grid=d.grid_list.getGrid(k)
            grid._Grid__densityStatus=DensityStatus.SPARSE
            grid._Grid__sparseStatus=SparseStatus.TODELETE
        #===============3 s1 not s2 NORMAL====================
        #s1:grid_object.densityThreshold()>grid_object.density(current_time)
        #s2:current_time>=(1+Helper().beta)*grid_object.time_remove()
        for i in range(3, 6):
            k = keys[i]

            grid = d.grid_list.getGrid(k)
            grid._Grid__densityStatus = DensityStatus.SPARSE
            grid._Grid__sparseStatus = SparseStatus.NORMAL
            # 使不符合s2，公式同上（s2需要修改time_remove,而s1中的Th需要用到time_remove,顾先改s2）
            grid._Grid__time_remove=time/(1+Helper().beta)+i
            #使符合s1，公式是自己推导出来的
            if not Helper().lamb**(time-grid._Grid__time_update)==0:
                grid._Grid_density=grid.densityThreshold(time)/(Helper().lamb**(time-grid._Grid__time_update))-i


        for i in range(6, 9):
            k = keys[i]
            grid = d.grid_list.getGrid(k)
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
            grid = d.grid_list.getGrid(k)
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
            grid = d.grid_list.getGrid(k)
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
            grid = d.grid_list.getGrid(k)
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
            grid = d.grid_list.getGrid(k)
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
        d.judgeAndremoveSporadic(time)
        #case1：3个TODELTE被删除
        for i in range(0,3):
            key=keys[i]
            grid=d.grid_list._GridList__grid_list[key]
            self.assertEqual(grid.sparseStatus(),SparseStatus.NORMAL)
            self.assertEqual(grid.time_remove(),time)
            self.assertEqual(grid.density(),0)
            self.assertEqual(grid.clusterKey(),-1)
            self.assertEqual(grid._Grid__change,0)
        #case2:3-15的grid依然是NORMAL
        logging.debug("case2-1")
        for i in range(3,15):
            key = keys[i]
            grid = d.grid_list.getGrid(key)
            self.assertGreater(grid.density(),0)
            self.assertEqual(grid.sparseStatus(),SparseStatus.NORMAL)
            self.assertEqual(grid.densityStatus(),DensityStatus.SPARSE)
        for i in range(15,21):
            key = keys[i]
            grid = d.grid_list.getGrid(key)
            self.assertEqual(grid.sparseStatus(),SparseStatus.TODELETE)
            self.assertEqual(grid.densityStatus(),DensityStatus.SPARSE)
            self.assertNotEqual(grid.density(),0)
            self.assertNotEqual(grid.time_remove(),time)

        #case3: 被判断要删除的grid，检查其不在gridlist和cluster里面
        logging.debug("case3")
        d = D_Stream()
        #grid作为sparse和todelete，被删除且，cluster里找不到它
        raw=HelperForTest.randomLegalRawData()
        key=Helper.getKeyFromRawData(raw)
        d.grid_list.addNewData(raw,1)
        g=d.grid_list.getGrid(key)
        d.cluster_manager.addNewCluster(g)
        g._Grid__densityStatus = DensityStatus.SPARSE
        g._Grid__sparseStatus = SparseStatus.TODELETE
        d.judgeAndremoveSporadic(2)
        self.assertEqual(g.clusterKey(),-1)
        self.assertEqual(0,g.density())
        clusters=d.cluster_manager.getAllCluster()
        for k in clusters:
            cluster=clusters[k]
            self.assertEqual(0,cluster.size())

if __name__ =="__main__":
    unittest.main()
