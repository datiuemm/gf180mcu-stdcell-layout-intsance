#!/bin/bash
# Copyright 2026 Dat Dinh Trong
# Licensed under the Apache License, Version 2.0

if [[ ! -f "scrips/down_and_place_grid.py" ]]; then
    echo "Error: scrips/down_and_place_grid.py not found." >&2
    exit 1
fi

if [[ ! -f "scrips/update_init.py" ]]; then
    echo "Error: scrips/update_init.py not found." >&2
    exit 1
fi

python3 scrips/down_and_place_grid.py 2>/dev/null
if [[ $? -ne 0 ]]; then
    echo "Error: Execution of scrips/down_and_place_grid.py failed." >&2
    exit 1
fi

python3 scrips/update_init.py 2>/dev/null
if [[ $? -ne 0 ]]; then
    echo "Error: Execution of scrips/update_init.py failed." >&2
    exit 1
fi
