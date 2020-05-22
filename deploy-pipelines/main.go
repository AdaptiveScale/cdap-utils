package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
	"time"
)

func main() {

	dir := os.ExpandEnv("${DIR}")
	items, err := ioutil.ReadDir(dir)
	if err != nil {
		fmt.Println(err)
	}

	c := make(chan string)
	for _, item := range items {
		jsonData, err := ioutil.ReadFile(dir + "/" + item.Name())
		fmt.Println(item.Name())
		if err != nil {
			fmt.Println(err)
		}

		fileName := strings.TrimSuffix(item.Name(), "-cdap-data-pipeline.json")
		url := os.ExpandEnv("${CDAP_ENDPOINT}/v3/namespaces/" + os.ExpandEnv("${NAMESPACE}/apps/") + fileName)
		fmt.Println(url)
		go deployPipeline(url, jsonData, c)
		time.Sleep(10 * time.Second)
	}

	//for loop for go routine channels
	for i := 0; i < len(items)-1; i++ {
		fmt.Println(<-c)
	}
}

func deployPipeline(url string, file []byte, c chan string) {

	method := "PUT"
	client := &http.Client{}
	req, err := http.NewRequest(method, url, bytes.NewBuffer(file))

	if err != nil {
		fmt.Println(err)
	}
	req.Header.Add("Authorization", os.ExpandEnv("Bearer ${AUTH_TOKEN}"))
	req.Header.Add("Content-Type", "application/json")

	res, err := client.Do(req)
	if err != nil {
		fmt.Println(err)
	}

	fmt.Println(res.StatusCode)
	body, err := ioutil.ReadAll(res.Body)
	if err != nil {
		fmt.Println(err)
	}

	fmt.Printf(string(body))
	defer res.Body.Close()
	c <- ("response received " + url + "\n")
}
