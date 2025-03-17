# 姿勢推定する蔵バックエンド

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

