#!/bin/bash
# Copyright 2026 Dat Dinh Trong
# Licensed under the Apache License, Version 2.0

show_usage() {
    echo "Usage: $0 [local|git] [-n <output_name>]" >&2
    echo "Options:" >&2
    echo "  local               Use local template.gds" >&2
    echo "  git                 Fetch template.gds from remote Git repository" >&2
    echo "  -n <output_name>    Target name for GDS file (default: default)" >&2
    exit 1
}

MODE=$1
shift

if [[ "$MODE" != "local" && "$MODE" != "git" ]]; then
    show_usage
fi

GDS_NAME="default"
while getopts "n:" opt; do
    case ${opt} in
        n ) GDS_NAME=$OPTARG ;;
        \? ) show_usage ;;
    esac
done

if [[ "$GDS_NAME" != *.gds ]]; then
    GDS_NAME="${GDS_NAME}.gds"
fi

mkdir -p ws

if [[ "$MODE" == "local" ]]; then
    if [[ ! -f "template/template.gds" ]]; then
        echo "Error: Local file template/template.gds not found." >&2
        exit 1
    fi
    cp "template/template.gds" "ws/$GDS_NAME" || { echo "Error: Failed to copy local template." >&2; exit 1; }

elif [[ "$MODE" == "git" ]]; then
    REPO_URL="https://github.com/datiuemm/gf180mcu-stdcell-layout-intsance.git"
    TEMP_DIR=$(mktemp -d)
    
    git clone -q --depth 1 --no-checkout "$REPO_URL" "$TEMP_DIR" 2>/dev/null
    if [[ $? -ne 0 ]]; then
        echo "Error: Failed to clone git repository skeleton." >&2
        rm -rf "$TEMP_DIR"
        exit 1
    fi
    
    cd "$TEMP_DIR" || exit 1
    git sparse-checkout set "template/template.gds" 2>/dev/null
    git checkout -q 2>/dev/null
    cd - > /dev/null || exit 1

    if [[ ! -f "$TEMP_DIR/template/template.gds" ]]; then
        echo "Error: template.gds not found in the remote repository target path." >&2
        rm -rf "$TEMP_DIR"
        exit 1
    fi

    cp "$TEMP_DIR/template/template.gds" "ws/$GDS_NAME" || { echo "Error: Failed to save fetched template." >&2; rm -rf "$TEMP_DIR"; exit 1; }
    rm -rf "$TEMP_DIR"
fi
