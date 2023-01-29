from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

def convertToTimestamp(string):
    if (len(string) < 11):
        return string
    string = string[:10] + "." + string[10:]
    return float(string)

def produceCsvRow(data): #array only
    row = ""
    for i in data:
        row += str(i) + ","
    row = row[:-1] + "\n"
    return row

def produceCsvHeadings(headings):
    data = ""
    for i in headings: 
        data += i + ","
    data = data[:-1] + "\n"
    return data

def crawlPriceData(stockCode):
    crawlType = "5"
    dataUrl = "http://stockboard2.sbsc.com.vn/ChartHandler.ashx?Type=" + crawlType + "&Symbol=" + stockCode + "&Range=all"
    resp = requests.get(dataUrl)
    
    data = resp.text

    #Remove callback
    data = data.split("callback(")[1]
    data = data.split(")")[0]

    #Json.parse data
    data = json.loads(data)

    return data

def producePriceDataCsv(priceData):
    res = ""
    for i in priceData:
        i[0] = convertToTimestamp(str(i[0]))
        i[0] = datetime.fromtimestamp(i[0])
        res += produceCsvRow(i)
    return res

stockCode = "FPT"
priceData = crawlPriceData(stockCode)
priceDataCols = ["Time", "Open", "High", "Low", "Close", "Quantity"]

csvPrice = ""
csvPrice += produceCsvHeadings(priceDataCols)
csvPrice += producePriceDataCsv(priceData)

def crawlAnnualData(stockCode):
    dataUrl = "https://e.cafef.vn/fi.ashx?symbol=" + stockCode
    resp = requests.get(dataUrl)
    
    data = resp.text

    #Json.parse data
    data = json.loads(data)

    return data

annualData = crawlAnnualData(stockCode)
annualDataCols = []
for key in dict.keys(annualData[0]):
    annualDataCols.append(key)

def produceAnnualDataCsv(annualData):
    res = ""
    for row in annualData: #each row
        rows = list(dict.values(row))
        rows[-1] = rows[-1].split("(")[1]
        rows[-1] = rows[-1].split(")")[0]
        rows[-1] = datetime.fromtimestamp(convertToTimestamp(rows[-1]))
        res += produceCsvRow(rows)
    return res

csvAnnual = ""
csvAnnual += produceCsvHeadings(annualDataCols)
csvAnnual += produceAnnualDataCsv(annualData)

f = open("./generated/crawlPrice" + stockCode + ".csv", "w")
f.write(csvPrice)
f.close()

f = open("./generated/crawlAnnual" + stockCode + ".csv", "w")
f.write(csvAnnual)
f.close()