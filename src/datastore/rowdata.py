import io
from dataclasses import dataclass

import pandas as pd
import requests

import model
import repository


#生データ取得
@dataclass
class RowDataGetter:
	def GetRowData(self, input: repository.GetRowDataInput) -> repository.GetRowDataOutput:
            response = requests.get(input.url.accUrl)
            response.raise_for_status()  # エラーがあれば例外を発生
            accData=pd.read_csv(io.StringIO(response.text))
            response = requests.get(input.url.gyroUrl)
            response.raise_for_status()  # エラーがあれば例外を発生
            gyroData=pd.read_csv(io.StringIO(response.text))
            return repository.GetRowDataOutput(
                model.Data(accData,gyroData)
            )

def NewQuaternionEstimator()-> RowDataGetter:
    return RowDataGetter()

def assert_protocol(impl: repository.RowDataGetter):
    pass

assert_protocol(RowDataGetter())  # 型チェックを通過すれば OK
