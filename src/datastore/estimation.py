from dataclasses import dataclass
import repository

#クォータニオン
@dataclass
class QuaternionEstimator:
	def EstimationQuaternion(self, input: repository.EstimationQuaternionInput) -> repository.EstimationQuaternionOutput:
            #todo 外部API叩く
            return repository.EstimationQuaternionOutput()


def NewQuaternionEstimator()-> QuaternionEstimator:
    return QuaternionEstimator()

def assert_protocol(impl: repository.QuaternionEstimator):
    pass

assert_protocol(QuaternionEstimator())  # 型チェックを通過すれば OK

#移動距離
@dataclass
class DistanceEstimator:
    def EstimationDistance(self,input: repository.EstimationDistanceInput)->repository.EstimationDistanceOutput:
            return repository.EstimationDistanceOutput()

def NewDistanceEstimator()-> DistanceEstimator:
    return DistanceEstimator()

def assert_protocol(impl: repository.DistanceEstimator):
    pass

assert_protocol(DistanceEstimator())