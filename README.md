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

