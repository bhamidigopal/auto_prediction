# src/test_model.py

import requests
from rich.console import Console

console = Console()

def test_model_connection():
    """Test basic model connectivity"""
    url = "http://localhost:8080/completion"
    
    # Test prompt using model's chat template
    prompt = """<|system|>
You are a helpful assistant
<|endoftext|>
<|user|>
Generate a simple test case
<|endoftext|>
<|assistant|>"""

    try:
        response = requests.post(
            url,
            json={
                "prompt": prompt,
                "max_tokens": 100
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            console.print("[green]✓ Successfully connected to model[/green]")
            console.print("\nModel response:")
            console.print(response.json()['content'])
            return True
        else:
            console.print(f"[red]Failed to get response from model: Status {response.status_code}[/red]")
            return False
            
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Connection error: {str(e)}[/red]")
        return False

if __name__ == "__main__":
    test_model_connection()