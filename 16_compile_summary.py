"""
16. Compile Summary

Automatically combine all visualization charts into a single PDF or multi-image output.
"""

from PIL import Image
import os

# Image paths and their descriptions
IMAGES = [
    ("course_offerings_comparison.png", "Course Offerings: 1996 vs 2024"),
    ("title_word_frequency_1996_vs_2024.png", "Most Common Course Title Terms: 1996 vs 2024"),
    ("subjects_new_and_discontinued.png", "New and Discontinued Courses"),
    ("curriculum_breadth_summary.png", "Curriculum Breadth: 1996 vs 2024"),
]

OUTPUT_PDF = "catalog_analysis_summary.pdf"


def load_images():
    """Load all visualization images."""
    images = []
    for path, title in IMAGES:
        if os.path.exists(path):
            img = Image.open(path)
            images.append(img.convert("RGB"))
            print(f"Loaded: {path}")
        else:
            print(f"Warning: {path} not found")
    return images


def compile_to_pdf(images):
    """Combine images into a single PDF."""
    if not images:
        print("No images to compile.")
        return
    
    images[0].save(
        OUTPUT_PDF,
        save_all=True,
        append_images=images[1:],
        optimize=False,
        duration=200,
    )
    print(f"Saved compiled PDF to {OUTPUT_PDF}")


def main():
    images = load_images()
    if images:
        compile_to_pdf(images)
    else:
        print("No images found. Please run the analysis scripts first.")


if __name__ == "__main__":
    main()
