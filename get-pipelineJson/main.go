package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"path/filepath"
)

func main() {

	path := makeDir()
	s, _ := getPipelineNames()
	pj := []pipelineJSON{}
	for k := range s {
		fmt.Println(s[k].Name)
		data, err := getPipelineJSON(s[k].Name)
		if err != nil {
			fmt.Println(err)
		}
		writeJSONtoFile(data, s[k].Name, path)
	}
	fmt.Printf("%+v\n", pj)
}

//Struct for Pipeline Names Json
type pipelineApp struct {
	Type        string `json:"type"`
	Name        string `json:"name"`
	Version     string `json:"version"`
	Description string `json:"description"`
	Artifact    artifact
}

type artifact struct {
	Name    string `json:"name"`
	Version string `json:"version"`
	Scope   string `json:"scope"`
}

func getPipelineNames() ([]pipelineApp, error) {

	url := os.ExpandEnv("${CDAP_ENDPOINT}/v3/namespaces/" + os.ExpandEnv("${NAMESPACE}/apps"))
	request, err := http.NewRequest("GET", url, nil)
	if err != nil {
		fmt.Printf("An error occured: %v", err)
	}
	client := &http.Client{}
	response, err := client.Do(request)
	if err != nil {
		fmt.Printf("An error occured: %v", err)
	}
	data, err := ioutil.ReadAll(response.Body)
	if err != nil {
		fmt.Printf("An error occured: %v", err)
	}
	var pipelineName []pipelineApp
	err = json.Unmarshal(data, &pipelineName)
	if err != nil {
		fmt.Printf("An error occured: %v", err)
		os.Exit(1)
	}

	return pipelineName, err
}

//Struct for Pipeline Json
type pipelineJSON struct {
	Name          string   `json:"name"`
	AppVersion    string   `json:"appVersion"`
	Description   string   `json:"description"`
	Configuration string   `json:"configuration"`
	Datasets      []string `json:"datasets"`
	Programs      []programs
	Plugins       []plugins
	Artifact      artifact
}

type programs struct {
	Type        string `json:"type"`
	App         string `json:"app"`
	Name        string `json:"name"`
	Description string `json:"description"`
}

type plugins struct {
	ID   string `json:"id"`
	Name string `json:"name"`
	Type string `json:"type"`
}

func getPipelineJSON(pipelinename string) (pipelineJSON, error) {

	URL := "http://localhost:11015/v3/namespaces/default/apps/" + pipelinename
	client := &http.Client{}
	request, err := http.NewRequest("GET", URL, nil)
	if err != nil {
		fmt.Println(err)
	}
	res, err := client.Do(request)
	if err != nil {
		fmt.Println(err)
	}

	data, err := ioutil.ReadAll(res.Body)

	//Error handing for err messages
	if err != nil {
		fmt.Printf("Http request failed with error %s\n", err.Error())
		fmt.Println(res.StatusCode)
	}

	var pJSON pipelineJSON
	err = json.Unmarshal(data, &pJSON)
	if err != nil {
		fmt.Printf("An error occured: %v ", err)
		os.Exit(1)
	}

	return pJSON, err
}

func writeJSONtoFile(data pipelineJSON, filename string, path string) {

	// dir is directory where you want to save file.
	dst, err := os.Create(filepath.Join(path, filepath.Base(filename)))

	if err != nil {
		fmt.Println(err)
	}
	defer dst.Close()

	dataj, err := json.MarshalIndent(data, "", " ")
	if err != nil {
		fmt.Println(err)
	}
	err = ioutil.WriteFile(filepath.Join(path,
		filepath.Base(filename)), dataj, 0644)
	if err != nil {
		fmt.Println(err)
	}
}

func makeDir() string {
	namespace := os.ExpandEnv("${NAMESPACE}")
	newpath := filepath.Join("pipelines/" + namespace + "/")
	err := os.MkdirAll(newpath, 0755)
	if err != nil {
		fmt.Println(err)
	}
	return newpath
}
