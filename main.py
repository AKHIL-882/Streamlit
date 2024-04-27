import streamlit as st
import requests
import csv
from datetime import datetime, timedelta

def getDataAndConvertToCSV(startDate, endDate, locationId):
    url = "https://dev-api.nextvue.io/api/starter/getAeratorUpByAerator"
    date_format = "%Y-%m-%d"
  
    while startDate <= endDate:
        formatStartDate = startDate.strftime(date_format)
        url = f"{url}?startDate={formatStartDate}T00:00:00.000&endDate={formatStartDate}T23:59:00.000&locationId={locationId}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                csvFileName = f"data_for_date_{formatStartDate}.csv"
                filtered_data = [{key: entry[key] for key in ["kvah", "aerationUpPercentage", "hr"]} for entry in data]
                with open(csvFileName, mode='w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=filtered_data[0].keys())
                    writer.writeheader()
                    writer.writerows(filtered_data)
                st.write(f"Data for {formatStartDate} appended to {csvFileName}")

        startDate += timedelta(days=1)

st.title("API Data to CSV")

startDate = st.date_input("Start Date")
endDate = st.date_input("End Date")
locationId = st.text_input("Location ID")

if st.button("Conver to CSV"):
    getDataAndConvertToCSV(startDate, endDate, locationId)
