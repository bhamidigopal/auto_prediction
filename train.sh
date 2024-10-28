#!/bin/bash
# train.sh

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "Starting Dataset Analysis..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Create required directories
mkdir -p logs output

# Run data analysis
echo -e "${GREEN}Running dataset analysis...${NC}"
python src/data_loader.py
python src/model_trainer.py

# Check if analysis was successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Dataset analysis completed successfully!${NC}"
    echo "Check output/dataset_analysis.json for detailed information"
else
    echo -e "${RED}Dataset analysis failed. Please check the logs.${NC}"
    exit 1
fi

# Deactivate virtual environment
deactivate