from pptx import Presentation
import sys

def list_layouts(pptx_path):
    try:
        prs = Presentation(pptx_path)
        print(f"Layouts in {pptx_path}:")
        for i, layout in enumerate(prs.slide_master.slide_layouts):
            print(f"  {i}: {layout.name}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        list_layouts(sys.argv[1])
    else:
        print("Usage: python list_layouts.py <path_to_pptx>")
