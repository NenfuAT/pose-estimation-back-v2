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
            """
            外部APIを叩いてデータを取得し\n
            生のセンサデータに線形補間等を行う
            """
            response = requests.get(input.url.accUrl)
            response.raise_for_status()  # エラーがあれば例外を発生
            accData=pd.read_csv(io.StringIO(response.text))
            response = requests.get(input.url.gyroUrl)
            response.raise_for_status()  # エラーがあれば例外を発生
            gyroData=pd.read_csv(io.StringIO(response.text))
            return repository.GetRowDataOutput(
                model.Data(accData,gyroData)
            )

def NewRowDataGetter()-> RowDataGetter:
    return RowDataGetter()

