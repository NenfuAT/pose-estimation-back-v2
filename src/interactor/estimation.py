from dataclasses import dataclass

import numpy as np

import datastore
import repository
import usecase


#クォータニオン
@dataclass
class QuaternionEstimator:
    rg: datastore.RowDataGetter
    def EstimationQuaternion(self, input: usecase.EstimationQuaternionInput) -> usecase.EstimationQuaternionOutput:
            rowData=self.rg.GetRowData(input=repository.GetRowDataInput(input.url))
            accData=rowData.data.acc
            gyroData=rowData.data.gyro
            #共通のタイムスタンプを作成
            common_timestamps = np.union1d(gyroData['time'], accData['time'])
            # 重複を削除
            gyroData = gyroData.drop_duplicates(subset=['time'])
            accData = accData.drop_duplicates(subset=['time'])
            # 線形補間を使用してデータを補間
            gyroData = gyroData.set_index('time').reindex(common_timestamps).interpolate().reset_index()
            accData = accData.set_index('time').reindex(common_timestamps).interpolate().reset_index()
            return usecase.EstimationQuaternionOutput()


def NewQuaternionEstimator()-> QuaternionEstimator:
    return QuaternionEstimator()

def assert_protocol(impl: usecase.QuaternionEstimator):
    pass

assert_protocol(QuaternionEstimator())  # 型チェックを通過すれば OK

#移動距離
@dataclass
class DistanceEstimator:
    def EstimationDistance(self,input: usecase.EstimationDistanceInput)->usecase.EstimationDistanceOutput:
            return usecase.EstimationDistanceOutput()

def NewDistanceEstimator()-> DistanceEstimator:
    return DistanceEstimator()

def assert_protocol(impl: usecase.DistanceEstimator):
    pass

assert_protocol(DistanceEstimator())