import kagglehub

DATASET = "adamjoseph7945/vehicle-routing-problem-set"

print("Downloading dataset from Kaggle...")

path = kagglehub.dataset_download(
    DATASET,
    output_dir="./data/raw"
)

print("Download complete!")
print(f"Dataset location: {path}")