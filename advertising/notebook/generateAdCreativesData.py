from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.business import Business
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adsinsights import AdsInsights

import pandas as pd

# Initialize the Facebook Ads API
FacebookAdsApi.init(access_token='EAAKPAmfjLb0BAK2oJZCeQZBvZAFK4MjGkZB0TslT83vloGLqcxML9E1ssgwZAtJhNR2vaAFjYlSlDkujIOzfaWu7H8ZCRNZBBAfAa6fyCAdZBwBGnA6qJ2aSHqasS4JCR4NtJ9ZAZAvDXtKLUXLvPhQhtWPFxJFRY1q7ZBLZAJnpuyjve9UHtCz2OfZAhDRdIAQ93ZBXAZD')

# The Business ID for your parent account
business_id = '770208824098437'
business = Business(business_id)

# Retrieve all ad accounts under the parent business account
child_accounts = business.get_owned_ad_accounts()

# Fetch insights for each child account
all_ad_creatives = []
all_ad_insights = []

for account in child_accounts:
    try:
        # Fetch Ad Creatives
        ad_creatives = AdAccount(account['id']).get_ad_creatives(fields=[
            'id',
            'name',
            'title',
            'body',
            'object_url',
        ])
        all_ad_creatives.extend(ad_creatives)

        # Fetch ad insights with ad creative breakdown
        insights = AdAccount(account['id']).get_insights(params={
            'level': 'ad',
            'fields': [
                'ad_id',
                'campaign_id',
                'clicks',
                'impressions',
                'reach',
                'cpm',
            ],
            'breakdowns': ['age', 'gender'],
        })
        all_ad_insights.extend(insights)
    except Exception as e:
        print(f"Error fetching insights for account {account['id']}: {str(e)}")

# Convert to DataFrames
df_creatives = pd.DataFrame(all_ad_creatives)
df_insights = pd.DataFrame(all_ad_insights)

# Merge the dataframes
merged_data = pd.merge(df_creatives, df_insights, left_on='id', right_on='ad_id', how='inner')

# Save the merged DataFrame
df_insights.to_csv('./all_ad_creatives_with_insights.csv', index=False)