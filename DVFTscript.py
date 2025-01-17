import pandas as pd
import argparse
import time
import os
import pyfiglet

#animate function
def animate_banner(text, delay=0.2):
    banner = pyfiglet.figlet_format(text)
    banner_lines = banner.splitlines()

    # Animation loop to display the banner line by line
    os.system('clear' if os.name == 'posix' else 'cls')  
    for i in range(1, len(banner_lines) + 1):
        os.system('clear' if os.name == 'posix' else 'cls') 
        print("\n".join(banner_lines[:i]))  
        time.sleep(delay)
    print("\n" * 2) 


#function to clean the data and save the output
def process_and_remove_duplicates(vulnerability_path, jira_path, output_path_1, vulnerabilities_to_remove, final_output_path):
    vulnerability_df = pd.read_csv(vulnerability_path)
    jira_df = pd.read_csv(jira_path)

    # Step 2: Preserve the original case of 'Vulnerability_Title' Normalize for comparison (lowercase and strip whitespace)
    vulnerability_df['Original_Title'] = vulnerability_df['Vulnerability_Title']
    vulnerability_df['Vulnerability_Title'] = vulnerability_df['Vulnerability_Title'].str.strip().str.lower()
    vulnerability_df['System_IP'] = vulnerability_df['System_IP'].str.strip()
    jira_df['Summary'] = jira_df['Summary'].str.strip().str.lower()
    jira_df['System_IP'] = jira_df['System_IP'].str.strip()

    # Step 3: Perform the merge to find duplicates
    merged_df = vulnerability_df.merge(
        jira_df,
        left_on=['Vulnerability_Title', 'System_IP'],
        right_on=['Summary', 'System_IP'],
        how='inner'
    )

    # Step 4: Remove duplicates from the original vulnerability data and drop the temp column Save the updated vulnerability data
    updated_vulnerability_df = vulnerability_df[~vulnerability_df.index.isin(merged_df.index)]
    updated_vulnerability_df['Vulnerability_Title'] = updated_vulnerability_df['Original_Title']
    updated_vulnerability_df = updated_vulnerability_df.drop(columns=['Original_Title'])
  
    updated_vulnerability_df.to_csv(output_path_1, index=False)
    print(f"Intermediate updated file saved as: {output_path_1}")
    print(f"Number of duplicates found and removed: {merged_df.shape[0]}")

    # Step 4: Process the intermediate output file
    df = pd.read_csv(output_path_1)
    df['First_Word'] = df['Vulnerability_Title'].str.split().str[0]


    def replace_unknown_with_first_word(row):
        parts = str(row['Technology']).split(',')
        updated_parts = [part.strip() for part in parts if 'Unknown' not in part]

        if updated_parts:
            updated_parts.insert(0, row['First_Word'])
        else:
            updated_parts = [row['First_Word']]
        return ', '.join(updated_parts)

    df['Technology'] = df.apply(replace_unknown_with_first_word, axis=1)

    # Remove rows where "Duplicate (Yes / No)" is marked as "Yes"
    # df = df[df['Duplicate (Yes / No)'].str.strip().str.lower() != 'yes']

    # Replace TLS solution text in the 'Recommendation' column
    df['Recommendation'] = df['Recommendation'].replace(
        "Enable support for TLS 1.2 and 1.3, and disable support for TLS 1.0.",
        "Enable support for TLS 1.2 and 1.3, and disable support for TLS 1.0 and 1.1."
    )

    # Remove rows where 'Vulnerability_Title' matches any in the user-provided list
    df = df[~df['Vulnerability_Title'].str.strip().isin(vulnerabilities_to_remove)]

    # Drop the intermediate 'First_Word' column and save the final list
    df = df.drop(columns=['First_Word'])
    df.to_csv(final_output_path, index=False)
    print(f"Final processed file saved as: {final_output_path}")

if __name__ == "__main__":
    #animating function
    text = "CYBERTEQ"
    animate_banner(text)

    # Argument parsing
    parser = argparse.ArgumentParser(description="Process and remove duplicates from vulnerability and Jira data.")
    parser.add_argument('--vulnerability', type=str, required=True, help="Path to the input vulnerability CSV file.")
    parser.add_argument('--jira', type=str, required=True, help="Path to the input Jira CSV file.")
    parser.add_argument('--intermediate_output', type=str, required=True, help="Path to save the intermediate output file.")
    parser.add_argument('--final_output', type=str, required=True, help="Path to save the final processed CSV file.")
    parser.add_argument('--vulnerabilities', type=str, required=True,
                        help="Comma-separated list of vulnerabilities to remove.")

    args = parser.parse_args()

    # Convert the comma-separated vulnerabilities to a list
    vulnerabilities_to_remove = [vul.strip() for vul in args.vulnerabilities.split(',')]

    process_and_remove_duplicates(
        args.vulnerability,
        args.jira,
        args.intermediate_output,
        vulnerabilities_to_remove,
        args.final_output
    )
