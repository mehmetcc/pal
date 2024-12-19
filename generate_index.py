import os
import json

def create_safetensors_index(folder_path):
    """
    Generates a model.safetensors.index.json file for sharded safetensors files.
    """
    safetensors_files = [f for f in os.listdir(folder_path) if f.endswith(".safetensors")]
    safetensors_files.sort()

    if not safetensors_files:
        raise RuntimeError("No .safetensors files found in the directory.")

    index_data = {
        "weight_map": {},
        "metadata": {"format": "safetensors"}
    }

    # Map keys to shard files
    for file in safetensors_files:
        # Assume all keys are split evenly across shards (transformers will map them)
        index_data["weight_map"][f"{file}"] = file

    # Save the index file
    index_file_path = os.path.join(folder_path, "model.safetensors.index.json")
    with open(index_file_path, "w") as f:
        json.dump(index_data, f, indent=4)

    print(f"Index file successfully created at {index_file_path}")

# Run the function
folder_path = "./src/phi-4"  # Path to your safetensors shards
create_safetensors_index(folder_path)
