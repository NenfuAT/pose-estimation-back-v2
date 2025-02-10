from dataclasses import dataclass
import usecase

#クォータニオン
@dataclass
class QuaternionEstimator:
	def EstimationQuaternion(self, input: usecase.EstimationQuaternionInput) -> usecase.EstimationQuaternionOutput:
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