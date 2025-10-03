# All indicators are noted with frequency updates

FRED_SERIES_IDS = {
    's&p500': 'SP500',            # (Daily)             S&P 500 Index
    'fed_rate': 'EFFR',           # (Daily)             Federal Funds Rate
    'dxy': 'DTWEXAFEGS',                # (Daily)             US Dollar Index
    'fed_balance_sheet': 'WALCL',     # (Weekly)            Fed's Balance Sheet (Monetary Policy)
    'cpi': 'CPIAUCSL',                # (Monthly)           Consumer Price Index
    'unemployment': 'UNRATE',         # (Monthly)           Unemployment Rate
    'consumer_confidence': 'UMCSENT', # (Monthly)           University of Michigan: Consumer Sentiment Index / CONCCONF: Conference Board Consumer Confidence Index (Not seasonally adjusted) / CSCICP03USM665S: Consumer Opinion Survey: Confidence Indicator for the U.S.
    'national_debt': 'GFDEGDQ188S',   # (Quarterly/Daily)   Federal Debt: Total Public Debt as Percent of Gross Domestic Product
    'gdp': 'GDPC1',                   # (Quarterly)         Gross Domestic Product ( 'GDPC1' for real GDP )
    'geopolitial_risk': 'USEPUINDXD', # (Unavailable)       Economic Policy Uncertainty Index for U.S.
}