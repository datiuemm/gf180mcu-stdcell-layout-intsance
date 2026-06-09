import os
import sys
import shutil

def copy_local_grid_file():
    current_script_dir = os.path.dirname(os.path.abspath(__file__)) if __file__ else os.getcwd()
    source_path = os.path.abspath(os.path.join(current_script_dir, "../pymacros/grid.py"))

    if not os.path.exists(source_path):
        sys.stderr.write(f"Error: Source grid.py not found at {source_path}\n")
        sys.exit(1)

    pdk_var = os.environ.get("PDK")
    pdk_root_var = os.environ.get("PDK_ROOT")
    
    search_roots = []
    if pdk_root_var and os.path.exists(pdk_root_var):
        search_roots.append(pdk_root_var)
    if pdk_var:
        if os.path.exists(pdk_var):
            search_roots.append(pdk_var)
        elif pdk_root_var:
            search_roots.append(os.path.join(pdk_root_var, pdk_var))

    target_dir = None
    
    for root in search_roots:
        for base_dir, _, files in os.walk(root):
            if "__init__.py" in files and "klayout" in base_dir and "cells" in base_dir:
                if "gf180mcu" in base_dir:
                    target_dir = base_dir
                    break
        if target_dir:
            break

    if not target_dir or not os.path.exists(target_dir):
        sys.stderr.write("Error: Target directory containing __init__.py could not be resolved via environment variables.\n")
        sys.exit(1)

    output_path = os.path.join(target_dir, "grid.py")

    try:
        shutil.copy2(source_path, output_path)
    except Exception as e:
        sys.stderr.write(f"Error: Failed to copy grid.py to target directory. Details: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    copy_local_grid_file()
