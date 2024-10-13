import pandas as pd

DATA_PATH = "data/"

df = pd.read_csv(f"{DATA_PATH}Netflix Userbase.csv")
country_type_fee_df = pd.read_csv(f"{DATA_PATH}Netflix subscription fee Dec-2021.csv")
revenue_df = pd.read_csv(f"{DATA_PATH}netflix_revenue_updated.csv")


# 국가, 등급별 구독금액 컬럼 생성
def subscription_cost():
    subscription_costs = []
    for i, user in df.iterrows():
        user_country = user["Country"]
        user_subscription = user["Subscription Type"]

        country_cost = country_type_fee_df[
            country_type_fee_df["Country"] == user_country
        ]

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

    return subscription_costs


# 날짜 형식 변경
def to_datetime():
    df["Join Date"] = pd.to_datetime(df["Join Date"], dayfirst=True, format="%d-%m-%y")
    df["Last Payment Date"] = pd.to_datetime(
        df["Last Payment Date"], dayfirst=True, format="%d-%m-%y"
    )


df["Subscription Cost"] = subscription_cost()
to_datetime()

df.to_csv(f"{DATA_PATH}netflix_userbase_preprocessed.csv")
