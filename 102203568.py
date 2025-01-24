import pandas as pd
import numpy as np
import sys
import os
def topsis(input_file, weights, impacts, result_file):
    if(input_file.lower().endswith(('.xlsx', '.xls', '.xlsm'))):
        directory, file_name = os.path.split(input_file)
        file_name_without_ext = os.path.splitext(file_name)[0]
        
        # Define the new CSV file path
        csv_file_path = os.path.join(directory, f"{file_name_without_ext}.csv")
        
        # Read the Excel file
        df = pd.read_excel(input_file)
        
        # Save it as CSV in the same directory
        df.to_csv(csv_file_path, index=False)
        
        print(f"File saved as {csv_file_path}")
    else:
        df=input_file
    try:
        data = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print("Error: Input file not found.")
        return

    if data.shape[1] < 3:
        print("Error: Input file must contain at least three columns.")
        return

    try:
        weights = [float(w) for w in weights.split(',')]
        impacts = impacts.split(',')
    except:
        print("Error: Weights and impacts must be valid and separated by ','.")
        return

    if len(weights) != len(impacts) or len(weights) != (data.shape[1] - 1):
        print("Error: Number of weights and impacts must match the criteria columns.")
        return

    if not all(i in ['+', '-'] for i in impacts):
        print("Error: Impacts must be '+' or '-'.")
        return
    
    df = data.iloc[:, 1:].values
    norm_matrix = df / np.sqrt((df**2).sum(axis=0))
    weighted_matrix = norm_matrix * weights

    ideal_best = [max(weighted_matrix[:, j]) if impacts[j] == '+' else min(weighted_matrix[:, j]) for j in range(len(impacts))]
    ideal_worst = [min(weighted_matrix[:, j]) if impacts[j] == '+' else max(weighted_matrix[:, j]) for j in range(len(impacts))]

    dist_best = np.sqrt(((weighted_matrix - ideal_best)**2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_matrix - ideal_worst)**2).sum(axis=1))

    scores = dist_worst / (dist_best + dist_worst)
    ranks = scores.argsort()[::-1] + 1

    data['Topsis Score'] = scores
    data['Rank'] = ranks

    data.to_csv(result_file, index=False)
    print(f"Results saved to {result_file}")
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <input_file> <weights> <impacts> <result_file>")
    else:
        topsis(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
