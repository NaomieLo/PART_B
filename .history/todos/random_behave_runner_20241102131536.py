import os
import random
import subprocess

# Path to the folder where your feature files are located
feature_dir = "features"

# List all feature files
feature_files = [
    os.path.join(feature_dir, f)
    for f in os.listdir(feature_dir)
    if f.endswith(".feature")
]

# Shuffle the list of feature files
random.shuffle(feature_files)

# Run each feature file in random order
for feature in feature_files:
    print(f"Running: {feature}")
    subprocess.run(["behave", feature])
