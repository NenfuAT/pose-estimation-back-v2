from dataclasses import dataclass


@dataclass
class URL:
	accUrl:str
	gyroUrl:str

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