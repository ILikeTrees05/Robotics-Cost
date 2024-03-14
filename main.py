from bs4 import BeautifulSoup as bs
from numpy import cumsum
import requests
import pandas as pd
import streamlit as st


def getGoBilda(link: str):
    soup = bs(requests.get(link).content, "html.parser")
    return (
        float(
            soup.find(attrs={"class": "price price--withoutTax"})
            .get_text()
            .split("/")[0]
            .replace("$", "")
        ),
        soup.find(attrs={"class": "productView-title"}).get_text(),
    )
def getRevRobotics(link: str):
    soup = bs(requests.get(link).content, "html.parser")
    return (
        float(
            soup.find(attrs={"class": "price price--withoutTax price-primary"})
            .get_text()
            .split("/")[0]
            .replace("$", "")
        ),
        soup.find(attrs={"class": "productView-title"}).get_text(),
    )
def getAndymark(link: str):
    soup = bs(requests.get(link).content, "html.parser")
    return (
        float(
            soup.find(attrs={"class": "product-prices__price"})
            .get_text()
            .split("/")[0]
            .replace("$", "")
        ),
        soup.find(attrs={"class": "product-details__heading"}).get_text(),
    )
def getMcMasterCarr(link: str):
    soup = bs(requests.get(link).content, "html.parser")
    return (
        float(
            soup.find(attrs={"class": "PrceTxt"})
            .get_text()
            .split(" ")[0]
            .replace("$", "")
        ),
        soup.find(attrs={"class": "Headers_productDetailHeaderPrimary__1Eaw5"}).get_text(),
    )
def getWCP(link: str):
    soup = bs(requests.get(link).content, "html.parser")
    return (
        float(
            soup.find(attrs={"class": "new-price"})
            .get_text()
            .split(" ")[0]
            .replace("$", "")
        ),
        soup.find(attrs={"class": "tt-title"}).get_text(),
    )

if __name__ == "__main__":
    st.title("Robotics Parts Cost $$$")
    inputCsv = st.file_uploader(
        type=["csv"], accept_multiple_files=False, label="Upload CSV"
    )
    st.markdown(
        "[Template Spreadsheet](https://docs.google.com/spreadsheets/d/1EE0nkI8h4506-zhxTSez_Uyiq6TKrHpjC8LqlnPCjn0/edit#gid=0)"
    )
    if inputCsv is not None:
        partList = pd.read_csv(inputCsv)
        partList = partList[pd.notnull(partList).any(axis=1)].reset_index(drop=True)
        partList["ITEM QUANTITY"] = partList["ITEM QUANTITY"]
        totalPrices = []
        prices = []
        itemNames = []
        for i in partList.iterrows():
            if i[1]["ITEM LINK"].__contains__("gobilda"):
                indPrice, itemName = getGoBilda(i[1]["ITEM LINK"])
                totalPrices.append(indPrice * i[1]["ITEM QUANTITY"])
                prices.append(indPrice)
                itemNames.append(itemName)
            elif i[1]["ITEM LINK"].__contains__("revrobotics"):
                indPrice, itemName = getRevRobotics(i[1]["ITEM LINK"])
                totalPrices.append(indPrice * i[1]["ITEM QUANTITY"])
                prices.append(indPrice)
                itemNames.append(itemName)
            elif i[1]["ITEM LINK"].__contains__("andymark"):
                indPrice, itemName = getAndymark(i[1]["ITEM LINK"])
                totalPrices.append(indPrice * i[1]["ITEM QUANTITY"])
                prices.append(indPrice)
                itemNames.append(itemName)
            elif i[1]["ITEM LINK"].__contains__("mcmaster"):
                indPrice, itemName = getWCP(i[1]["ITEM LINK"])
                totalPrices.append(indPrice * i[1]["ITEM QUANTITY"])
                prices.append(indPrice)
                itemNames.append(itemName)
        partList.insert(2, "TOTAL COST", cumsum(totalPrices))
        partList.insert(2, "TOTAL ITEM PRICE", totalPrices)
        partList.insert(2, "INDIVIDUAL ITEM PRICE", prices)
        partList.insert(1, "ITEM NAME", itemNames)
        st.dataframe(partList)
        st.download_button("Download CSV", partList.to_csv())
