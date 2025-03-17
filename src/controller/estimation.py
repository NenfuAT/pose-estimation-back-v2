from dataclasses import dataclass

from fastapi.responses import Response

import model
import usecase


@dataclass
class EstimationController:
	df:usecase.DataFormatter
	qe:usecase.QuaternionEstimator
	de:usecase.DistanceEstimator
	cc:usecase.CsvCreator
	zc:usecase.ZipCreator
	mc:usecase.MultipartCreator

	def EstimationQuaternion(self,gyroUrl=str,accUrl=str) -> Response:
		"""
		クォータニオンのリクエスト処理を行う\n
		返り値はfastapi.responsesのResponse型
		"""
		url=model.URL(accUrl=accUrl,gyroUrl=gyroUrl)
		input=usecase.FormatDataInput(url=url)
		formatData=self.df.FormatData(input=input)
		quaternions=self.qe.EstimationQuaternion(
			input=usecase.EstimationQuaternionInput(
				data=formatData.data
			)
		).quaternions
		csv=self.cc.CreateCsv(
			input=usecase.CreateCsvInput(
				data=quaternions
			)
		).csv
		response=self.mc.CreateMultipart(
			input=usecase.CreateMultipartInput(
				data=csv
			)
		).response
		return response
	
	def EstimationDistance(self,gyroUrl=str,accUrl=str) -> Response:
		"""
		移動距離のリクエスト処理を行う\n
		返り値はfastapi.responsesのResponse型
		"""
		url=model.URL(accUrl=accUrl,gyroUrl=gyroUrl)
		input=usecase.FormatDataInput(url=url)
		formatData=self.df.FormatData(input=input)
		quaternions=self.qe.EstimationQuaternion(
			input=usecase.EstimationQuaternionInput(
				data=formatData.data
			)
		).quaternions
		distances=self.de.EstimationDistance(
			input=usecase.EstimationDistanceInput(
				data=formatData.data,
				quaternions=quaternions
			)
		).distances
		csv=self.cc.CreateCsv(
			input=usecase.CreateCsvInput(
				data=distances
			)
		).csv
		response=self.mc.CreateMultipart(
			input=usecase.CreateMultipartInput(
				data=csv
			)
		).response
		return response
	
	def EstimationPose(self,gyroUrl=str,accUrl=str) -> Response:
		"""
		3次元の動きのリクエスト処理を行う\n
		返り値はfastapi.responsesのResponse型
		"""
		url=model.URL(accUrl=accUrl,gyroUrl=gyroUrl)
		input=usecase.FormatDataInput(url=url)
		formatData=self.df.FormatData(input=input)
		quaternions=self.qe.EstimationQuaternion(
			input=usecase.EstimationQuaternionInput(
				data=formatData.data
			)
		).quaternions
		quaCsv=self.cc.CreateCsv(
			input=usecase.CreateCsvInput(
				data=quaternions
			)
		).csv
		distances=self.de.EstimationDistance(
			input=usecase.EstimationDistanceInput(
				data=formatData.data,
				quaternions=quaternions
			)
		).distances
		disCsv=self.cc.CreateCsv(
			input=usecase.CreateCsvInput(
				data=distances
			)
		).csv
		zip=self.zc.CreateZip(
			input=usecase.CreateZipInput(
				data=[quaCsv,disCsv],
				zipName="result"
			)
		).zip
		response=self.mc.CreateMultipart(
			input=usecase.CreateMultipartInput(
				data=zip
			)
		).response
		return response


def NewEstimationController(
		df:usecase.DataFormatter,
		qe:usecase.QuaternionEstimator,
		de:usecase.DistanceEstimator,
		cc:usecase.CsvCreator,
		zc:usecase.ZipCreator,
		mc:usecase.MultipartCreator,
		) -> EstimationController:
    return EstimationController(
		df=df,
		qe=qe,
		de=de,
		cc=cc,
		zc=zc,
		mc=mc
		)
