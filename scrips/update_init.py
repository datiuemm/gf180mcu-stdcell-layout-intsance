import os
import sys
import shutil

def update_init_file():
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

    if "/foss/pdks" not in search_roots and os.path.exists("/foss/pdks"):
        search_roots.append("/foss/pdks")

    init_file = None
    
    for root in search_roots:
        for base_dir, _, files in os.walk(root):
            if "__init__.py" in files and "klayout" in base_dir and "cells" in base_dir:
                if "gf180mcu" in base_dir:
                    init_file = os.path.join(base_dir, "__init__.py")
                    break
        if init_file:
            break

    if not init_file or not os.path.exists(init_file):
        sys.stderr.write("Error: Target __init__.py for gf180mcu klayout cells could not be resolved via environment variables.\n")
        sys.exit(1)

    try:
        backup_file = init_file + ".bak"
        shutil.copy2(init_file, backup_file)
    except Exception as e:
        sys.stderr.write(f"Error: Failed to create backup file. Details: {str(e)}\n")
        sys.exit(1)

    try:
        with open(init_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        imported, registered = False, False
        import_statement = "from .grid import stdcell_grid\n"
        register_statement = "        self.layout().register_pcell(\"stdcell_grid\", stdcell_grid())  # VIAS\n"

        for line in lines:
            new_lines.append(line)
            
            if "import pya" in line and not imported:
                if not any("from .grid import" in l for l in lines):
                    new_lines.append(import_statement)
                    imported = True
            
            if "# VIAS" in line and not registered:
                if not any(".register_pcell(\"stdcell_grid\"" in l for l in lines):
                    new_lines.insert(-1, register_statement)
                    registered = True

        with open(init_file, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
            
    except Exception as e:
        sys.stderr.write(f"Error: Failed to patch __init__.py. Details: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    update_init_file()
