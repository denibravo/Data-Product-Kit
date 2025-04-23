import requests
import os
from dotenv import load_dotenv

def check_missing_agencies_from_url(file_path: str, api_url: str):
    """
    Check for missing agencies by comparing the agencies in the agencies.txt file
    with the agencies fetched from the regulations.gov API.
    If any missing agencies are found, they are appended to the file.
    """
    try:
        # Fetch the latest agencies from the URL
        response = requests.get(api_url)
        response.raise_for_status()
        regulations_data = response.json()

        # Extract agency IDs and names from the API response
        regulations_agencies = {
            agency.get("id"): agency.get("attributes", {}).get("name", "Unknown Agency")
            for agency in regulations_data.get("data", [])
        }

        if not regulations_agencies:
            print("No agency IDs found in the API response.")
            return

        # Read the agencies from the text file
        file_agencies = {}
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('#'):
                    continue 
                try:
                    agency_id, agency_name = line.strip().split('|')
                    file_agencies[agency_id] = agency_name
                # Skip over and identify malformed lines   
                except ValueError:
                    print(f"Skipping malformed line in agencies.txt: {line.strip()}")
                    continue

        # Identify missing agencies
        missing_agencies = {
            agency_id: agency_name
            for agency_id, agency_name in regulations_agencies.items()
            if agency_id not in file_agencies
        }

        # Add missing agencies to text file
        if missing_agencies:
            with open(file_path, 'a') as file:
                for agency_id, agency_name in missing_agencies.items():
                    file.write(f"\n{agency_id}|{agency_name}")
            print(f"Added {len(missing_agencies)} missing agencies to '{file_path}'.")
        else:
            print("No missing agencies. The agencies.txt file is up to date.")

    except requests.RequestException as e:
        print(f"Error fetching data from the URL: {e}")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    load_dotenv()

    # Fetch the API key from .env file, otherwise prompt the user to set it
    api_key = os.getenv("REGULATIONS_API_KEY")
    if not api_key:
        print("Error: API key not found. Please set the 'REGULATIONS_API_KEY' environment variable.")
        return

    # Path to the agencies.txt file
    file_path = "agencies.txt"

    # URL to fetch agencies from regulations.gov based on user's API key
    api_url = f"https://api.regulations.gov/v4/agencies?api_key={api_key}"

    check_missing_agencies_from_url(file_path, api_url)

if __name__ == "__main__":
    main()
