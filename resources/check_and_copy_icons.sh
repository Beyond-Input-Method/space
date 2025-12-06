#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Define paths relative to the script directory
YAML_FILE="$SCRIPT_DIR/../themes/public/preset_keys/default.yaml"
ICON_DIR="$SCRIPT_DIR/icon"
SVG_SOURCE_DIR="$SCRIPT_DIR/svgs_by_name"

# Check if files/directories exist
if [ ! -f "$YAML_FILE" ]; then
    echo "Error: YAML file not found at $YAML_FILE"
    exit 1
fi

if [ ! -d "$SVG_SOURCE_DIR" ]; then
    echo "Error: Source SVG directory not found at $SVG_SOURCE_DIR"
    exit 1
fi

# Create icon directory if it doesn't exist
if [ ! -d "$ICON_DIR" ]; then
    echo "Creating icon directory at $ICON_DIR"
    mkdir -p "$ICON_DIR"
fi

echo "Checking icons in $YAML_FILE..."

# Extract icon names from the YAML file
# We look for patterns like icon: "name.svg" or icon: 'name.svg'
# grep -oE 'icon: ["'"'"'][^"'"'"']*["'"'"']' extracts the key-value pair
# sed then extracts just the filename
ICONS=$(grep -oE 'icon: ["'"'"'][^"'"'"']*["'"'"']' "$YAML_FILE" | sed -E 's/icon: ["'"'"']([^"'"'"']*)["'"'"']/\1/')

COUNT=0
MISSING=0
COPIED=0
FAILED=0

for ICON in $ICONS; do
    ((COUNT++))
    DEST_PATH="$ICON_DIR/$ICON"
    
    if [ ! -f "$DEST_PATH" ]; then
        ((MISSING++))
        SOURCE_PATH="$SVG_SOURCE_DIR/$ICON"
        
        if [ -f "$SOURCE_PATH" ]; then
            cp "$SOURCE_PATH" "$DEST_PATH"
            echo "Copied missing icon: $ICON"
            ((COPIED++))
        else
            echo "Warning: Icon '$ICON' not found in source directory!"
            ((FAILED++))
        fi
    fi
done

echo "----------------------------------------"
echo "Summary:"
echo "Total icons checked: $COUNT"
echo "Icons missing from destination: $MISSING"
echo "Icons successfully copied: $COPIED"
if [ $FAILED -gt 0 ]; then
    echo "Icons not found in source: $FAILED"
fi
echo "Done."
