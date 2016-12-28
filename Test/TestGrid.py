from Helper import *
import unittest
from TestHelper import  *
from Grid import *
# =========================================Test Code============================================

class TestGrid(unittest.TestCase):
    def test_key(self):
        # TODO:制造100个随机的合法rawData，测key（）函数能否正确返回该key值
        for i in range(1, 100 + 1):
            rawData = TestHelper.randomLegalRawData()
            right_key = Helper().getKeyFromRawData(rawData)
            g = Grid()
            g.addData(rawData, random)
            totest_key =g.key()
            self.assertEqual(right_key,totest_key)
    def test_cluster(self):
        #TODO：给他随便设置一个cluster，测试cluster的get和isNoCluster
        g=Grid()
        rawData = TestHelper.randomLegalRawData()
        right_key = Helper().getKeyFromRawData(rawData)
        self.assertTrue(g.isNoCluster())
        g.setClusterKey(right_key)
        self.assertEqual(g.clusterKey(),right_key)

    def test_time_remove(self):
        g=Grid()
        t=random.randint(1,10000)
        g.setRemoveTime(t)
        self.assertEqual(t,g.time_remove())

    def test_densityThreshold(self):

    def test_SparseStatus(self):
        g=Grid()
        g.setSparseStatus(SparseStatus.TODELETE)
        self.assertEqual(g.sparseStatus(),SparseStatus.TODELETE)
        g.setSparseStatus(SparseStatus.TEMP)
        self.assertEqual(g.sparseStatus(),SparseStatus.TEMP)
        g.setSparseStatus(SparseStatus.NORMAL)
        self.assertEqual(g.sparseStatus(),SparseStatus.NORMAL)

    def test_densityStatus(self):
        #TODO：测试

    #检查grid经过addData后，key值是否正确
    def test_addData_key(self):

        #TODO：add之后检查key是否正确，检查错误的rawData抛出异常，检查当前更新时间是否正确、想办法测试change，测试TODELETE
        g=Grid()
        rawData=TestHelper.randomLegalRawData()
        correct_key=Helper.getKeyFromRawData(rawData)
        g.addData(rawData,1)
        self.assertEqual(correct_key,g.key())
        self.assertEqual(1,g._Grid_time_update)

    def test_addData_wrongKey(self):
        g=Grid()
        rawData=TestHelper.randomLegalRawData()
        g.addData(rawData,1)
        #换一个key，测错误的key抛出异常
        anotherRawData=TestHelper.anotherKeyRawdataFromKey(rawData)
        with self.assertRaises(ValueError):
            g.addData(anotherRawData,2)

    # 检查当前更新时间是否正确
    def test_addData_timeUpdate(self):
        g = Grid()
        t=1
        rawData=TestHelper.randomLegalRawData()
        for 1 in range(1,50):
            t+=random.randint(1,500)
            g.addData(rawData,t)
            self.assertEqual(g._Grid_time_update,t)

    #检查densityStatus的get方法是否正确
    def test_densityStatus(self):
        g = Grid()
        g._Grid__densityStatus=DensityStatus.SPARSE
        self.assertEqual(DensityStatus.SPARSE,g.densityStatus())

        g._Grid__densityStatus=DensityStatus.DENSE
        self.assertEqual(DensityStatus.DENSE,g.densityStatus())

        g._Grid__densityStatus=DensityStatus.TRANSITIONAL
        self.assertEqual(DensityStatus.TRANSITIONAL,g.densityStatus())

    # 检查addData的逻辑里各个参数的变更
    def test_addData_changeAndDensity(self):
        #测试Dense
        rawData=TestHelper.randomLegalRawData()
        g=Grid()
        g._Grid__change=0
        g._Grid__densityStatus=DensityStatus.SPARSE
        g._Grid__density=Helper().Dm+100
        g._Grid__time_update=1 #上次更新时间和当前时间相同，保证density不会太多的改变，更利于测试
        self.assertEqual(self)
        g.addData(rawData,1)
        self.assertEqual(g._Grid__change,1)
        self.assertEqual(DensityStatus.DENSE,g.density())

        #测试Sparse
        g._Grid__change=0
        g._Grid__densityStatus = DensityStatus.DENSE
        g._Grid__density=Helper.Dl-100
        g.addData(rawData, 1)
        self.assertEqual(g._Grid__change,1)
        self.assertEqual(DensityStatus.SPARSE, g.density())


        #测试Transitinal
        g._Grid__change = 0
        g._Grid__densityStatus = DensityStatus.DENSE
        g._Grid__density = Helper.Dl+(Helper.Dl+Helper.Dm)/2
        g.addData(rawData,1)
        self.assertEqual(g._Grid__change,1)
        self.assertEqual(DensityStatus.TRANSITIONAL,g.densityStatus())

        g._Grid__change = 0
        g._Grid__densityStatus = DensityStatus.SPARSE
        g._Grid__density = Helper.Dl + (Helper.Dl + Helper.Dm) / 2
        g.addData(rawData, 1)
        self.assertEqual(g._Grid__change, 1)
        self.assertEqual(DensityStatus.TRANSITIONAL, g.densityStatus())

        #测试TODELETE
        g._Grid__sparseStatus=SparseStatus.TODELETE
        g.addData(rawData,1)
        self.assertEqual(g._Grid__sparseStatus,SparseStatus.TEMP)

        g._Grid__sparseStatus = SparseStatus.NORMAL
        g.addData(rawData, 1)
        self.assertEqual(g._Grid__sparseStatus, SparseStatus.NORMAL)

        g._Grid__sparseStatus = SparseStatus.TEMP
        g.addData(rawData, 1)
        self.assertEqual(g._Grid__sparseStatus, SparseStatus.TEMP)


    def test_clear(self):
        g=Grid()
        g._Grid__cluster_key = 10000000000
        g._Grid__density = 10000000000
        g._Grid__change =10000000000
        g._Grid__densityStatus = DensityStatus.DENSE
        g._Grid__sparseStatus = SparseStatus.TODELETE
        g._Grid__time_remove = 1000000000
        g._Grid__time_update = 1000000000
        g.clear()

        self.assertEqual(g._Grid__cluster_key,-1)
        self.assertEqual(g._Grid__cluster_key,0)
        self.assertEqual(g._Grid__change, 0)
        self.assertEqual(g._Grid__time_remove,0)
        self.assertEqual(g._Grid__time_update,0)
        self.assertEqual(g._Grid__densityStatus,DensityStatus.SPARSE)
        self.assertEqual(g._Grid__sparseStatus,SparseStatus.NORMAL)












