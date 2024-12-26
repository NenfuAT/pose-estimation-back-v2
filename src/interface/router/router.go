package router

import (
	"net/http"
	"pose-estimation/interface/handler"
)

func Init() {
	// "/hello" エンドポイントにリクエストが来たときに helloHandler 関数を呼び出す
	http.HandleFunc("/hello", handler.Handler)
	// サーバーをポート8080で開始
	http.ListenAndServe(":8000", nil)
}
