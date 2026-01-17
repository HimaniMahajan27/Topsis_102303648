# TOPSIS Assignment – 1 
---

## About TOPSIS

**TOPSIS** (Technique for Order of Preference by Similarity to Ideal Solution) is a multi-criteria decision-making (MCDM) technique used to rank alternatives based on their distance from an ideal best and an ideal worst solution.

The best alternative is:
- Closest to the positive ideal solution
- Farthest from the negative ideal solution

---

## Assignment Overview

This repository contains three different implementations of TOPSIS, developed as part of an academic assignment:

| Part | Implementation Type | Description |
|------|-------------------|-------------|
| Part 1 | Command Line Program | Pure Python script executed via terminal |
| Part 2 | PyPI Package | Installable TOPSIS package |
| Part 3 | Web Application | Hosted web app using Flask |

---
## Quick Links

| Resource | Link |
|----------|------|
| PyPI Package | [Pipy link](https://pypi.org/project/topsis-himani-102303648/1.0.2/) |
| Web Application | [live demo](https://topsispart3.vercel.app/) |

---

## Repository Structure

```
Topsis_102303648/
│
├── part1/                  # Command-line implementation
│   ├── topsis.py
│   ├── d1.csv
│   └── output.csv
│
├── part2/                  # PyPI package implementation
│   └── (package source files)
│
├── part3/                  # Web application
│   ├── app.py
│   ├── templates/
│   ├── requirements.txt
│   └── vercel.json
│
└── README.md               # Project documentation
```

---

## Part 1: Command-Line TOPSIS Program

A standalone Python script that runs TOPSIS directly from the terminal.

### Usage

```bash
python topsis.py d1.csv "1,1,1,2,1" "+,+,+,-,+" output.csv
```

### Parameters Used
- **Weights:** `1,1,1,2,1`
- **Impacts:** `+,+,+,-,+`

### Features
- Validates number of arguments
- Handles file not found errors
- Ensures numeric values in data columns
- Checks matching count of weights, impacts and criteria
- Outputs a CSV file with Topsis Score and Rank

### Code

<details>
<summary>Click to view topsis.py</summary>

```python
import sys
import pandas as pd
import numpy as np

def validate_inputs(data, weights, impacts):
    """Validate the input data, weights, and impacts"""
    if len(data.columns) < 3:
        raise ValueError("Input file must contain at least 3 columns")
    
    # Check if all columns (except first) are numeric
    for col in data.columns[1:]:
        if not pd.api.types.is_numeric_dtype(data[col]):
            raise ValueError(f"Column '{col}' contains non-numeric values")
    
    num_criteria = len(data.columns) - 1
    
    if len(weights) != num_criteria:
        raise ValueError(f"Number of weights ({len(weights)}) must match number of criteria ({num_criteria})")
    
    if len(impacts) != num_criteria:
        raise ValueError(f"Number of impacts ({len(impacts)}) must match number of criteria ({num_criteria})")
    
    for impact in impacts:
        if impact not in ['+', '-']:
            raise ValueError("Impacts must be either '+' or '-'")

def normalize_data(data):
    """Normalize the decision matrix"""
    data_values = data.iloc[:, 1:].values
    normalized = data_values / np.sqrt((data_values ** 2).sum(axis=0))
    return normalized

def calculate_topsis(data, weights, impacts):
    """Calculate TOPSIS scores and ranks"""
    # Normalize the data
    normalized = normalize_data(data)
    
    # Apply weights
    weighted = normalized * weights
    
    # Calculate ideal best and worst
    ideal_best = np.zeros(len(weights))
    ideal_worst = np.zeros(len(weights))
    
    for i in range(len(weights)):
        if impacts[i] == '+':
            ideal_best[i] = weighted[:, i].max()
            ideal_worst[i] = weighted[:, i].min()
        else:
            ideal_best[i] = weighted[:, i].min()
            ideal_worst[i] = weighted[:, i].max()
    
    # Calculate distances
    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))
    
    # Calculate TOPSIS score
    scores = dist_worst / (dist_best + dist_worst)
    
    # Calculate ranks
    ranks = pd.Series(scores).rank(ascending=False).astype(int)
    
    return scores, ranks

def main():
    # Check number of arguments
    if len(sys.argv) != 5:
        print("Error: Incorrect number of parameters")
        print("Usage: python topsis.py <InputDataFile> <Weights> <Impacts> <ResultFileName>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    weights_str = sys.argv[2]
    impacts_str = sys.argv[3]
    output_file = sys.argv[4]
    
    try:
        # Read input file
        data = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    try:
        # Parse weights and impacts
        weights = np.array([float(w) for w in weights_str.split(',')])
        impacts = impacts_str.split(',')
        
        # Validate inputs
        validate_inputs(data, weights, impacts)
        
        # Calculate TOPSIS
        scores, ranks = calculate_topsis(data, weights, impacts)
        
        # Add results to dataframe
        result = data.copy()
        result['Topsis Score'] = scores
        result['Rank'] = ranks
        
        # Save to output file
        result.to_csv(output_file, index=False)
        print(f"Results saved to '{output_file}'")
        
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

</details>

---

## Part 2: TOPSIS PyPI Package

TOPSIS implemented as a reusable Python package and published on PyPI.

### Installation

```bash
pip install topsis-himani-102303648==1.0.2
```

### Usage

```bash
topsis input.csv "1,1,1,2,1" "+,+,+,-,+" result.csv
```

### Features
- Easy installation using pip
- Same validation checks as Part 1
- Suitable for reuse in other Python projects
- Clean command-line interface


---

## Part 3: Web Application

A Flask-based web application that allows users to perform TOPSIS analysis through a browser.

### Live Application


### Features
- CSV file upload
- Input weights and impacts via form
- Server-side validation
- Automatic result file generation
- Direct download of result CSV
- Deployed on Vercel

### Run Locally

```bash
cd part3
pip install -r requirements.txt
python app.py
```

Open in browser: `http://127.0.0.1:5000`

---

## Input File Format

### Example CSV

```csv
Model,Price,Storage,Camera,Looks,Battery
M1,250,16,12,5,4000
M2,200,16,8,3,3500
M3,300,32,16,4,4500
```

### Rules
- First column contains alternative names
- Remaining columns contain numeric values only
- Weights and impacts must be comma-separated
- `+` indicates benefit criteria (higher is better)
- `-` indicates cost criteria (lower is better)

---


## Author

**Himani Mahajan**  
Roll Number: 102303648

---


## License

This project is part of an academic assignment and is for educational purposes only.

---
⭐ Star this repository if you find it helpful!

