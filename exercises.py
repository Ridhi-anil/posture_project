def get_exercise(posture_type):

    exercises = {
        "Hunched Shoulders": "Do 10 shoulder rolls and stretch your chest.",
        "Uneven Shoulders": "Do side stretches for 20 seconds each side.",
        "Forward Head": "Perform 10 chin tucks slowly.",
        "Leaning Too Close": "Move back and adjust chair height.",
        "Good Posture": "Great job! Maintain this posture."
    }

    return exercises.get(posture_type, "Maintain good posture.")
