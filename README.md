# Toyota Woven Platform Dataset Analysis

This project provides tools to analyze and visualize the Toyota Woven Platform prediction dataset, focusing on autonomous vehicle scenarios, agent behaviors, and traffic patterns.

## Prerequisites

- Python 3.8+
- Toyota prediction dataset (`sample.zarr`)
- Approximately 2GB free disk space

## Project Structure
```
auto_prediction/
sample.zarr/          # Toyota prediction dataset
│       ├── agents/
│       ├── frames/
│       ├── scenes/
│       └── traffic_light_faces/
 src/
│   ├── data_loader.py        # Basic data loading and validation
│   └── scene_analyzer.py     # Scene analysis and visualization
output/                   # Generated analysis and visualizations
logs/                     # Execution logs
requirements.txt          # Python dependencies
```

## Setup Instructions
Run train.sh with required permissions
 
## Troubleshooting

1. **Dataset Not Found**
```bash
# Verify dataset location
ls -l data/sample.zarr
```

2. **Import Errors**
```bash
# Verify virtual environment is activated
which python
# Should point to your venv

# Reinstall requirements if needed
pip install -r requirements.txt
```

3. **Visualization Issues**
```bash
# Check output directory permissions
mkdir -p output
chmod 755 output
```

## Notes
- The visualization uses matplotlib and may need adjustments based on your screen resolution
- Large scenes may take longer to process
- Memory usage depends on scene size and number of agents

## Contributing
Feel free to submit issues and enhancement requests!

## License
Please ensure compliance with Toyota Woven Platform dataset license terms.
