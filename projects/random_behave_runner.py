import os
import random
import subprocess

# folder w features
feature_dir = "features"

# features
feature_files = [
    os.path.join(feature_dir, f)
    for f in os.listdir(feature_dir)
    if f.endswith(".feature")
]

# randomize
random.shuffle(feature_files)

# run tests
for feature in feature_files:
    print(f"Running: {feature}")
    subprocess.run(["behave", feature])
