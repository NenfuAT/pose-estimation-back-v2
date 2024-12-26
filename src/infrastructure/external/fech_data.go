package external

import (
	"encoding/csv"
	"fmt"
	"net/http"
	"pose-estimation/domain/model"
	"strconv"
)

// ExternalAPIRepository リポジトリのインターフェース
type ExternalAPIRepository interface {
	FetchData(model.SignedUrls) (*model.RowData, error)
}

// 実際のリポジトリ実装
type externalAPIRepository struct {
	client *http.Client
}

// NewExternalAPIRepository コンストラクタ
func NewExternalAPIRepository() ExternalAPIRepository {
	return &externalAPIRepository{
		client: &http.Client{},
	}
}

// FetchData 外部APIからデータを取得
func (r *externalAPIRepository) FetchData(signedUrls model.SignedUrls) (*model.RowData, error) {
	// CSVを取得して構造体に変換
	accData, err := fetchCSVAsStruct(signedUrls.AccUrl)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return nil, err
	}

	gyroData, err := fetchCSVAsStruct(signedUrls.GyroUrl)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return nil, err
	}

	rowData := model.RowData{
		Accelerations: accData,
		Gyroscopes:    gyroData,
	}

	return &rowData, nil
}

// MiniO署名付きURLでCSVを取得し、構造体に変換
func fetchCSVAsStruct(signedURL string) ([]model.SensorData, error) {
	// HTTPリクエストを送信
	resp, err := http.Get(signedURL)
	if err != nil {
		return nil, fmt.Errorf("failed to fetch CSV: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("received non-200 response: %d", resp.StatusCode)
	}

	// CSVリーダーを作成
	reader := csv.NewReader(resp.Body)

	// ヘッダーをスキップ
	_, err = reader.Read()
	if err != nil {
		return nil, fmt.Errorf("failed to read header: %v", err)
	}

	// データを構造体に変換
	var dataList []model.SensorData
	for {
		record, err := reader.Read()
		if err != nil {
			break
		}

		// 必要なデータをパース
		time, err := strconv.ParseInt(record[0], 10, 64)
		if err != nil {
			return nil, fmt.Errorf("failed to parse time: %v", err)
		}
		x, err := strconv.ParseFloat(record[1], 64)
		if err != nil {
			return nil, fmt.Errorf("failed to parse X: %v", err)
		}
		y, err := strconv.ParseFloat(record[2], 64)
		if err != nil {
			return nil, fmt.Errorf("failed to parse Y: %v", err)
		}
		z, err := strconv.ParseFloat(record[3], 64)
		if err != nil {
			return nil, fmt.Errorf("failed to parse Z: %v", err)
		}

		// 構造体に格納
		data := model.SensorData{
			Time: time,
			X:    x,
			Y:    y,
			Z:    z,
		}

		dataList = append(dataList, data)
	}

	return dataList, nil
}
