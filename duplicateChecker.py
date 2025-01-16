import pandas as pd

# Load the CSV files
vulnerability_path = '/home/bright/Documents/Scripts/csv/vulnerability5.csv'  # Replace with your file path
jira_path = '/home/bright/Documents/Scripts/csv/Jira5.csv'  # Replace with your file path

# Read the files into DataFrames
vulnerability_df = pd.read_csv(vulnerability_path)
jira_df = pd.read_csv(jira_path)

# Normalize the columns for comparison (strip whitespaces and convert to lowercase)
vulnerability_df['Vulnerability_Title'] = vulnerability_df['Vulnerability_Title'].str.strip().str.lower()
vulnerability_df['System_IP'] = vulnerability_df['System_IP'].str.strip()
jira_df['Summary'] = jira_df['Summary'].str.strip().str.lower()
jira_df['System_IP'] = jira_df['System_IP'].str.strip()

# Perform the merge to find duplicates
merged_df = vulnerability_df.merge(
    jira_df,
    left_on=['Vulnerability_Title', 'System_IP'],
    right_on=['Summary', 'System_IP'],
    how='inner'
)

# Remove duplicates from the original vulnerability data
updated_vulnerability_df = vulnerability_df[~vulnerability_df.index.isin(merged_df.index)]

# Save the updated vulnerability data to a new CSV file
output_path = 'updated_vulnerability5.csv'  # Replace with your desired output path
updated_vulnerability_df.to_csv(output_path, index=False)

# Output results
print(f"Number of duplicates found and removed: {merged_df.shape[0]}")
print(f"Updated vulnerability file saved to: {output_path}")
