from dataclasses import dataclass

import numpy as np

import model
import repository
import usecase


@dataclass
class DataFormatter:
	rg: repository.RowDataGetter
	def FormatData(self, input: usecase.FormatDataInput) -> usecase.FormatDataOutput:
		rowData=self.rg.GetRowData(input=repository.GetRowDataInput(input.url))
		accData=rowData.data.acc
		gyroData=rowData.data.gyro
		#共通のタイムスタンプを作成
		commonTimestamps = np.union1d(gyroData['time'], accData['time'])
		# 重複を削除(あったら)
		gyroData = gyroData.drop_duplicates(subset=['time'])
		accData = accData.drop_duplicates(subset=['time'])
		# 線形補間を使用してデータを補間
		gyroData = gyroData.set_index('time').reindex(commonTimestamps).interpolate().reset_index()
		accData = accData.set_index('time').reindex(commonTimestamps).interpolate().reset_index()
		return usecase.FormatDataOutput(
            model.Data(acc=accData, gyro=gyroData)
        )

def NewDataFormatter(rg: repository.RowDataGetter) -> DataFormatter:
    return DataFormatter(rg=rg)
