import sys
sys.path.append("..")

from Helper import *
import unittest
from HelperForTest import *
import math
class TestHelper(unittest.TestCase):
    #测试Dm的值是否正确
    def test_Dm(self):
        dm=Helper().Cm/(Helper().N*(1-Helper().lamb))
        self.assertEqual(Helper().Dm,dm)
    #同上
    def test_Dl(self):
        dl = Helper().Cl / (Helper().N * (1 - Helper().lamb))
        self.assertEqual(Helper().Dl, dl)
    #同上
    def test_gap(self):
        gap=min(math.floor(math.log((Helper().Cl/Helper.Cm),Helper().lamb)),math.floor(math.log(((Helper().N-Helper().Cm)/(Helper().N-Helper().Cl)),Helper().lamb)))
        self.assertEqual(Helper().gap(),gap)

    #测试getDensityStatus，给定一个value值，是否能达到正确的status
    def test_getDensityStatus(self):
        self.assertEqual(Helper().getDensityStatus(Helper().Dm),DensityStatus.DENSE)
        self.assertEqual(Helper().getDensityStatus(Helper().Dm+1),DensityStatus.DENSE)
        self.assertNotEqual(Helper().getDensityStatus(Helper().Dm-1),DensityStatus.DENSE)
        self.assertEqual(Helper().getDensityStatus(Helper().Dm-(Helper().Dm+Helper().Dl)/2),DensityStatus.TRANSITIONAL)
        self.assertEqual(Helper().getDensityStatus(Helper().Dl),DensityStatus.SPARSE)
        self.assertEqual(Helper().getDensityStatus(Helper().Dl-1),DensityStatus.SPARSE)
        self.assertNotEqual(Helper().getDensityStatus(Helper().Dl+1),DensityStatus.SPARSE)


    # 测试getKeyFromRawData和getKey,给定一个Rawdata，能否返回正确的key
    def test_getKey(self):
        #case1:pw越界
        with self.assertRaisesRegex(ValueError,'pw'):
            Helper.getKey(-1,13,180)
        with self.assertRaisesRegex(ValueError,'pw'):
            Helper.getKey(201,13,180)
        rawData=RawData(-1,13,180)
        with self.assertRaisesRegex(ValueError, 'pw'):
            Helper.getKeyFromRawData(rawData)
        rawData=RawData(201,13,180)
        with self.assertRaisesRegex(ValueError, 'pw'):
            Helper.getKeyFromRawData(rawData)

        #case2:rf越界
        with self.assertRaisesRegex(ValueError, 'rf'):
            Helper.getKey(150,-1,180)
        with self.assertRaisesRegex(ValueError, 'rf'):
            Helper.getKey(150,16,180)

        rawData=RawData(150,-1,180)
        with self.assertRaisesRegex(ValueError, 'rf'):
            Helper.getKeyFromRawData(rawData)
        rawData = RawData(150, 16, 180)
        with self.assertRaisesRegex(ValueError, 'rf'):
            Helper.getKeyFromRawData(rawData)

        #case3:doa越界
        with self.assertRaisesRegex(ValueError, 'doa'):
            Helper.getKey(150,13,-1)
        with self.assertRaisesRegex(ValueError, 'doa'):
            Helper.getKey(150,13,361)
        rawData=RawData(150,13,-1)
        with self.assertRaisesRegex(ValueError, 'doa'):
            Helper.getKeyFromRawData(rawData)
        rawData=RawData(150,13,361)
        with self.assertRaisesRegex(ValueError, 'doa'):
            Helper.getKeyFromRawData(rawData)

        #case4:得到正确的值
        rawData=HelperForTest.randomLegalRawData()
        k=str(round((rawData.PW / 0.1)) * 1000000 + round((rawData.RF / 0.05)) * 1000 + round(rawData.DOA / 0.5))
        self.assertEqual(Helper.getKey(rawData.PW, rawData.RF, rawData.DOA), k)
        self.assertEqual(Helper.getKeyFromRawData(rawData), k)











    #给定一个key，检查返回值是否是其neighbor
    def test_getNeighborKeys(self):
        #TODO：测试边界点在获取Neighbor时是否获取成功


        rawData=HelperForTest.randomLegalRawData()
        key=Helper().getKeyFromRawData(rawData)
        neighbor_keys=Helper.getNeighborKeys(key)
        key_int=int(key)
        self.assertIn(str(key_int+1000000),neighbor_keys)
        self.assertIn(str(key_int-1000000),neighbor_keys)
        self.assertIn(str(key_int+1000),neighbor_keys)
        self.assertIn(str(key_int-1000),neighbor_keys)
        self.assertIn(str(key_int+1),neighbor_keys)
        self.assertIn(str(key_int-1),neighbor_keys)


if __name__=='__main__':
    unittest.main()