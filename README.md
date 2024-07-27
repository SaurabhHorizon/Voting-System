# Face Recognition Voting System

This project implements a face recognition voting system using Flask and OpenCV. The system recognizes voters using facial recognition, and allows them to cast votes for different political parties. The votes are stored and can be retrieved for tallying.

## Features

- **Facial Recognition**: Uses OpenCV's Haar Cascade for face detection and LBPH Face Recognizer for face recognition.
- **Voting System**: Allows authenticated users to cast votes for predefined parties.
- **Web Interface**: Provides a web-based interface for interaction, including voting and viewing video feed.
- **Vote Storage**: Stores votes in a text file for persistence.

## Files

- `app.py`: Main Flask application that handles routes and server-side logic.
- `FER_Camera.py`: Contains classes and functions for camera handling, face recognition, and voting logic.
- `haarcascade_frontalface_default.xml`: XML file for Haar Cascade face detection.
- `party_votes.txt`: Stores the vote count for each party.

## Requirements

- Python 3.x
- Flask
- OpenCV
- NumPy

## Setup

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd <repository-folder>
    ```

2. **Install dependencies**:
    ```sh
    pip install flask opencv-python-headless numpy
    ```
   **Training data**
``` python train.py <Name of the person> ```
3. **Run the application**:
    ```sh
    python app.py
    ```

4. **Access the web interface**:
    Open your browser and go to `http://127.0.0.1:5000/`

## Usage

- **Homepage**: Displays the homepage of the application.
- **Vote**: Cast your vote by selecting a party. This can be done via `/vote?party=<party_name>`.
- **Get Status**: Retrieve the status of the current voter via `/get_status`.
- **Video Feed**: Access the video feed from the camera via `/video_feed`.
- **Video Page**: View the video feed along with party options via `/video`.

## Code Structure

### `app.py`
- Initializes the Flask app.
- Defines routes for the homepage, voting, status check, video feed, and video page.
- Manages the camera instance and video streaming.

### `FER_Camera.py`
- **Party Class**: Represents a political party.
- **Voter Class**: Represents a voter.
- **VideoCamera Class**: Handles video capturing, face recognition, and voting logic.
- **write_party_votes Function**: Writes the current vote counts to `party_votes.txt`.

### `haarcascade_frontalface_default.xml`
- Pre-trained model for face detection.

### `party_votes.txt`
- Stores vote counts in the format:
    ```
    BJP : 0
    CONGRESS : 0
    BSP : 1
    AAP : 0
    SP : 0
    ```

## Authors

- Saurabh Nayak

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Image: 
![image](https://github.com/SaurabhHorizon/Online-Voting/assets/75537121/5cfae971-522c-4b90-b06a-e077138dcd72)


Feel free to modify and expand upon this README as necessary.
