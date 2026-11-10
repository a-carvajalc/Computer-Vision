#!/usr/bin/env python3
"""
CV1 Assignment 1 - Quick Start Script

Run this to verify everything is set up correctly and understand next steps.
"""

import os
import sys
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    width = 70
    print(f"\n{'='*width}")
    print(f"  {text}")
    print(f"{'='*width}\n")

def main():
    # Check location
    project_root = Path(__file__).parent
    print_header("CV1 ASSIGNMENT 1 - QUICK START")
    
    print(f"📍 Project Location: {project_root}")
    print()
    
    # Check structure
    print("✓ Checking project structure...")
    required_files = [
        "LEARNING_GUIDE.md",
        "README.md", 
        "PROJECT_STATUS.md",
        "requirements.txt",
        "src/thin_lens.py",
        "src/transformations.py",
        "src/opencv_operations.py",
        "tests/test_thin_lens.py",
        "tests/test_transformations.py",
        "tests/test_opencv_basics.py",
    ]
    
    missing = []
    for file in required_files:
        path = project_root / file
        if path.exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MISSING")
            missing.append(file)
    
    if missing:
        print(f"\n⚠️  Warning: {len(missing)} files missing. Setup may be incomplete.")
        return False
    
    print("\n✓ All project files present!\n")
    
    # Check Python version
    print("✓ Checking Python environment...")
    print(f"  Python version: {sys.version.split()[0]}")
    
    # Check pytest
    try:
        import pytest
        print(f"  pytest: ✅ {pytest.__version__}")
    except ImportError:
        print("  pytest: ❌ NOT INSTALLED - Run: pip install -r requirements.txt")
        return False
    
    # Check numpy
    try:
        import numpy
        print(f"  numpy: ✅ {numpy.__version__}")
    except ImportError:
        print("  numpy: ❌ NOT INSTALLED - Run: pip install -r requirements.txt")
        return False
    
    # Check opencv
    try:
        import cv2
        print(f"  opencv-python: ✅ {cv2.__version__}")
    except ImportError:
        print("  opencv-python: ❌ NOT INSTALLED - Run: pip install -r requirements.txt")
        return False
    
    print()
    
    print_header("NEXT STEPS")
    
    print("1. READ THE DOCUMENTATION")
    print("   Start with LEARNING_GUIDE.md for complete theory and examples:")
    print("   $ cat LEARNING_GUIDE.md")
    print()
    
    print("2. UNDERSTAND THE WORKFLOW")
    print("   Read README.md for instructions:")
    print("   $ cat README.md")
    print()
    
    print("3. RUN THE TESTS")
    print("   See which tests are available (will all fail initially - expected!):")
    print("   $ pytest tests/ -v")
    print()
    print("   Or run specific module:")
    print("   $ pytest tests/test_thin_lens.py -v")
    print()
    
    print("4. START IMPLEMENTING")
    print("   Implement functions in src/ following the docstring specifications.")
    print("   Example: Implement src/thin_lens.py::compute_image_distance()")
    print()
    print("   Then verify with:")
    print("   $ pytest tests/test_thin_lens.py::TestThinLensEquation -v")
    print()
    
    print("5. TRACK YOUR PROGRESS")
    print("   Run all tests to see your progress:")
    print("   $ pytest tests/ --tb=no  # Quick summary")
    print("   $ pytest tests/ -v       # Detailed results")
    print()
    
    print_header("QUICK REFERENCE")
    
    print("KEY FILES:")
    print("  • LEARNING_GUIDE.md - Theory, formulas, examples")
    print("  • README.md         - Workflow and debugging")
    print("  • src/thin_lens.py  - Your first module to implement")
    print()
    
    print("TEST COMMANDS:")
    print("  pytest tests/ -v                           # All tests")
    print("  pytest tests/test_thin_lens.py -v          # One module")
    print("  pytest tests/test_thin_lens.py -v -k test_compute  # Specific tests")
    print("  pytest tests/ -vv --tb=long                # Detailed errors")
    print()
    
    print("IMPLEMENTATION MODULES (in recommended order):")
    print("  1. Thin Lens Equation       (7 functions,  ~1-2 hours)")
    print("  2. Geometric Transforms     (12 functions, ~2-3 hours)")
    print("  3. OpenCV Operations        (12 functions, ~2-3 hours)")
    print()
    
    print_header("READY TO START!")
    
    print("✅ Your environment is properly configured.")
    print("✅ All project files are in place.")
    print("✅ Tests can be executed.")
    print()
    print("📖 Next: Read LEARNING_GUIDE.md or README.md to get started!")
    print()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
