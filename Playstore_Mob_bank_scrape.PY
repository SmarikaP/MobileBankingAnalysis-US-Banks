from google_play_scraper import app
import pandas as pd
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename='app_data_errors.log', level=logging.ERROR)

# Target app and its competitors (extended list)
package_names = [
    "com.mfoundry.mb.android.mb_beb101584",  # UMTB USA Mobile Banking (Example)
    "com.jpm.sig.android",  # JPMorgan Chase
    "com.wf.wellsfargomobile",  # Wells Fargo
    "com.infonow.bofa",  # Bank of America
    "com.usbank.mobilebanking",  # U.S. Bank
    "com.regions.mobbanking",  # Regions Bank
    "com.tdbank",  # TD Bank (US)
    "com.capitalone.mobile",  # Capital One Mobile
    "com.ubs.mobile.android",  # UBS Mobile Banking
    "com.bbt.myfi",  # BB&T (now Truist)
    "com.citi.citimobile",  # Citi Mobile
    "com.pnc.ecommerce.mobile",  # PNC Mobile
    "com.discoverfinancial.mobile",  # Discover Mobile
    "com.truist.mobile",  # SunTrust Mobile (now Truist)
]

app_data = []

for package_name in package_names:
    try:
        # Retrieve app details
        app_details = app(package_name)

        # Extract relevant information
        app_name = app_details.get('title', 'N/A')
        app_installs = app_details.get('installs', 'N/A')
        ratings = app_details.get('ratings', 'N/A')
        score = app_details.get('score', 'N/A')
        icon = app_details.get('icon', 'N/A')
        header_image = app_details.get('headerImage', 'N/A')
        histogram = app_details.get('histogram', [0]*5)

        # Create a dictionary to hold app data
        app_dict = {
            'App Name': app_name,
            'Installs': app_installs,
            'Ratings': ratings,
            'Score': score,
            'Icon': icon,
            'Header Image': header_image
        }

        # Add star rating columns
        for i in range(1, 6):
            app_dict[f"{i} Star Ratings"] = histogram[i - 1]

        # Append the dictionary to the list
        app_data.append(app_dict)

    except Exception as e:
        logging.error(f"Error retrieving data for {package_name}: {e}")

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(app_data)

# Save to Excel with a timestamp
excel_path = f'app_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
df.to_excel(excel_path, index=False)

print(f"Data has been saved to {excel_path}")
