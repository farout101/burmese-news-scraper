import pandas as pd

def csv_to_xlsx(csv_file_path, xlsx_file_path):
    """
    Convert CSV file to XLSX with only category and text columns
    
    Args:
        csv_file_path (str): Path to input CSV file
        xlsx_file_path (str): Path to output XLSX file
    """
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)
        
        # Select only the required columns
        df_filtered = df[['category', 'text']]
        
        # Save to XLSX format
        df_filtered.to_excel(xlsx_file_path, index=False)
        
        print(f"Successfully converted {csv_file_path} to {xlsx_file_path}")
        print(f"Number of rows processed: {len(df_filtered)}")
        
    except Exception as e:
        print(f"Error: {e}")

# Usage
csv_to_xlsx('combined_csv_file.csv', 'output_file.xlsx')