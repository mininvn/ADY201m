from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

sbscDataToType = {
    "data": "5",
    "column": "9"
}

def crawlData(stockCode, crawlType):
    dataUrl = "http://stockboard2.sbsc.com.vn/ChartHandler.ashx?Type=" + crawlType + "&Symbol=" + stockCode + "&Range=all"
    resp = requests.get(dataUrl)
    
    data = resp.text

    #Remove callback
    data = data.split("callback(")[1]
    data = data.split(")")[0]

    #Json.parse data
    data = json.loads(data)

    return data

def produceCsvRow(data):
    row = ""
    for i in data:
        row += str(i) + ","
    row = row[:-1] + "\n"
    return row

stockCode = "FPT"
crawlType = "5"
dataRows = crawlData(stockCode, crawlType)

dataCols = ["Time", "Open", "High", "Low", "Close", "Quantity"]

csvData = ""

for i in dataCols: 
    csvData += i + ","
csvData = csvData[:-1] + "\n"

for i in dataRows:
    i[0] = str(i[0])
    i[0] = i[0][:11]
    i[0] = int(i[0])
    i[0] = datetime.fromtimestamp(i[0])
    csvData += produceCsvRow(i)

f = open("./generated/crawl" + stockCode + ".csv", "a")
f.write(csvData)
f.close()