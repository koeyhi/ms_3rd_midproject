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

#연령대 분류
bins = [10, 20, 30, 40, 50, float('inf')]
labels = ['10대', '20대', '30대', '40대', '50대 이상']

bins2 = [18, 35, 50, 65, float('inf')]
labels2 = ['청년층', '중년층', '장년층', '노년층']

#연령대 범주화
Age_Group = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
Age_Group2 = pd.cut(df['Age'], bins=bins2, labels=labels2, right=False)

#M-R, P-D 열 삭제
df = df.drop(['Monthly Revenue', 'Plan Duration'], axis=1)

#연령대 열 삽입
df.insert(6, '나이대',Age_Group)
df.insert(7, '연령대',Age_Group2)

df.to_csv(f"{DATA_PATH}netflix_userbase_preprocessed.csv")

# 국가를 UCAN, EMEA, LATM, APAC으로 묶기
region_mapping = {
    # UCAN (United States and Canada)
    'United States': 'UCAN', 'Canada': 'UCAN',
    
    # LATM (Latin America and Caribbean)
    'Mexico': 'LATM', 'Brazil': 'LATM', 'Argentina': 'LATM', 'Chile': 'LATM',
    'Colombia': 'LATM', 'Peru': 'LATM', 'Venezuela': 'LATM', 'Cuba': 'LATM',
    'Ecuador': 'LATM', 'Panama': 'LATM', 'Uruguay': 'LATM',
    
    # EMEA (Europe, Middle East, and Africa)
    'United Kingdom': 'EMEA', 'Germany': 'EMEA', 'France': 'EMEA', 'Spain': 'EMEA',
    'South Africa': 'EMEA', 'Nigeria': 'EMEA', 'Egypt': 'EMEA', 'Italy': 'EMEA',
    'Russia': 'EMEA', 'Turkey': 'EMEA', 'Saudi Arabia': 'EMEA', 'Ireland': 'EMEA',
    'Netherlands': 'EMEA', 'Sweden': 'EMEA', 'Norway': 'EMEA', 'Denmark': 'EMEA',
    'Finland': 'EMEA', 'Poland': 'EMEA', 'Portugal': 'EMEA', 'Greece': 'EMEA',
    'Austria': 'EMEA', 'Belgium': 'EMEA', 'Switzerland': 'EMEA',
    
    # APAC (Asia Pacific)
    'Australia': 'APAC', 'New Zealand': 'APAC', 'India': 'APAC', 'Japan': 'APAC',
    'South Korea': 'APAC', 'China': 'APAC', 'Philippines': 'APAC', 'Thailand': 'APAC',
    'Vietnam': 'APAC', 'Malaysia': 'APAC', 'Indonesia': 'APAC', 'Singapore': 'APAC',
    'Hong Kong': 'APAC', 'Taiwan': 'APAC'
}

# Region Code 컬럼 추가 (netflix_userbase에만 적용, Country 컬럼 왼쪽에 위치)
netflix_userbase.insert(5, 'Region Code', netflix_userbase['Country'].map(region_mapping).fillna('Other'))
