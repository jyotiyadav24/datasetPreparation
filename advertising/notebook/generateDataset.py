from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.business import Business
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.campaign import Campaign

import pandas as pd

# Initialize the Facebook Ads API
FacebookAdsApi.init(access_token='EAAKPAmfjLb0BAK2oJZCeQZBvZAFK4MjGkZB0TslT83vloGLqcxML9E1ssgwZAtJhNR2vaAFjYlSlDkujIOzfaWu7H8ZCRNZBBAfAa6fyCAdZBwBGnA6qJ2aSHqasS4JCR4NtJ9ZAZAvDXtKLUXLvPhQhtWPFxJFRY1q7ZBLZAJnpuyjve9UHtCz2OfZAhDRdIAQ93ZBXAZD')

# The Business ID for your parent account
business_id = '770208824098437'
business = Business(business_id)

# Retrieve all ad accounts under the parent business account
child_accounts = business.get_owned_ad_accounts()

# Fetch insights for each child account
all_insights = []
exclude_ad_account = '571601977885778'
for account in child_accounts:
    if account['id'] == f'act_{exclude_ad_account}':
        continue
    
    insights = Campaign(account['id']).get_insights(params={
        'level': 'campaign',
        'date_preset': 'maximum',  # Retrieves data for the lifetime of the campaigns
        'fields': [
            'ad_id',
            'ad_name',
            'adset_id',
            'adset_name',
            'campaign_id',
            'campaign_name',
            'impressions',
            'frequency',
            'full_view_impressions',
            'full_view_reach',
            'reach',
            'clicks',
            'spend',
            'purchase_roas',
            'conversions',
            'conversion_rate_ranking',
            'cost_per_conversion',
            'cost_per_action_type',
            'cost_per_estimated_ad_recallers',
            'cost_per_inline_link_click',
            'cost_per_inline_post_engagement',
            'cost_per_outbound_click',
            'cost_per_unique_click',
            'cost_per_unique_inline_link_click',
            'cpc',
            'cpm',
            'cpp',
            'ctr',
            'action_values',
            'inline_link_clicks',
            'inline_post_engagement',
            'objective',
            'optimization_goal',
            'outbound_clicks',
            'outbound_clicks_ctr',
            'social_spend',
            'website_ctr',
            'website_purchase_roas',
        ],
    })
    all_insights.extend(insights)

# Convert to DataFrame and export
data = pd.DataFrame(all_insights)
data.to_csv('./all_campaigns_insights.csv', index=False)
