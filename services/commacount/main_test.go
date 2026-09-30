package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestCountCommas(t *testing.T) {
	tests := []struct {
		input    string
		expected int
	}{
		{"hello,world", 1},
		{"a,b,c,d,e", 4},
		{"no commas here", 0},
		{",,,", 3},
	}

	for _, test := range tests {
		result := countCommas(test.input)
		if result != test.expected {
			t.Errorf("countCommas(%q) = %d; want %d", test.input, result, test.expected)
		}
	}
}

func TestHandler(t *testing.T) {
	req := httptest.NewRequest("GET", "/?text=hello,world,this,is,Go", nil)
	w := httptest.NewRecorder()

	handler(w, req)

	resp := w.Result()
	if resp.StatusCode != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", resp.StatusCode, http.StatusOK)
	}
}
