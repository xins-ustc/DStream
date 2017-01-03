from Helper import *
import unittest
from HelperForTest import *
class TestHelper(unittest.TestCase):
    #测试Dm的值是否正确
    def test_Dm(self):

    #同上
    def test_Dl(self):

    #同上
    def test_gap(self):

    #测试getDensityStatus，给定一个value值，是否能达到正确的status
    def test_getDensityStatus(self)

    #测试getKeyFromRawData,给定一个Rawdata，能否返回正确的key
    def test_getKeyFromRawData(self):
        # case1:pw越界
        # case2:rf越界
        # case3:doa越界
        # case4:得到正确的值

    #同上
    def test_getKey(self):
        #case1:pw越界
        with self.assertRaisesRegex(ValueError,'pw'):
            Helper.getKey(-1,13,180)
        with self.assertRaisesRegex(ValueError,'pw'):
            Helper.getKey(201,13,180)
        #case2:rf越界
        with self.assertRaisesRegex(ValueError, 'rf'):
            Helper.getKey(150,-1,180)
        with self.assertRaisesRegex(ValueError, 'rf'):
            Helper.getKey(150,16,180)
        #case3:doa越界
        with self.assertRaisesRegex(ValueError, 'doa'):
            Helper.getKey(150,13,-1)
        with self.assertRaisesRegex(ValueError, 'doa'):
            Helper.getKey(150,13,361)
        #case4:得到正确的值
        rawData=HelperForTest.randomLegalRawData()
        k=str(round((rawData.PW / 0.1)) * 1000000 + round((RawData.RF / 0.05)) * 1000 + round(RawData.DOA / 0.5))
        self.assertEqual(Helper.getKey(rawData.PW,RawData.RF,RawData.DOA),k)





    #给定一个key，检查返回值是否是其neighbor
    def test_getNeighborKeys(self):
