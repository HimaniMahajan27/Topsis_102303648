import sys
import os
import pandas as pd
import numpy as np

def topsis(input_file, weights, impacts, output_file):
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error: Could not read CSV file. {e}")
        return

    if df.shape[1] < 3:
        print("Error: Input file must have at least 3 columns (first column names, others numeric).")
        return
    data = df.iloc[:, 1:]

    try:
        data = data.astype(float)
    except:
        print("Error: All criteria columns must be numeric.")
        return
    weight_list = weights.split(",")
    impact_list = impacts.split(",")

    if len(weight_list) != data.shape[1] or len(impact_list) != data.shape[1]:
        print("Error: Number of weights and impacts must match number of criteria columns.")
        return
    try:
        weight_list = np.array([float(w) for w in weight_list])
    except:
        print("Error: Weights must be numeric.")
        return
    for imp in impact_list:
        if imp not in ["+", "-"]:
            print("Error: Impacts must be '+' or '-' only.")
            return
    norm = np.sqrt((data ** 2).sum())
    normalized_data = data / norm
    weighted_data = normalized_data * weight_list
    ideal_best = []
    ideal_worst = []
    for i, imp in enumerate(impact_list):
        if imp == "+":
            ideal_best.append(weighted_data.iloc[:, i].max())
            ideal_worst.append(weighted_data.iloc[:, i].min())
        else:
            ideal_best.append(weighted_data.iloc[:, i].min())
            ideal_worst.append(weighted_data.iloc[:, i].max())
    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)
    d_best = np.sqrt(((weighted_data - ideal_best) ** 2).sum(axis=1))
    d_worst = np.sqrt(((weighted_data - ideal_worst) ** 2).sum(axis=1))
    score = d_worst / (d_best + d_worst)
    df["Topsis Score"] = score
    df["Rank"] = df["Topsis Score"].rank(ascending=False).astype(int)

    # Save result to CSV
    df.to_csv(output_file, index=False)
    print(f"TOPSIS completed successfully! Result saved as '{output_file}'")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python topsis.py <InputDataFile> <Weights> <Impacts> <OutputResultFileName>")
    else:
        input_file = sys.argv[1]
        weights = sys.argv[2]
        impacts = sys.argv[3]
        output_file = sys.argv[4]
        topsis(input_file, weights, impacts, output_file)
