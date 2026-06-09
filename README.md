# GF180MCU Standard Cell Layout Workspace & PCell Setup

This repository provides automated tools to configure a custom Routing Grid PCell (`stdcell_grid`) for KLayout in the `gf180mcuD` PDK environment, and to initialize a standardized layout development workspace.

---

# 1. Automated PCell Installation

To integrate the `std_grid` PCell into your KLayout PDK library, execute the setup script from the repository root:

```bash
chmod +x setup.sh
./setup.sh
```

## What this script does

- Locates the active GF180MCU KLayout cell directory dynamically via `$PDK` and `$PDK_ROOT`.
- Copies the local layout generator `grid.py` into the PDK directory.
- Safely patches the PDK's `__init__.py` to register the new PCell.
- Creates an automatic backup (`__init__.py.bak`) before modification.
- Prevents duplicate registration entries when executed multiple times.

---

# 2. Workspace Initialization

Use the `run.sh` script to create a working directory (`ws/`) and prepare your target GDS layout file.

```bash
chmod +x run.sh
```

## Option A: Using Local Files

Copies the local baseline template from `template/template.gds` into the workspace.

### Create `ws/default.gds`

```bash
./run.sh local
```

### Create `ws/my_cell_name.gds`

```bash
./run.sh local -n my_cell_name
```

---

## Option B: Fetching from Remote Git

Performs a sparse checkout to fetch only the `template.gds` file directly from the remote repository without downloading the entire commit history.

### Create `ws/default.gds`

```bash
./run.sh git
```

### Create `ws/my_cell_name.gds`

```bash
./run.sh git -n my_cell_name
```

---

# Directory Structure

```text
.
├── README.md
├── setup.sh
├── run.sh
├── layout_generator/
│   └── grid.py
├── template/
│   └── template.gds
└── ws/
    └── <generated_gds_files>
```

---

# Notes

- Requires a properly configured GF180MCU PDK installation.
- The setup script automatically detects the active PDK location through the environment variables:

```bash
PDK
PDK_ROOT
```

- Running `setup.sh` multiple times is safe and will not create duplicate registration entries.
- The generated workspace is intended for standard-cell layout development and verification using KLayout.
- This README and some scripts are generated with AI ^^

