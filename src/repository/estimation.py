from dataclasses import dataclass
from typing import Protocol

import model


#生データ取得
@dataclass
class GetRowDataInput:
	url:model.URL

@dataclass
class GetRowDataOutput:
	data:model.Data


class RowDataGetter(Protocol):
    def GetRowData(self, input: GetRowDataInput) -> GetRowDataOutput:
        ...


#クォータニオン推定
@dataclass
class EstimationQuaternionInput:
	url:model.URL

@dataclass
class EstimationQuaternionOutput:
	quaternions:list[model.Quaternion]


class QuaternionEstimator(Protocol):
    def EstimationQuaternion(self, input: EstimationQuaternionInput) -> EstimationQuaternionOutput:
        ...

#移動距離推定
@dataclass
class EstimationDistanceInput:
	url:model.URL

@dataclass
class EstimationDistanceOutput:
	distance:list[model.Distance]

class DistanceEstimator(Protocol):
    def EstimationDistance(self, input: EstimationDistanceInput) -> EstimationDistanceOutput:
        ...