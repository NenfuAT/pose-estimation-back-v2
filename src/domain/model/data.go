package model

// 加速度・ジャイロを格納
type SensorData struct {
	Time int64   `csv:"time"` // タイムスタンプ
	X    float64 `csv:"x"`    // X軸のデータ
	Y    float64 `csv:"y"`    // Y軸のデータ
	Z    float64 `csv:"z"`    // Z軸のデータ
}

type RowData struct {
	Accelerations []SensorData
	Gyroscopes    []SensorData
}

type Quaternion struct {
	T float64
	X float64
	Y float64
	Z float64
	W float64
}

type Distance struct {
	T float64
	X float64
	Y float64
	Z float64
}
