package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"
)

type Response struct {
	Answer int `json:"answer"`
}

func countCommas(text string) int {
	return strings.Count(text, ",")
}

func handler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")

	if r.Method != http.MethodGet {
		http.Error(w, "Only GET requests are allowed", http.StatusMethodNotAllowed)
		return
	}

	query := r.URL.Query()
	text := query.Get("text")

	if text == "" {
		w.Header().Set("Content-Type", "text/plain")
		fmt.Fprintln(w, "commacount is running")
		return
	}

	answer := countCommas(text)
	response := Response{Answer: answer}
	json.NewEncoder(w).Encode(response)
}

func main() {
	http.HandleFunc("/", handler)

	port := "8080"
	fmt.Printf("Server is running on port %s...\n", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
