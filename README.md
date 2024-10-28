# Toyota Woven Platform Dataset Analysis

This project provides tools to analyze and visualize the Toyota Woven Platform prediction dataset, focusing on autonomous vehicle scenarios, agent behaviors, and traffic patterns.

## Prerequisites

- Python 3.8+
- Toyota prediction dataset (`data.zarr`)
- Approximately 2GB free disk space

## Project Structure
```
toyota_analysis/
├── data/
│   └── sample.zarr/          # Toyota prediction dataset
│       ├── agents/
│       ├── frames/
│       ├── scenes/
│       └── traffic_light_faces/
├── src/
│   ├── data_loader.py        # Basic data loading and validation
│   └── scene_analyzer.py     # Scene analysis and visualization
├── output/                   # Generated analysis and visualizations
├── logs/                     # Execution logs
└── requirements.txt          # Python dependencies
```

## Setup Instructions

1. **Create Project Directory**
```bash
mkdir toyota_analysis
cd toyota_analysis
```

2. **Create Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. **Install Requirements**
```bash
# Create requirements.txt
cat << EOF > requirements.txt
numpy==1.24.3
pandas==2.1.1
zarr==2.16.1
rich==13.6.0
matplotlib==3.8.0
EOF

# Install requirements
pip install -r requirements.txt
```

4. **Copy Dataset**
```bash
# Create data directory
mkdir -p data

# Copy your Toyota dataset
cp -r /path/to/sample.zarr data/
```

5. **Create Project Structure**
```bash
# Create necessary directories
mkdir -p src output logs
```

6. **Copy Source Files**
Copy the provided `scene_analyzer.py` to the `src` directory:
```bash
# Create scene_analyzer.py in src directory
cp /path/to/scene_analyzer.py src/
```

## Usage

1. **Basic Scene Analysis**
```bash
python src/scene_analyzer.py
```

This will generate:
- Detailed console output showing:
  - Scene duration and host information
  - Frame details
  - Agent information (positions, velocities, sizes)
- Visualization (`output/scene_visualization.png`) showing:
  - Ego vehicle position (blue marker)
  - Other agents (color-coded by type)
  - Velocity vectors
  - Agent orientations
- Analysis data (`output/scene_analysis.json`)

## Output Examples

### Console Output
```
Scene Analysis
-------------
Scene Duration: 25.00 seconds
Host: host-a013
Total Frames: 248

Frame Information:
Timestamp: 1572643684801892606
Number of agents: 38
Ego vehicle position: [680.62, -2183.33, 288.54]

Agents in Scene:
┌──────────┬────────────────┬──────────┬──────────┬─────────┐
│ Type     │ Position       │ Velocity │ Size     │ Heading │
├──────────┼────────────────┼──────────┼──────────┼─────────┤
│ VEHICLE  │ (665.03,       │ (0.0,    │ 4.39×    │ 58.2°   │
│          │ -2207.51)      │ 0.0)     │ 1.81×    │         │
│          │                │          │ 1.59     │         │
└──────────┴────────────────┴──────────┴──────────┴─────────┘
```

### Visualization
The generated visualization (`output/scene_visualization.png`) shows:
- Top-down view of the scene
- Ego vehicle and other agents
- Movement vectors and orientations
- Color-coded agent types
- Legend with agent types and IDs

## Data Structure
The dataset contains:
- `agents/`: Agent information (position, velocity, size)
- `frames/`: Temporal frame data
- `scenes/`: Scene context and metadata
- `traffic_light_faces/`: Traffic light states

## Analysis Features
1. Scene Analysis
   - Duration and timeline
   - Agent counts and types
   - Ego vehicle position
   - Traffic light states

2. Agent Analysis
   - Position and velocity
   - Physical dimensions
   - Movement patterns
   - Type classification

3. Visualization
   - Scene overview
   - Agent positions and orientations
   - Velocity vectors
   - Type-based coloring

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