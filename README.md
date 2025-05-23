# RIGHT-TO-MUSIC

<div align="center">

[![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-v18.2.0-blue.svg)](https://reactjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

</div>

A full-stack application for music identification and management using audio fingerprinting technology. Built with Python backend and React.js frontend.

## Dataset

The project includes a test dataset consisting of:
- 10 original full-length songs for training
- 5-second snippets of each song taken at different time intervals
- Labeled CSV mapping files for testing and validation
- Both small and large test sets for comprehensive algorithm evaluation

## Quick Start

### Prerequisites

#### Backend
- Python 3.6+
- FFmpeg (for audio processing)
- pip package manager

#### Frontend
- Node.js 14+ and npm
- Modern web browser with WebAssembly support
- System audio drivers for audio capture

### Installation

1. Clone the repository:
```bash
git clone https://github.com/shivamk1075/Right-To-Music
cd Right-To-Music
```

2. Install backend dependencies:
```bash
cd Project/server
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd ../client
npm install
```

## 💻 Usage

### Starting the Backend Server
```bash
cd Project/server
python main.py serve --proto http -p 5000
```

### Starting the Frontend Development Server
```bash
cd Project/client
npm start
```
The application will be available at `http://localhost:3000`

### Basic Commands
```bash
# Find a song from a file (Backend)
python main.py find <file_path>

# Download from Spotify (Backend)
python main.py download <spotify_url>

# Erase all downloaded songs (Backend)
python main.py erase

# Erase a specific song by ID (Backend)
python main.py eraseID <SongID>
```

## Technical Details

### Audio Fingerprinting

The project uses a custom implementation of audio fingerprinting technology, similar to Shazam's algorithm:

1. Audio Processing ([`spectrogram.py`](Project/server/shazam/spectrogram.py))
   - Converts audio to spectrogram
   - Uses FFT (Fast Fourier Transform) for frequency analysis

2. Fingerprint Generation ([`fingerprint.py`](Project/server/shazam/fingerprint.py))
   - Creates unique audio fingerprints
   - Stores in SQLite database for quick matching

### Database Structure

The SQLite database ([`sqlite.py`](Project/server/db/sqlite.py)) maintains:
- Song metadata (title, artist, YouTube ID)
- Audio fingerprints
- Relationship mappings


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project was inspired by an open-source Go implementation by Chigozirim Igweamaka (MIT Licensed). The codebase has been fully re-implemented in Python by Shivam.

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## Contact

shivam.kumar.101075@gmail.com

---

<div align="center">
  <p>
    <a href="https://github.com/shivamk1075/Right-To-Music/stargazers">
      <img src="https://img.shields.io/github/stars/shivamk1075/Right-To-Music?style=social" alt="Github Stars" />
    </a>&nbsp;&nbsp;
    <a href="https://github.com/shivamk1075/Right-To-Music/network/members">
      <img src="https://img.shields.io/github/forks/shivamk1075/Right-To-Music?style=social" alt="Github Forks" />
    </a>
  </p>
  
  <p><strong>⭐ If you find this project useful, please consider giving it a star!</strong></p>
  
  <p>
    <a href="https://github.com/shivamk1075/Right-To-Music/issues">Report Bug</a> · 
    <a href="https://github.com/shivamk1075/Right-To-Music/issues">Request Feature</a>
  </p>
</div>
