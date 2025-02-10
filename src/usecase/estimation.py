from dataclasses import dataclass
from typing import Protocol

import model


#クォータニオン推定
@dataclass
class EstimationQuaternionInput:
	data:model.URL

@dataclass
class EstimationQuaternionOutput:
	quaternions:list[model.Quaternion]


class QuaternionEstimator(Protocol):
    def EstimationQuaternion(self, input: EstimationQuaternionInput) -> EstimationQuaternionOutput:
        ...
        

#移動距離推定
@dataclass
class EstimationDistanceInput:
	data:model.URL

@dataclass
class EstimationDistanceOutput:
	distance:list[model.Distance]

class DistanceEstimator(Protocol):
    def EstimationDistance(self, input: EstimationDistanceInput) -> EstimationDistanceOutput:
        ...
        