# レスポンスデータ作成に関するユースケース

from dataclasses import dataclass
from typing import Protocol

from fastapi.responses import Response

import model


#csvファイルの作成(メモリ上)
@dataclass
class CreateCsvInput:
	data: list

@dataclass
class CreateCsvOutput:
	csv: model.FileData

class CsvCreator(Protocol):
    def CreateCsv(self, input: CreateCsvInput) -> CreateCsvOutput:
        ...
        
#zipファイルの作成(メモリ上)
@dataclass
class CreateZipInput:
	data: list[model.FileData]
	zipName: str

@dataclass
class CreateZipOutput:
	zip: model.FileData

class ZipCreator(Protocol):
	def CreateZip(self, input: CreateZipInput) -> CreateZipOutput:
		...

#multipart-form-dataのレスポンス作成
@dataclass
class CreateMultipartInput:
	data: model.FileData

@dataclass
class CreateMultipartOutput:
	response: Response

class MultipartCreator(Protocol):
    def CreateMultipart(self, input: CreateMultipartInput) -> CreateMultipartOutput:
        ...
        