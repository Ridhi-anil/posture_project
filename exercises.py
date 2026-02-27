def get_exercise(posture_type):

    exercises = {
        "Hunched Shoulders": "Do 10 shoulder rolls and stretch your chest.",
        "Uneven Shoulders": "Do side stretches for 20 seconds each side.",
        "Forward Head": "Perform 10 chin tucks slowly.",
        "Leaning Too Close": "Move back and adjust chair height.",
        "Good Posture": "Great job! Maintain this posture."
    }

    return exercises.get(posture_type, "Maintain good posture.")


def get_exercise_media(posture_issue):
    mapping = {
        "Hunched Shoulders": "assets/shoulder_roll.gif",
        "Uneven Shoulders": "assets/side_stretch.gif",
        "Forward Head": "assets/Chin_tucks.gif",
        "Leaning Too Close": "assets/neck_stretch.gif"
    }

    return mapping.get(posture_issue, None)
