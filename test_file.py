import requests
import json

API_URL = "http://localhost:8000/generate-docs/"

def test_display_formats():
    print("🚀 Sending code to agent...\n")
    
    # Simple code to test
    raw_code = """
def multiply(a, b):
    return a * b
    """
    
    try:
        response = requests.post(API_URL, json={"code": raw_code})
        
        if response.status_code == 200:
            data = response.json()
            
            # --- DISPLAY 1: RAW JSON ---
            print("👇 [FORMAT 1: JSON OUTPUT] 👇")
            print(json.dumps(data, indent=2))
            print("-" * 60)
            
            # --- DISPLAY 2: NORMAL TEXT ---
            print("👇 [FORMAT 2: NORMAL TEXT/CODE] 👇")
            # Extract the string from the JSON
            clean_code = data.get("documented_code", "")
            print(clean_code)
            print("-" * 60)
            
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {str(e)}")

if __name__ == "__main__":
    test_display_formats()