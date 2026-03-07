import requests
import sys

def verify():
    print("--- BUBEX Backend Verification ---")
    
    # 1. Check if server is reachable
    try:
        response = requests.get("http://localhost:8000/api/movies/")
        if response.status_code == 200:
            print("[SUCCESS] Backend API is reachable!")
            movies = response.json()
            print(f"[INFO] Found {len(movies)} movies in database.")
            for movie in movies:
                print(f" - {movie.get('title')} (ID: {movie.get('id')})")
        else:
            print(f"[FAILED] Backend API returned status {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Could not connect to backend: {e}")
        print("Tip: Make sure to run 'python manage.py runserver' first!")

    # 2. Check Scan Endpoint
    print("\nChecking Scan Endpoint...")
    try:
        response = requests.post("http://localhost:8000/api/scan/")
        # We expect a 400 because we didn't send a video, but it proves the route exists
        if response.status_code == 400:
            print("[SUCCESS] Scan API route is active.")
        else:
            print(f"[INFO] Scan API returned {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Scan endpoint check failed: {e}")

if __name__ == "__main__":
    verify()
