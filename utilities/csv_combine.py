import pandas as pd
import glob
import os

# Define directories
input_dir = '../output/'  # folder containing your CSV files
output_dir = '.'  # current directory for output

# Get all CSV files from input directory
csv_files = glob.glob(os.path.join(input_dir, '*.csv'))

# Combine all files
combined_df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)

# Save to current directory
output_path = os.path.join(output_dir, 'combined_csv_file.csv')
combined_df.to_csv(output_path, index=False)

print(f"Combined {len(csv_files)} files from '{input_dir}' into '{output_path}'")