import os
# Force cache early
HF_CACHE_PATH = "/mnt/data-disk/ai2cup/AI2CUP/apps/backend/.hf_cache"
os.environ["HF_HOME"] = HF_CACHE_PATH
os.environ["HF_DATASETS_CACHE"] = HF_CACHE_PATH
os.environ["TRANSFORMERS_CACHE"] = HF_CACHE_PATH
os.environ["TMPDIR"] = HF_CACHE_PATH

from datasets import load_dataset

def inspect():
    ds = load_dataset("SamruddhK/coffee-bean-grading-dataset")
    print(f"Features: {ds['train'].features}")
    item = ds['train'][0]
    print(f"First item keys: {item.keys()}")
    img = item['image']
    print(f"Image type: {type(img)}")
    if hasattr(img, 'filename'):
        print(f"Image filename: {img.filename}")
    else:
        print("Image has no filename attribute")

if __name__ == "__main__":
    inspect()
