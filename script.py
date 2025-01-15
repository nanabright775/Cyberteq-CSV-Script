import pandas as pd
import argparse

def process_csv(file_path, output_path, vulnerabilities_to_remove):
    # Load the CSV file
    df = pd.read_csv(file_path)

    # Extract the first word of each vulnerability title
    df['First_Word'] = df['Vulnerability_Title'].str.split().str[0]

    # Replace "Unknown" in the "Technology" column with the first word from the title
    def replace_unknown_with_first_word(row):
        parts = str(row['Technology']).split(',')
        updated_parts = [part.strip() for part in parts if 'Unknown' not in part]

        if updated_parts:  # Ensure there are ports left to append
            updated_parts.insert(0, row['First_Word'])
        else:
            updated_parts = [row['First_Word']]  
        return ', '.join(updated_parts)

    df['Technology'] = df.apply(replace_unknown_with_first_word, axis=1)

    # Remove rows where "Duplicate (Yes / No)" is marked as "Yes"
    df = df[df['Duplicate (Yes / No)'].str.strip().str.lower() != 'yes']

    # Replace specific text in the 'Recommendation' column
    df['Recommendation'] = df['Recommendation'].replace(
        "Enable support for TLS 1.2 and 1.3, and disable support for TLS 1.0.",
        "Enable support for TLS 1.2 and 1.3, and disable support for TLS 1.0 and 1.1."
    )

    # Remove rows where 'Vulnerability_Title' matches any in the user-provided list
    df = df[~df['Vulnerability_Title'].str.strip().isin(vulnerabilities_to_remove)]

    # Drop the intermediate 'First_Word' column as it's no longer needed
    df = df.drop(columns=['First_Word'])

    # Save the processed data to a new file
    df.to_csv(output_path, index=False)

    print(f"Processed file saved as: {output_path}")

if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Process a vulnerability CSV file.")
    parser.add_argument('file_path', type=str, help="Path to the input CSV file.")
    parser.add_argument('output_path', type=str, help="Path to save the processed CSV file.")
    parser.add_argument('--vulnerabilities', type=str, required=True,
                        help="Comma-separated list of vulnerabilities to remove.")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Convert the comma-separated vulnerabilities to a list
    vulnerabilities_to_remove = [vul.strip() for vul in args.vulnerabilities.split(',')]
    
    # Process the CSV file
    process_csv(args.file_path, args.output_path, vulnerabilities_to_remove)
