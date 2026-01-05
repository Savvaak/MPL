import concurrent
import csv
import random
from collections import defaultdict
import statistics
from concurrent.futures import ThreadPoolExecutor


for i in range(5):
    csvfile = f"file{i+1}.csv"
    with open(csvfile, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["category", "value"])
        for i in range(50):
            letter = ["A", "B", "C", "D"]
            category = random.choice(letter)
            value = round(random.uniform(0.00, 5.00), 1)
            writer.writerow([category, value])

def calculate(filename):
    data = defaultdict(list)
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = row["category"]
            value = float(row["value"])
            data[category].append(value)
        result = {}
        for c, v in data.items():
            if v:
                med = round(statistics.median(v), 1)
                std = round(statistics.stdev(v), 1) if len(v) > 1 else 0.0
            else:
                med = 0.0
                std = 0.0
            result[c] = (med, std)
    return filename, result

filenames = [f"file{i+1}.csv" for i in range(5)]
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for i in range(5):
        futures.append(executor.submit(calculate, filenames[i]))
    results = [future.result() for future in futures]

medians = defaultdict(list)
for filename, result in results:
    first_print=f"{filename}:\n"
    for c in sorted(result.keys()):
        first_print +=f"\t {c}, {result[c][0]}, {result[c][1]}\n"
        medians[c].append(result[c][0])
    print(first_print)

second_print = "result \n"
for c in sorted(medians.keys()):
    if c:
        med = round(statistics.median(medians[c]), 1)
        std = round(statistics.stdev(medians[c]), 1) if len(medians[c]) > 1 else 0.0
    else:
        med = 0.0
        std = 0.0
    second_print += f"\t {c}, {med}, {std} \n"
print(second_print)