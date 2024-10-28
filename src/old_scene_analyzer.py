# src/scenario_generator.py

import zarr
import numpy as np
from rich.console import Console
from rich.progress import Progress
import requests
import json
from pathlib import Path

console = Console()

class ToyotaScenarioGenerator:
    def __init__(self, zarr_path="sample.zarr", model_url="http://localhost:8080/completion"):
        self.zarr_path = zarr_path
        self.model_url = model_url
        self.agent_types = {
            3: "VEHICLE",
            1: "PEDESTRIAN",
            2: "BICYCLE",
            4: "MOTORCYCLE",
            5: "CYCLIST"
        }

    def extract_scene_context(self, scene_idx=0):
        """Extract rich context from a scene"""
        root = zarr.open(self.zarr_path, mode='r')
        scene = root['scenes'][scene_idx]
        
        # Get all frames for this scene
        frames = root['frames'][scene['frame_index_interval'][0]:scene['frame_index_interval'][1]]
        
        # Get first and last frame for trajectory analysis
        first_frame = frames[0]
        last_frame = frames[-1]
        
        # Get agents and their trajectories
        initial_agents = root['agents'][first_frame['agent_index_interval'][0]:
                                      first_frame['agent_index_interval'][1]]
        final_agents = root['agents'][last_frame['agent_index_interval'][0]:
                                    last_frame['agent_index_interval'][1]]

        # Get traffic light states if available
        traffic_lights = []
        if 'traffic_light_faces_index_interval' in first_frame.dtype.names:
            tl_start, tl_end = first_frame['traffic_light_faces_index_interval']
            traffic_lights = root['traffic_light_faces'][tl_start:tl_end]

        return {
            "scene_info": {
                "duration": (scene['end_time'] - scene['start_time']) / 1e9,  # Convert to seconds
                "num_frames": len(frames),
                "host": scene['host']
            },
            "ego_vehicle": {
                "initial_position": first_frame['ego_translation'].tolist(),
                "final_position": last_frame['ego_translation'].tolist(),
                "initial_rotation": first_frame['ego_rotation'].tolist()
            },
            "agents": self._analyze_agents(initial_agents, final_agents),
            "traffic": self._analyze_traffic(traffic_lights) if traffic_lights else None
        }

    def _analyze_agents(self, initial_agents, final_agents):
        """Analyze agent behaviors and interactions"""
        agents_analysis = []
        
        for i_agent, f_agent in zip(initial_agents, final_agents):
            # Get agent type
            agent_type = self.agent_types.get(
                np.argmax(i_agent['label_probabilities']), "UNKNOWN"
            )
            
            # Calculate trajectory
            displacement = f_agent['centroid'] - i_agent['centroid']
            avg_velocity = displacement / 5.0  # Assuming 5 second scenes
            
            agents_analysis.append({
                "type": agent_type,
                "track_id": int(i_agent['track_id']),
                "trajectory": {
                    "initial_position": i_agent['centroid'].tolist(),
                    "final_position": f_agent['centroid'].tolist(),
                    "initial_velocity": i_agent['velocity'].tolist(),
                    "average_velocity": avg_velocity.tolist(),
                    "initial_heading": float(i_agent['yaw']),
                    "final_heading": float(f_agent['yaw'])
                },
                "size": i_agent['extent'].tolist()
            })
            
        return agents_analysis

    def _analyze_traffic(self, traffic_lights):
        """Analyze traffic light states"""
        return [{
            "id": str(tl['face_id']),
            "status": np.argmax(tl['traffic_light_face_status'])
        } for tl in traffic_lights]

    def generate_scenario(self, scene_context):
        """Generate comprehensive test scenario"""
        # Create rich context prompt
        prompt = f"""<|system|>
You are a test scenario generator for autonomous vehicles. Generate detailed BDD-style test scenarios 
based on real traffic data from the Toyota Woven Platform.
<|endoftext|>
<|user|>
Create a comprehensive test scenario for the following real-world traffic situation:

Scene Duration: {scene_context['scene_info']['duration']:.2f} seconds
Location: Recorded by {scene_context['scene_info']['host']}

Ego Vehicle:
- Initial Position: {scene_context['ego_vehicle']['initial_position']}
- Final Position: {scene_context['ego_vehicle']['final_position']}

Other Agents ({len(scene_context['agents'])} total):
{self._format_agents(scene_context['agents'])}

Traffic Context:
{self._format_traffic(scene_context['traffic'])}

Generate a BDD format test scenario that includes:
1. Initial scene setup
2. Multiple agent interactions
3. Traffic rule compliance
4. Safety requirements
5. Expected outcomes
<|endoftext|>
<|assistant|>"""

        try:
            response = requests.post(
                self.model_url,
                json={
                    "prompt": prompt,
                    "max_tokens": 1000,
                    "temperature": 0.7
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return response.json()['content']
            else:
                console.print(f"[red]Error: {response.status_code} - {response.text}[/red]")
                return None
                
        except Exception as e:
            console.print(f"[red]Request error: {str(e)}[/red]")
            return None

    def _format_agents(self, agents):
        """Format agent information for prompt"""
        agent_descriptions = []
        for agent in agents:
            desc = f"""- {agent['type']}:
  * Track ID: {agent['track_id']}
  * Movement: {agent['trajectory']['initial_position']} → {agent['trajectory']['final_position']}
  * Speed: {np.linalg.norm(agent['trajectory']['average_velocity']):.2f} m/s
  * Size: {agent['size']} (L×W×H)"""
            agent_descriptions.append(desc)
        return "\n".join(agent_descriptions)

    def _format_traffic(self, traffic_data):
        if not traffic_data:
            return "No traffic light data available"
            
        status_map = {0: "RED", 1: "YELLOW", 2: "GREEN"}
        traffic_desc = ["Traffic Light States:"]
        for light in traffic_data:
            traffic_desc.append(f"- Light {light['id']}: {status_map.get(light['status'], 'UNKNOWN')}")
        return "\n".join(traffic_desc)

def main():
    generator = ToyotaScenarioGenerator()
    
    try:
        # Extract scene context
        console.print("[yellow]Extracting scene context...[/yellow]")
        scene_context = generator.extract_scene_context()
        
        # Generate scenario
        console.print("[yellow]Generating scenario...[/yellow]")
        scenario = generator.generate_scenario(scene_context)
        
        if scenario:
            # Save results
            output = {
                "scene_context": scene_context,
                "generated_scenario": scenario
            }
            
            with open('output/detailed_scenario.json', 'w') as f:
                json.dump(output, f, indent=2)
            
            console.print("\n[bold green]Generated Scenario:[/bold green]")
            console.print(scenario)
            console.print("\n[green]✓ Scenario saved to output/detailed_scenario.json[/green]")
            
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

if __name__ == "__main__":
    main()