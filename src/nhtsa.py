import requests
from rich.console import Console
import pandas as pd
import os
from datetime import datetime
import logging

console = Console()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=f'feature_generation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
)

class FeatureGenerator:
    def __init__(self, granite_url="http://localhost:8080/completion"):
        self.granite_url = granite_url
        self.console = Console()
        self.data = None

    def load_data(self, url):
        """Load NHTSA data from URL"""
        try:
            self.data = pd.read_csv(url)
            logging.info(f"Loaded {len(self.data)} vehicle records")
            return True
        except Exception as e:
            logging.error(f"Failed to load data: {str(e)}")
            return False

    def generate_feature_prompt(self, vehicle_data):
        """Create prompt for Granite to generate BDD features"""
        prompt = f"""<|system|>
You are a BDD test expert. Create Gherkin-style feature files for vehicle safety testing based on this data:

Make: {vehicle_data['MAKE']}
Model: {vehicle_data['MODEL']}
Year: {vehicle_data['MODEL_YR']}
Safety Features:
- Overall Rating: {vehicle_data.get('OVERALL_STARS', 'N/A')}
- Front Collision Warning: {vehicle_data.get('FRNT_COLLISION_WARNING', 'N/A')}
- Lane Departure Warning: {vehicle_data.get('LANE_DEPARTURE_WARNING', 'N/A')}
- Crash Imminent Brake: {vehicle_data.get('CRASH_IMMINENT_BRAKE', 'N/A')}
- Dynamic Brake Support: {vehicle_data.get('DYNAMIC_BRAKE_SUPPORT', 'N/A')}
- Blind Spot Detection: {vehicle_data.get('BLIND_SPOT_DETECTION', 'N/A')}

Generate a Gherkin feature file that includes scenarios for:
1. Basic safety rating validation
2. Advanced safety feature verification
3. NHTSA compliance checks
4. Crash test performance validation

Use standard Gherkin format with Feature, Scenario, Given, When, Then.
<|endoftext|>
<|user|>
Create a comprehensive BDD feature file for testing this vehicle's safety features.
<|endoftext|>
<|assistant|>"""
        return prompt

    def get_granite_response(self, prompt):
        """Send prompt to Granite and get response"""
        try:
            response = requests.post(
                self.granite_url,
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
                logging.error(f"Granite API error: Status {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Granite API error: {str(e)}")
            return None

    def save_feature_file(self, content, make, model, year):
        """Save generated feature file"""
        directory = "features"
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        filename = f"{directory}/{make.lower()}_{model.lower()}_{year}_safety.feature"
        
        with open(filename, 'w') as f:
            f.write(content)
            
        return filename

    def generate_features(self, num_vehicles=5):
        """Generate feature files for multiple vehicles"""
        if self.data is None:
            console.print("[red]No data loaded. Please load data first.[/red]")
            return
            
        # Sample vehicles ensuring different makes
        vehicles = self.data.groupby('MAKE').sample(n=1).head(num_vehicles)
        
        generated_files = []
        
        for _, vehicle in vehicles.iterrows():
            console.print(f"\n[bold]Generating features for {vehicle['MAKE']} {vehicle['MODEL']} {vehicle['MODEL_YR']}[/bold]")
            
            prompt = self.generate_feature_prompt(vehicle)
            feature_content = self.get_granite_response(prompt)
            
            if feature_content:
                filename = self.save_feature_file(
                    feature_content,
                    vehicle['MAKE'],
                    vehicle['MODEL'],
                    vehicle['MODEL_YR']
                )
                generated_files.append(filename)
                console.print(f"[green]✓ Generated feature file: {filename}[/green]")
            else:
                console.print(f"[red]Failed to generate features for {vehicle['MAKE']} {vehicle['MODEL']}[/red]")
                
        return generated_files

def main():
    generator = FeatureGenerator()
    
    # Load NHTSA data
    console.print("[bold]Loading NHTSA dataset...[/bold]")
    success = generator.load_data("https://static.nhtsa.gov/nhtsa/downloads/Safercar/Safercar_data.csv")
    
    if not success:
        console.print("[red]Failed to load NHTSA data. Exiting.[/red]")
        return
        
    console.print("[green]Dataset loaded successfully![/green]")
    
    # Generate features
    console.print("\n[bold]Generating BDD features...[/bold]")
    files = generator.generate_features(num_vehicles=5)
    
    if files:
        console.print("\n[bold green]Feature generation complete![/bold green]")
        console.print("\nGenerated feature files:")
        for file in files:
            console.print(f"- {file}")
    else:
        console.print("[red]No feature files were generated.[/red]")

if __name__ == "__main__":
    main()