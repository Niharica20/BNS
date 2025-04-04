import pyttsx3
import speech_recognition as sr
from geopy.distance import geodesic
from geopy import Point
from geopy.distance import great_circle
import json
import time
import difflib
import math

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 160)  
engine.setProperty("volume", 1.0)

# Load university locations from GeoJSON
with open("university_map.geojson", "r", encoding="utf-8") as file:
    university_map = json.load(file)

# Extract locations into a dictionary
locations = {}
for feature in university_map["features"]:
    name = feature["properties"].get("name", "").strip().lower()  # Clean location names
    coordinates = feature["geometry"]["coordinates"]
    if name:
        locations[name] = tuple(reversed(coordinates))  # Convert (lat, lon)

# Function to simulate getting real-time GPS location (Replace with real GPS input)
def get_current_location():
    return (30.7715, 76.5755)  # Replace with actual GPS data

# Function to calculate the bearing angle
def calculate_bearing(start, end):
    """Calculate bearing (direction) from start point to end point."""
    lat1, lon1 = math.radians(start[0]), math.radians(start[1])
    lat2, lon2 = math.radians(end[0]), math.radians(end[1])

    delta_lon = lon2 - lon1
    x = math.sin(delta_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)
    bearing = math.degrees(math.atan2(x, y))

    return (bearing + 360) % 360  # Normalize to 0-360 degrees

# Function to determine movement direction
def get_direction(current_location, target_location):
    """Determine the best movement direction based on bearing."""
    bearing = calculate_bearing(current_location, target_location)
    
    if 45 <= bearing < 135:
        return "Move Right"
    elif 135 <= bearing < 225:
        return "Move Backward"
    elif 225 <= bearing < 315:
        return "Move Left"
    else:
        return "Move Forward"

# Navigation function
def navigate_to(destination):
    """Guides the user towards a predefined location."""
    target_location = locations[destination]
    print(f"✅ Navigating to {destination} → 📍 Coordinates: {target_location}")
    engine.say(f"Navigating to {destination}")
    engine.runAndWait()

    last_direction = None  # Prevent repeating same direction

    while True:
        current_location = get_current_location()
        distance = geodesic(current_location, target_location).meters  # Distance in meters

        if distance < 3:  # User has reached the destination
            engine.say(f"You have reached {destination}.")
            engine.runAndWait()
            break

        # Determine movement direction
        direction = get_direction(current_location, target_location)

        # Only announce if direction changes (to avoid repetition)
        if direction != last_direction:
            print(f"📍 Distance: {distance:.2f} meters | Direction: {direction}")
            engine.say(f"{direction}, {int(distance)} meters remaining.")
            engine.runAndWait()
            last_direction = direction

        time.sleep(5)  # Delay before updating again

# Function to capture voice command
def get_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening for destination...")
        engine.say("Where do you want to go?")
        engine.runAndWait()

        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"User said: {command}")
            return command
        except sr.UnknownValueError:
            print("❌ Could not understand the audio.")
            engine.say("I couldn't understand you. Please try again.")
            engine.runAndWait()
            return None
        except sr.WaitTimeoutError:
            print("⏳ No speech detected. Try again.")
            engine.say("I didn't hear anything. Please try again.")
            engine.runAndWait()
            return None
        except sr.RequestError:
            print("❌ Speech Recognition service is unavailable.")
            engine.say("Speech Recognition service is unavailable.")
            engine.runAndWait()
            return None

# Function to find the closest match for the spoken destination
def find_closest_match(user_input, location_list):
    matches = difflib.get_close_matches(user_input.lower(), location_list, n=1, cutoff=0.5)
    return matches[0] if matches else None

if __name__ == "__main__":
    engine.say("Please say your destination.")
    engine.runAndWait()
    destination = get_voice_command()

    if destination:
        # Normalize location names for better matching
        normalized_locations = {key.lower(): key for key in locations.keys()}
        matched_location = find_closest_match(destination.lower(), normalized_locations.keys())

        if matched_location:
            navigate_to(normalized_locations[matched_location])  # Navigate to best-matched location
        else:
            engine.say("Destination not recognized. Try again.")
            engine.runAndWait()
