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
        g.setRemoveTime()
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

    def test_addData(self):
        #grid是初始化时key值是-1，若收个rawData加进来后，它的key值便以这个值为基准，后续的rawData若不符合这个key，认为是误操作
        #TODO：add之后检查key是否正确，检查错误的rawData抛出异常，检查当前更新时间是否正确、想办法测试change，测试TODELETE
        g=Grid()
        rawData=TestHelper.randomLegalRawData()
        correct_key=Helper.getKeyFromRawData(rawData)
        g.addData(rawData,1)
        self.assertEqual(correct_key,g.key())
        self.assertEqual(1,g._Grid_time_update)



        #换一个key，测错误的key抛出异常








