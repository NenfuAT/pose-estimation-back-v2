from dataclasses import dataclass

import pandas as pd


@dataclass
class URL:
	accUrl:str
	gyroUrl:str

@dataclass
class Data:
	acc:pd.DataFrame
	gyro:pd.DataFrame

@dataclass
class Quaternion:
	time:int
	w:float
	x:float
	y:float
	z:float

@dataclass
class Distance:
	time:int
	x:float
	y:float
	z:float

@dataclass
class FileData:
	fileName:str
	binary:bytes