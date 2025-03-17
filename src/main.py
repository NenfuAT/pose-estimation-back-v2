# main.py
import uvicorn

import factory


def main():
    # FastAPI アプリケーションを作成
    app = factory.newApp()
    # サーバーを起動
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")

if __name__ == '__main__':
    main()
