# 姿勢推定する蔵バックエンド
pythonが嫌だったのでほぼGoの書き方をしています
## ディレクトリ構造
```
.
├── Makefile
├── README.md
├── .env
├── docker
│   └── python
│       └── Dockerfile
├── docker-compose.yml
└── src
    ├── controller
    │   ├── __init__.py
    │   └── estimation.py
    ├── datastore 
    │   ├── __init__.py
    │   └── rowdata.py
    ├── factory.py
    ├── interactor 
    │   ├── __init__.py
    │   ├── estimation.py
    │   ├── format.py
    │   └── response.py
    ├── lib
    │   └── requirements.txt
    ├── main.py　
    ├── model 
    │   ├── __init__.py
    │   └── model.py
    ├── repository
    │   ├── __init__.py
    │   └── estimation.py
    ├── router.py 
    └── usecase 
        ├── __init__.py
        ├── estimation.py
        ├── format.py
        └── response.py
```

## 各層の責務
後から機能の追加等がしやすいようにクリンアーキテクチャで実装しています
### model
アプリケーション全体で使用されるデータモデルの定義を行う層
### controller
外部からのリクエストの処理を行う層
### usecase
ビジネスロジックのインターフェースやデータの入出力モデルを定義する層
### interactor
ビジネスロジックの実装を行う層
### repository
データ取得のインターフェースやデータの入出力モデルを定義する層
### datastore
データ取得の実装を行う層
### その他
- main.py: プログラムのエントリーポイント
- factory.py: 依存性の注入とアプリケーションの初期化
- router.py: API のルーティング

## 環境変数
プロジェクト直下に以下のような内容で`.env`ファイルを作成してください
```env
# Python
PYTHON_CONTAINER_HOST=<コンテナ名(任意)>
PYTHON_HOST=localhost
```

## 実行方法
- git cloneする
- プロジェクト直下で`make build`して`make up`でコンテナ&プログラム実行
- pythonコンテナに入りたかったら`make py`
- コンテナのログ見たかったら `make log`
- コンテナを落としたかったら `make down`

## API
### POST:/api/estimation/quaternion
クォータニオン推定エンドポイント
<details>
<summary>request</summary>

```json
{
    "gyro_url": "https://minio.kajilab.dev/fishex/2024-11-27%2013%3A46%3A03_gyro.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=hRjq2yhc1WqPrfEV%2F20250317%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250317T135534Z&X-Amz-Expires=900&X-Amz-SignedHeaders=host&X-Amz-Signature=eb5a9e678f8e123369e5b28fbc21e09f420d44e6b01ec1ff11eb0adf5dc90df6",
    "acc_url": "https://minio.kajilab.dev/fishex/2024-11-27%2013%3A46%3A03_accg.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=hRjq2yhc1WqPrfEV%2F20250317%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250317T135534Z&X-Amz-Expires=900&X-Amz-SignedHeaders=host&X-Amz-Signature=358620cd2ae6e3b8cc1a6880ab498747cf6122f81c171876b5fa2bc471d0e8d8"
}
```

</details>

<details>
<summary>response</summary>

#### 成功

##### Status : 200

```multipart
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="quaternion.csv"
Content-Type: text/csv

time,w,x,y,z
1732682789608,1.0,0.0,0.0,0.0
1732682789612,1.0,0.0,0.0,0.0
1732682789685,0.9999984415197393,-0.0017625867187168042,4.0452861154573335e-05,-9.278856322853723e-05
1732682789765,0.9999983684225384,-0.001804960545840035,-3.986111085309677e-05,-6.066944078751021e-05
1732682789769,0.9999982866053957,-0.001846596284265677,-0.00012670167718828413,-2.855032279316817e-05
~~省略~~

------WebKitFormBoundary7MA4YWxkTrZu0gW--

```
</details>

### POST:/api/estimation/distance
距離推定エンドポイント
<details>
<summary>request</summary>

```json
{
    "gyro_url": "https://minio.kajilab.dev/fishex/2024-11-27%2013%3A46%3A03_gyro.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=hRjq2yhc1WqPrfEV%2F20250317%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250317T135534Z&X-Amz-Expires=900&X-Amz-SignedHeaders=host&X-Amz-Signature=eb5a9e678f8e123369e5b28fbc21e09f420d44e6b01ec1ff11eb0adf5dc90df6",
    "acc_url": "https://minio.kajilab.dev/fishex/2024-11-27%2013%3A46%3A03_accg.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=hRjq2yhc1WqPrfEV%2F20250317%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250317T135534Z&X-Amz-Expires=900&X-Amz-SignedHeaders=host&X-Amz-Signature=358620cd2ae6e3b8cc1a6880ab498747cf6122f81c171876b5fa2bc471d0e8d8"
}
```

</details>

<details>
<summary>response</summary>

#### 成功

##### Status : 200

```multipart
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="distance.csv"
Content-Type: text/csv


~~省略~~

------WebKitFormBoundary7MA4YWxkTrZu0gW--

```
</details>

### POST:/api/estimation/pose
可視化用データ返却エンドポイント
<details>
<summary>request</summary>

```json
{
    "gyro_url": "https://minio.kajilab.dev/fishex/2024-11-27%2013%3A46%3A03_gyro.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=hRjq2yhc1WqPrfEV%2F20250317%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250317T135534Z&X-Amz-Expires=900&X-Amz-SignedHeaders=host&X-Amz-Signature=eb5a9e678f8e123369e5b28fbc21e09f420d44e6b01ec1ff11eb0adf5dc90df6",
    "acc_url": "https://minio.kajilab.dev/fishex/2024-11-27%2013%3A46%3A03_accg.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=hRjq2yhc1WqPrfEV%2F20250317%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250317T135534Z&X-Amz-Expires=900&X-Amz-SignedHeaders=host&X-Amz-Signature=358620cd2ae6e3b8cc1a6880ab498747cf6122f81c171876b5fa2bc471d0e8d8"
}
```

</details>

<details>
<summary>response</summary>

#### 成功

##### Status : 200

```multipart
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="result.zip"
Content-Type: application/zip


~~省略~~

------WebKitFormBoundary7MA4YWxkTrZu0gW--

```
</details>