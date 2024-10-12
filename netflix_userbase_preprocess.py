import pandas as pd

DATA_PATH = "data/"

# 날짜 형식 변경
# df = pd.read_csv(f"{DATA_PATH}Netflix Userbase.csv")
# df["Join Date"] = pd.to_datetime(df["Join Date"], format="%d-%m-%y").dt.strftime("%Y-%m-%d")
# df["Last Payment Date"] = pd.to_datetime(df["Last Payment Date"], format="%d-%m-%y").dt.strftime("%Y-%m-%d")
# df.to_csv("C:/Users/kwon3/Desktop/converted_file.csv", index=False)

df = pd.read_csv(f"{DATA_PATH}converted_file.csv")
country_type_fee_df = pd.read_csv(f"{DATA_PATH}Netflix subscription fee Dec-2021.csv")
revenue_df = pd.read_csv(f"{DATA_PATH}netflix_revenue_updated.csv")

subscription_costs = []

for i, user in df.iterrows():
    user_country = user["Country"]
    user_subscription = user["Subscription Type"]

    country_cost = country_type_fee_df[country_type_fee_df["Country"] == user_country]

    if not country_cost.empty:
        if user_subscription == "Basic":
            subscription_costs.append(
                country_cost["Cost Per Month - Basic ($)"].values[0]
            )
        elif user_subscription == "Standard":
            subscription_costs.append(
                country_cost["Cost Per Month - Standard ($)"].values[0]
            )
        elif user_subscription == "Premium":
            subscription_costs.append(
                country_cost["Cost Per Month - Premium ($)"].values[0]
            )
    else:
        subscription_costs.append("UNK")

df["Subscription Cost"] = subscription_costs
df.to_csv("netflix_userbase_preprocessed.csv")
