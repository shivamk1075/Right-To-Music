import subprocess
import csv
import itertools
import time
import os

# Parameter grid to search
param_grid = {
    "coef1": [0.25],             # Keep fingerprint extraction fixed
    "coef2": [0.5],
    "targetZoneSize1": [8],
    "targetZoneSize2": [2],     # Try current best and a slightly larger value
    "threshold": [7],         # Try a lower threshold as well to allow more candidates
    "tolerance": [100]  # Adjust tolerance around the current best
}

PARAMS_FILE = "params.py"
ORIGINALS =r"..\..\Audio_Dataset\Originals"
TESTERS = r"..\..\Audio_Dataset\Testers"
MAPPING = "test_mapping.csv"

def set_params(params):
    with open(PARAMS_FILE, "w") as f:
        for k, v in params.items():
            f.write(f"{k}={v}\n")

def erase_db():
    subprocess.run(["python", "main.py", "erase"], check=True)

def save_originals():
    subprocess.run(["python", "main.py", "save", ORIGINALS], check=True)

def run_find(snippet_path):
    result = subprocess.run(["python", "main.py", "find", snippet_path], capture_output=True, text=True)
    return result.stdout

def get_top3_labels(output):
    lines = output.splitlines()
    matches_section = False
    top3 = []
    for line in lines:
        if line.strip().startswith("Matches:") or line.strip().startswith("Top 20 matches:"):
            matches_section = True
            continue
        if matches_section:
            if line.strip().startswith("-"):
                # Remove "- " and split by " by "
                parts = line.strip()[2:].split(" by ")
                if parts:
                    top3.append(parts[0].strip())
                if len(top3) == 5:
                    break
            elif not line.strip():
                break  # End of matches section
    return top3

def load_mapping():
    mapping = []
    with open(MAPPING, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mapping.append((row["test_path"], row["label"]))
    return mapping

from concurrent.futures import ThreadPoolExecutor

def test_snippet(args):
    test_path, label = args
    output = run_find(test_path)
    top3 = get_top3_labels(output)
    result = {
        "test_path": test_path,
        "label": label,
        "top3": top3,
        "top1": top3[0] if top3 else None,
        "rank": (top3.index(label) + 1) if label in top3 else None
    }
    return result
def main():
    mapping = load_mapping()
    best_acc = 0
    best_params_list = []  # Store all best parameter sets

    # Parameters that require erase/save if changed
    fp_keys = ["coef1", "coef2", "targetZoneSize1"]

    keys, values = zip(*param_grid.items())
    last_fp_params = None

    for param_values in itertools.product(*values):
        params = dict(zip(keys, param_values))
        print(f"\n=== Testing with parameters: {params} ===")
        # Extract only the fingerprinting-dependent params
        fp_params = {k: params[k] for k in fp_keys}

        # Only erase/save if fingerprinting params changed
        if last_fp_params != fp_params:
            set_params(params)
            erase_db()
            save_originals()
            last_fp_params = fp_params.copy()
        else:
            # Only update params.py for matching params
            set_params(params)
        # set_params(params)


        correct = 0
        total = 0
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            results = list(executor.map(test_snippet, mapping))

        for res in results:
            print(f"Testing: {os.path.basename(res['test_path'])}")
            print("Top-3 predictions:", res["top3"])
            if res["rank"]:
                print(f"Correct label '{res['label']}'  :: found at rank {res['rank']}")
                correct += 1
            else:
                # print(f"Correct label '{res['label']}' ::  not ranked in top-3")
                print(f"Correct label '{res['label']}' ::  not ranked in top-5")
            if res["top1"]:
                print(f"Top-1 prediction: {res['top1']}")
            else:
                print("No predictions returned.")
            print("-" * 40)
            total += 1

        acc = correct / total
        print("")
        print(f"Top-5 accuracy: {acc:.2%}")
        print("")
        if acc > best_acc:
            best_acc = acc
            best_params_list = [params.copy()]
        elif acc == best_acc:
            best_params_list.append(params.copy())

    print("\nBest parameter set(s):")
    for p in best_params_list:
        print(p)
    # print("Best top-3 accuracy:", f"{best_acc:.2%}")
    print("Best top-5 accuracy:", f"{best_acc:.2%}")


if __name__ == "__main__":
    main()