import pandas as pd
import numpy as np
 
customers = pd.read_excel("olist_customers_cleaned.xlsx", sheet_name="Customers")
geo = pd.read_excel("olist_geolocation_cleaned.xlsx")
items = pd.read_excel("olist_order_items_cleaned.xlsx", sheet_name="Order Items Data")
payments = pd.read_excel("olist_order_payments_cleaned.xlsx")
reviews = pd.read_excel("olist_order_reviews_cleaned.xlsx")
products = pd.read_excel("olist_products_cleaned.xlsx")
sellers = pd.read_excel("olist_sellers_cleaned.xlsx")
 
print(customers.head())
print(items.tail())
print(payments.sample(5))
print(products.shape)
print(sellers.columns)
print(reviews.dtypes)
print(geo.info())
print(payments.describe())
 
# checking nulls and duplicates
print(customers.isnull().sum())
print(reviews.isna().sum())
print(items.duplicated().sum())
print(payments.duplicated().sum())
customers = customers.drop_duplicates()
items = items.drop_duplicates()
 
# unique values and counts
print(customers["State"].unique())
print(customers["State"].nunique())
print(customers["State"].value_counts())
print(payments["Payment Type"].value_counts(normalize=True))
print(products["Category"].value_counts().head(10))
print(sellers["Region"].value_counts())
 
# renaming columns and changing datatypes
items = items.rename(columns={"Price (R$)": "Price", "Freight Value (R$)": "Freight"})
payments = payments.rename(columns={"Payment Value (BRL)": "Payment Value"})
items["Shipping Limit Date"] = pd.to_datetime(items["Shipping Limit Date"])
items["Item Seq"] = items["Item Seq"].astype(int)
payments["Installments"] = payments["Installments"].astype("int64")
 
#aggregate functions
print(items["Price"].sum())
print(items["Price"].mean())
print(items["Price"].median())
print(items["Price"].min())
print(items["Price"].max())
print(items["Price"].std())
print(items["Price"].count())
print(payments["Payment Value"].sum())
print(reviews["Review Score"].mean())
print(products["Weight (g)"].max())
 
# math functions on columns
items["Total Cost"] = items["Price"] + items["Freight"]
items["Freight Percent"] = (items["Freight"] / items["Price"]) * 100
items["Freight Percent"] = items["Freight Percent"].round(2)
products["Volume Check"] = products["Length (cm)"] * products["Height (cm)"] * products["Width (cm)"]
payments["Avg Installment"] = (payments["Payment Value"] / payments["Installments"]).round(2)
payments["Value Diff"] = (payments["Payment Value"] - payments["Payment Value"].mean()).abs()
items["Running Total"] = items["Price"].cumsum()
print(items[["Price", "Freight", "Total Cost", "Freight Percent"]].head())
 
# numpy functions
prices = items["Price"].values
print(np.mean(prices))
print(np.median(prices))
print(np.std(prices))
print(np.sum(prices))
print(np.max(prices))
print(np.min(prices))
print(np.percentile(prices, 25))
print(np.percentile(prices, 75))
print(np.round(np.mean(prices), 2))
print(np.corrcoef(items["Price"], items["Freight"]))
print(np.sqrt(products["Weight (g)"]).head())
print(np.log(items["Price"] + 1).head())
print(np.arange(1, 11))
print(np.unique(payments["Payment Type"]))
 
s# filtering
print(items[items["Price"] > 500])
print(payments[payments["Payment Type"] == "Credit Card"])
print(customers[customers["State"] == "SP"])
print(reviews[reviews["Review Score"] == 1])
print(products[(products["Weight (g)"] > 1000) & (products["Photos"] > 3)])
print(payments[(payments["Payment Type"] == "Boleto") | (payments["Installments"] > 10)])
print(customers[customers["State"].isin(["SP", "RJ", "MG"])])
print(items[items["Price"].between(50, 100)])
print(reviews[~(reviews["Sentiment"] == "Positive")])
print(payments.query("Installments > 6 and `Payment Value` > 200"))
print(sellers[sellers["Region"] != "Southeast"])
print(items.loc[items["Freight"] > 50, ["Order ID", "Price", "Freight"]])
print(products.iloc[0:5, 0:4])
print(customers.loc[0:4, ["City", "State"]])
 
# string handling
customers["City Upper"] = customers["City"].str.upper()
customers["City Lower"] = customers["City"].str.lower()
customers["City Title"] = customers["City"].str.title()
customers["City"] = customers["City"].str.strip()
customers["City Length"] = customers["City"].str.len()
customers["City First 3"] = customers["City"].str[:3]
customers["City Fixed"] = customers["City"].str.replace(" Do ", " do ", regex=False)
print(customers[customers["City"].str.contains("Sao")].head())
print(customers[customers["City"].str.startswith("Rio")].head())
print(customers[customers["City"].str.endswith("Preto")].head())
print(customers[customers["City"].str.contains("sao", case=False)].shape)
print(customers["City"].str.split(" ").head())
customers["First Word"] = customers["City"].str.split(" ").str[0]
products["Category Clean"] = products["Category"].str.replace("_", " ").str.title()
products["Category Short"] = products["Category"].str.slice(0, 5)
sellers["City Code"] = sellers["City"].str.upper().str[:3] + "-" + sellers["State"]
reviews["Comment Words"] = reviews["Comment Message"].str.split().str.len()
reviews["Title Length"] = reviews["Comment Title"].str.len()
print(reviews[reviews["Comment Message"].str.contains("recomendo", case=False, na=False)].shape)
print(customers["Customer ID"].str[:6].head())
print(customers[["City", "State"]].head())
print(customers["City"].str.cat(customers["State"], sep=", ").head())
  
# sorting
print(items.sort_values("Price", ascending=False).head(10))
print(products.sort_values(["Category", "Weight (g)"], ascending=[True, False]).head())
print(payments.nlargest(5, "Payment Value"))
print(payments.nsmallest(5, "Payment Value"))
 
# merging tables
items_products = items.merge(products, on="Product ID", how="left")
items_sellers = items.merge(sellers, on="Seller ID", how="left")
order_pay = items.merge(payments, on="Order ID", how="inner")
order_reviews = payments.merge(reviews, on="Order ID", how="left")
print(items_products[["Order ID", "Category", "Price"]].head())
print(items_sellers.groupby("Region")["Price"].sum())
print(items_products.groupby("Category")["Price"].sum().sort_values(ascending=False).head(10))
print(order_pay.shape)
 
# date handling
reviews["Review Year"] = reviews["Review Created"].dt.year
reviews["Review Month"] = reviews["Review Created"].dt.month
reviews["Review Day Name"] = reviews["Review Created"].dt.day_name()
items["Ship Year"] = items["Shipping Limit Date"].dt.year
print(reviews.groupby("Review Year")["Review Score"].mean().round(2))
print(items.groupby("Ship Year")["Price"].sum())
print(reviews[reviews["Review Created"] >= "2018-01-01"].shape)
 
# handling missing values
print(reviews["Response Time (Days)"].fillna(0).head())
print(reviews["Response Time (Days)"].fillna(reviews["Response Time (Days)"].mean()).head())
print(reviews.dropna(subset=["Response Time (Days)"]).shape)
 
# saving results
top_sellers = items.groupby("Seller ID")["Price"].sum().sort_values(ascending=False).head(10)
top_sellers.to_csv("top_sellers.csv")
items_products.to_excel("items_with_products.xlsx", index=False)
 
