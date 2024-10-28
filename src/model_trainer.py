# src/model_trainer.py

import requests
import json
from rich.console import Console
from rich.progress import Progress
from pathlib import Path

console = Console()

class GraniteModelTrainer:
    def __init__(self, model_url="http://localhost:8080/completion"):  # Fixed endpoint
        self.model_url = model_url

    def generate_scenario(self, agent_data):
        """Generate test scenario for an agent"""
        prompt = f"""<|system|>
You are a test scenario generator for autonomous vehicles. Generate BDD-style test scenarios.
<|endoftext|>
<|user|>
Create a test scenario for:
Agent Type: {agent_data['type']}
Position: {agent_data['position']}
Velocity: {agent_data['velocity']}
Heading: {agent_data['heading']}

Format as:
Feature: [Feature Name]
Scenario: [Scenario Name]
  Given [initial conditions]
  When [actions]
  Then [expected results]
<|endoftext|>
<|assistant|>"""

        try:
            response = requests.post(
                self.model_url,
                json={
                    "prompt": prompt,
                    "max_tokens": 500,
                    "temperature": 0.7,
                    "top_p": 0.9
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return response.json().get('content', '')
            else:
                console.print(f"[red]Error: {response.status_code} - {response.text}[/red]")
                return None
                
        except Exception as e:
            console.print(f"[red]Request error: {str(e)}[/red]")
            return None

    def generate_test_suite(self, scene_analysis_path="output/scene_analysis.json"):
        """Generate test scenarios from scene analysis"""
        console.print("\n[bold blue]Generating Test Scenarios[/bold blue]")
        
        try:
            # Load scene data
            with open(scene_analysis_path) as f:
                scene_data = json.load(f)
            
            scenarios = []
            with Progress() as progress:
                task = progress.add_task("Generating scenarios...", total=len(scene_data['agents']))
                
                for agent in scene_data['agents']:
                    console.print(f"\n[cyan]Generating scenario for {agent['type']}...[/cyan]")
                    
                    scenario = self.generate_scenario(agent)
                    if scenario:
                        scenarios.append({
                            "agent_data": agent,
                            "generated_scenario": scenario
                        })
                        console.print("[green]✓ Scenario generated[/green]")
                    
                    progress.advance(task)
            
            # Save generated scenarios
            if scenarios:
                output_dir = Path('output')
                output_dir.mkdir(exist_ok=True)
                
                with open(output_dir / 'generated_scenarios.json', 'w') as f:
                    json.dump(scenarios, f, indent=2)
                
                # Display sample scenario
                console.print("\n[bold]Sample Generated Scenario:[/bold]")
                console.print(scenarios[0]['generated_scenario'])
                
                console.print("\n[green]✓ All scenarios saved to output/generated_scenarios.json[/green]")
                return True
            
            return False
            
        except Exception as e:
            console.print(f"[red]Error generating test suite: {str(e)}[/red]")
            return False

def main():
    try:
        # First test the model connection
        test_prompt = """<|system|>
You are a helpful assistant
<|endoftext|>
<|user|>
Hello
<|endoftext|>
<|assistant|>"""

        model = GraniteModelTrainer()
        
        console.print("[yellow]Testing model connection...[/yellow]")
        response = requests.post(
            model.model_url,
            json={"prompt": test_prompt, "max_tokens": 10},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            console.print("[green]✓ Model connection successful[/green]")
            
            # Generate test scenarios
            success = model.generate_test_suite()
            
            if success:
                console.print("\n[bold green]Test generation completed successfully![/bold green]")
            else:
                console.print("\n[bold red]Test generation failed.[/bold red]")
        else:
            console.print(f"[red]Failed to connect to model: {response.status_code} - {response.text}[/red]")
            
    except Exception as e:
        console.print(f"[red]Error in main execution: {str(e)}[/red]")

if __name__ == "__main__":
    main()