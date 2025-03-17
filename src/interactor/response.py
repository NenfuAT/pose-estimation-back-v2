import csv
import io
import mimetypes
import zipfile
from dataclasses import dataclass, fields, is_dataclass
from typing import Type

from fastapi.responses import Response

import model
import usecase


@dataclass
class CsvCreator:
    def CreateCsv(self, input: usecase.CreateCsvInput) -> usecase.CreateCsvOutput:
        # データの型を取得
        data_type: Type = type(input.data[0])
        # data_type が dataclass かどうかを確認
        if not is_dataclass(data_type):
            raise TypeError(f"Expected dataclass type, but got {data_type}")
        typeName = data_type.__name__.lower()  # 型名を小文字に変換
        fileName = f"{typeName}.csv"          # ファイル名を設定

        # ヘッダーを取得（dataclass のフィールド名）
        header = [field.name for field in fields(data_type)]
        
        # CSVデータをメモリ上で作成
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(header)  # ヘッダーを書き込み

        # データを書き込み
        for item in input.data:
            writer.writerow([getattr(item, field) for field in header])

        # バイナリ変換
        binary = buffer.getvalue().encode("utf-8")
        buffer.close()
        return usecase.CreateCsvOutput(
            csv=model.FileData(
                fileName=fileName,
                binary=binary
            )
        )


@dataclass
class ZipCreator:
    def CreateZip(self, input: usecase.CreateZipInput) -> usecase.CreateZipOutput:
        fileDatas = input.data
        fileName = input.zipName if input.zipName.endswith(".zip") else input.zipName + ".zip"

        # ZIPファイルをメモリ上で作成
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for fileData in fileDatas:  
                zip_file.writestr(fileData.fileName, fileData.binary)

        # ZIPファイルのバイナリデータを取得
        zip_binary = buffer.getvalue()
        buffer.close()

        return usecase.CreateZipOutput(
            zip=model.FileData(
                fileName=fileName,
                binary=zip_binary
            )
        )


@dataclass
class MultipartCreator:
	def CreateMultipart(self, input: usecase.CreateMultipartInput) -> usecase.CreateMultipartOutput:
		fileName = input.data.fileName
		binary = input.data.binary
		# 拡張子から Content-Type を取得（デフォルトは application/octet-stream）
		contentType, _ = mimetypes.guess_type(fileName)
		if contentType is None:
			contentType = "application/octet-stream"  # 不明な場合のデフォルト値
        # マルチパートフォームデータの構築
		boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
		content = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{fileName}"\r\n'
            f"Content-Type: {contentType}\r\n\r\n"
        ).encode("utf-8") + binary + f"\r\n--{boundary}--".encode("utf-8")

		# レスポンスを返す
		return usecase.CreateMultipartOutput(
			response=Response(content, media_type=f"multipart/form-data; boundary={boundary}")
        )


def NewMultipartCreator() -> MultipartCreator:
    return MultipartCreator()
