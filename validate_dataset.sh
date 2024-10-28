#!/bin/bash

echo "Validating dataset structure..."

# Check for required files
if [ ! -f "feedback.txt" ]; then
    echo -e "${RED}Error: feedback.txt not found!${NC}"
    exit 1
fi

if [ ! -f "LICENSE" ]; then
    echo -e "${RED}Error: LICENSE file not found!${NC}"
    exit 1
fi

if [ ! -d "sample.zarr" ]; then
    echo -e "${RED}Error: sample.zarr directory not found!${NC}"
    exit 1
fi

# Check for required folders in sample.zarr
required_folders=("agents" "frames" "scenes" "traffic_light_faces")
for folder in "${required_folders[@]}"; do
    if [ ! -d "sample.zarr/$folder" ]; then
        echo -e "${RED}Error: sample.zarr/$folder directory not found!${NC}"
        exit 1
    fi
done

echo -e "${GREEN}Dataset validation successful!${NC}"
