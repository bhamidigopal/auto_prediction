# src/scene_analyzer.py

import zarr
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import matplotlib.pyplot as plt
from pathlib import Path
import json

console = Console()

class ToyotaSceneAnalyzer:
    def __init__(self, zarr_path="sample.zarr"):
        self.zarr_path = zarr_path
        self.label_map = {
            3: "VEHICLE",  # Based on your data showing index 3 with probability 1.0
            0: "UNKNOWN",
            1: "PEDESTRIAN",
            2: "BICYCLE",
            4: "MOTORCYCLE",
            5: "CYCLIST",
            6: "BUS",
            7: "TRUCK",
            8: "EMERGENCY_VEHICLE"
        }

    def analyze_scene(self, scene_idx=0):
        """Analyze a specific scene with all its components"""
        console.print(Panel("[bold blue]Scene Analysis[/bold blue]"))
        
        root = zarr.open(self.zarr_path, mode='r')
        
        # Get scene data
        scene = root['scenes'][scene_idx]
        frame_start, frame_end = scene['frame_index_interval']
        frames = root['frames'][frame_start:frame_end]
        
        # Get first frame and its agents
        first_frame = frames[0]
        agent_start, agent_end = first_frame['agent_index_interval']
        agents = root['agents'][agent_start:agent_end]

        # Scene Duration
        duration = (scene['end_time'] - scene['start_time']) / 1e9  # Convert to seconds
        console.print(f"Scene Duration: {duration:.2f} seconds")
        console.print(f"Host: {scene['host']}")
        console.print(f"Total Frames: {len(frames)}")

        # Frame Analysis
        console.print("\n[bold cyan]Frame Information:[/bold cyan]")
        console.print(f"Timestamp: {first_frame['timestamp']}")
        console.print(f"Number of agents: {len(agents)}")
        console.print(f"Ego vehicle position: {first_frame['ego_translation'].tolist()}")

        # Agents Analysis
        console.print("\n[bold cyan]Agents in Scene:[/bold cyan]")
        agent_table = Table()
        agent_table.add_column("Type")
        agent_table.add_column("Position (x, y)")
        agent_table.add_column("Velocity")
        agent_table.add_column("Size (L×W×H)")
        agent_table.add_column("Heading")

        for agent in agents:
            agent_type = self._get_agent_type(agent['label_probabilities'])
            agent_table.add_row(
                agent_type,
                f"({agent['centroid'][0]:.2f}, {agent['centroid'][1]:.2f})",
                f"({agent['velocity'][0]:.2f}, {agent['velocity'][1]:.2f})",
                f"{agent['extent'][0]:.2f}×{agent['extent'][1]:.2f}×{agent['extent'][2]:.2f}",
                f"{np.degrees(agent['yaw']):.1f}°"
            )

        console.print(agent_table)

        # Create visualization
        self._create_scene_visualization(first_frame, agents)
        
        return {
            "scene_info": {
                "duration": duration,
                "num_frames": len(frames),
                "host": scene['host']
            },
            "ego_vehicle": {
                "position": first_frame['ego_translation'].tolist(),
                "rotation": first_frame['ego_rotation'].tolist()
            },
            "agents": [self._convert_agent_data(agent) for agent in agents]
        }

    def _get_agent_type(self, label_probabilities):
        """Get agent type from label probabilities"""
        max_prob_idx = np.argmax(label_probabilities)
        return self.label_map.get(max_prob_idx, "UNKNOWN")

    def _convert_agent_data(self, agent):
        """Convert agent data to serializable format"""
        return {
            "type": self._get_agent_type(agent['label_probabilities']),
            "position": agent['centroid'].tolist(),
            "velocity": agent['velocity'].tolist(),
            "heading": float(agent['yaw']),
            "size": agent['extent'].tolist(),
            "track_id": int(agent['track_id'])
        }

    def _create_scene_visualization(self, frame, agents):
        """Create a visualization of the scene"""
        plt.figure(figsize=(15, 10))
        
        # Plot ego vehicle
        ego_pos = frame['ego_translation'][:2]
        plt.plot(ego_pos[0], ego_pos[1], 'bo', markersize=15, label='Ego Vehicle')
        
        # Plot agents
        colors = {
            'VEHICLE': 'red',
            'PEDESTRIAN': 'green',
            'BICYCLE': 'yellow',
            'MOTORCYCLE': 'purple',
            'UNKNOWN': 'gray'
        }
        
        for agent in agents:
            pos = agent['centroid']
            vel = agent['velocity']
            agent_type = self._get_agent_type(agent['label_probabilities'])
            color = colors.get(agent_type, 'gray')
            
            # Plot agent position
            plt.plot(pos[0], pos[1], 'o', color=color, markersize=10, 
                    label=f'{agent_type} (ID: {agent["track_id"]})')
            
            # Draw velocity vector if non-zero
            if np.any(vel):
                plt.arrow(pos[0], pos[1], vel[0]*2, vel[1]*2, 
                         head_width=1.0, head_length=1.5, 
                         fc=color, ec=color, alpha=0.6)
            
            # Draw agent orientation
            heading = agent['yaw']
            length = max(agent['extent'][0], 2.0)  # Use agent length or minimum 2.0
            dx = length * np.cos(heading)
            dy = length * np.sin(heading)
            plt.arrow(pos[0], pos[1], dx, dy, 
                     head_width=0.5, head_length=1.0, 
                     fc='black', ec='black', alpha=0.5)

        plt.title("Scene Overview")
        plt.xlabel("X Position (m)")
        plt.ylabel("Y Position (m)")
        plt.axis('equal')
        plt.grid(True)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Save visualization
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        plt.savefig(output_dir / 'scene_visualization.png', bbox_inches='tight')
        console.print("\n[green]Scene visualization saved to output/scene_visualization.png[/green]")
        plt.close()

def main():
    try:
        analyzer = ToyotaSceneAnalyzer()
        scene_data = analyzer.analyze_scene(0)
        
        # Save analysis results
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        with open(output_dir / 'scene_analysis.json', 'w') as f:
            json.dump(scene_data, f, indent=2)
            
        console.print("\n[green]Scene analysis saved to output/scene_analysis.json[/green]")
        
    except Exception as e:
        console.print(f"[red]Error in scene analysis: {str(e)}[/red]")

if __name__ == "__main__":
    main()