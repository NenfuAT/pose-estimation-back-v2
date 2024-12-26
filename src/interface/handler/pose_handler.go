package handler

import (
	"fmt"
	"net/http"
)

func Handler(w http.ResponseWriter, r *http.Request) {
	// HTTPメソッド
	fmt.Fprintln(w, "Method:", r.Method)
	// URL
	fmt.Fprintln(w, "URL:", r.URL)
	// HTTPバージョン
	fmt.Fprintln(w, "Proto:", r.Proto)
}
