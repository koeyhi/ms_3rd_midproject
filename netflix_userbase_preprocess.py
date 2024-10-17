import pandas as pd

DATA_PATH = "data/"

userbase = pd.read_csv(f"{DATA_PATH}Netflix Userbase.csv")
country_type_fee = pd.read_csv(f"{DATA_PATH}Netflix subscription fee Dec-2021.csv")
revenue = pd.read_csv(f"{DATA_PATH}netflix_revenue_updated.csv")


# 국가, 등급별 구독금액 컬럼 생성
subscription_costs = []
for i, user in userbase.iterrows():
    user_country = user["Country"]
    user_subscription = user["Subscription Type"]

    country_cost = country_type_fee[country_type_fee["Country"] == user_country]

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

userbase["Subscription Cost"] = subscription_costs


# 날짜 형식 변경
userbase["Join Date"] = pd.to_datetime(
    userbase["Join Date"], dayfirst=True, format="%d-%m-%y"
)
userbase["Last Payment Date"] = pd.to_datetime(
    userbase["Last Payment Date"], dayfirst=True, format="%d-%m-%y"
)


# 연령대 분류
bins = [10, 20, 30, 40, 50, float("inf")]
labels = ["10대", "20대", "30대", "40대", "50대 이상"]

bins2 = [18, 35, 50, 65, float("inf")]
labels2 = ["청년층", "중년층", "장년층", "노년층"]

# 연령대 범주화
Age_Group = pd.cut(userbase["Age"], bins=bins, labels=labels, right=False)
Age_Group2 = pd.cut(userbase["Age"], bins=bins2, labels=labels2, right=False)

# M-R, P-D 열 삭제
userbase = userbase.drop(["Monthly Revenue", "Plan Duration"], axis=1)

# 연령대 열 삽입
userbase.insert(6, "나이대", Age_Group)
userbase.insert(7, "연령대", Age_Group2)

# 국가별 작품 수 컬럼 생성
tmp = country_type_fee.iloc[:, 1:5]
userbase = pd.merge(userbase, tmp, on="Country", how="left")

# 국가를 UCAN, EMEA, LATM, APAC으로 묶기
region_mapping = {
    # UCAN (United States and Canada)
    "United States": "UCAN",
    "Canada": "UCAN",
    # LATM (Latin America and Caribbean)
    "Mexico": "LATM",
    "Brazil": "LATM",
    "Argentina": "LATM",
    "Chile": "LATM",
    "Colombia": "LATM",
    "Peru": "LATM",
    "Venezuela": "LATM",
    "Cuba": "LATM",
    "Ecuador": "LATM",
    "Panama": "LATM",
    "Uruguay": "LATM",
    # EMEA (Europe, Middle East, and Africa)
    "United Kingdom": "EMEA",
    "Germany": "EMEA",
    "France": "EMEA",
    "Spain": "EMEA",
    "South Africa": "EMEA",
    "Nigeria": "EMEA",
    "Egypt": "EMEA",
    "Italy": "EMEA",
    "Russia": "EMEA",
    "Turkey": "EMEA",
    "Saudi Arabia": "EMEA",
    "Ireland": "EMEA",
    "Netherlands": "EMEA",
    "Sweden": "EMEA",
    "Norway": "EMEA",
    "Denmark": "EMEA",
    "Finland": "EMEA",
    "Poland": "EMEA",
    "Portugal": "EMEA",
    "Greece": "EMEA",
    "Austria": "EMEA",
    "Belgium": "EMEA",
    "Switzerland": "EMEA",
    # APAC (Asia Pacific)
    "Australia": "APAC",
    "New Zealand": "APAC",
    "India": "APAC",
    "Japan": "APAC",
    "South Korea": "APAC",
    "China": "APAC",
    "Philippines": "APAC",
    "Thailand": "APAC",
    "Vietnam": "APAC",
    "Malaysia": "APAC",
    "Indonesia": "APAC",
    "Singapore": "APAC",
    "Hong Kong": "APAC",
    "Taiwan": "APAC",
}

# Region Code 컬럼 추가 (netflix_userbase에만 적용, Country 컬럼 왼쪽에 위치)
userbase.insert(
    5, "Region Code", userbase["Country"].map(region_mapping).fillna("Other")
)

userbase.to_csv(f"{DATA_PATH}netflix_userbase_preprocessed.csv")
