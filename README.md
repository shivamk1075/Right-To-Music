# RIGHT-TO-MUSIC 🎵

<div align="center">

[![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-v18.2.0-blue.svg)](https://reactjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

<h3>🎵 Identify, Download, and Manage Music with AI-Powered Audio Fingerprinting 🎵</h3>

[Features](#-features) •
[Installation](#-getting-started) •
[Usage](#-usage) •
[Documentation](#-technical-details) •
[Contributing](#-contributing)

</div>

---

## 📖 Overview

A powerful full-stack application that combines the accuracy of Shazam-like audio fingerprinting with modern web technologies. Built with Python and React.js, it offers both CLI and web interface for seamless music identification and management.

## 🌟 Features

### Backend Features
- **Song Identification**: Find and identify songs using audio fingerprinting ([`MainShazam.py`](Project/server/shazam/MainShazam.py))
- **Spotify Integration**: Download tracks directly from Spotify URLs ([`getYT.py`](Project/server/spotify/getYT.py))
- **Local Server**: Host your own music identification server with HTTP/HTTPS support
- **Database Management**: SQLite-based song and fingerprint storage ([`sqlite.py`](Project/server/db/sqlite.py))
- **Excel Export**: Export your music database to Excel ([`DBinspect.py`](Project/server/DBinspect.py))
- **WAV Processing**: Advanced WAV file handling and conversion ([`wavFuncs.py`](Project/server/wav/wavFuncs.py))

### Frontend Features (React.js)
- **Modern UI**: Beautiful and responsive interface with gradient backgrounds and modern card layouts
- **Real-time Audio Recognition**: Record audio from both microphone and system audio
- **WebAssembly Integration**: Fast audio fingerprinting using WASM
- **Socket.IO Integration**: Real-time communication with the backend server
- **Rich Animations**: Smooth transitions and loading states
- **Cross-Platform**: Works on both desktop and mobile devices
- **Song Statistics**: Live counter showing total songs in the database
- **Toast Notifications**: User-friendly status updates and notifications

## 🚀 Getting Started

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

## 🏗️ Project Structure

```
├── Project/
│   ├── client/                # React frontend application
│   │   ├── public/           # Static files
│   │   ├── src/             # Source code
│   │   │   ├── components/  # React components
│   │   │   ├── styles/     # CSS modules
│   │   │   └── App.js      # Main application component
│   │   └── package.json    # Frontend dependencies
│   │
│   └── server/              # Python backend application
│       ├── main.py         # Main entry point and CLI handler
│       ├── CMD.py          # Command implementation
│       ├── DBinspect.py    # Database inspection
│       ├── params.py       # Configuration parameters
│       ├── Sockets.py      # Network socket handling
│       ├── db/            # Database management
│       ├── shazam/        # Audio fingerprinting
│       ├── spotify/       # Spotify integration
│       ├── wav/          # WAV file processing
│       └── utils/        # Helper utilities
│
└── Audio_Dataset/          # Test audio files and mappings
```

## 🛠️ Technical Details

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

### Server Component

The server provides:
- RESTful API endpoints
- Real-time audio processing
- Secure HTTPS support
- Cross-platform compatibility

## 📈 Future Improvements

- [ ] Add batch processing for multiple files
- [ ] Implement caching for faster lookups
- [ ] Add support for more music platforms
- [ ] Improve fingerprint matching accuracy
- [ ] Add API documentation

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgments

Note: This project was inspired by an open-source Go implementation by Chigozirim Igweamaka (MIT Licensed). The codebase has been fully re-implemented in Python by Shivam.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

## 📞 Contact

shivam.kumar.101075@gmail.com
<!-- <div align="center">
  <a href="https://github.com/shivamk1075">
    <img src="https://img.shields.io/badge/-Github-181717?style=for-the-badge&logo=Github&logoColor=white" />
  </a>&nbsp;
  <!-- Add your LinkedIn if you have one -->
  <!-- <a href="mailto:shivam.kumar.101075@gmail.com">
    <img src="https://img.shields.io/badge/-Email-EA4335?style=for-the-badge&logo=Gmail&logoColor=white" />
  </a>
</div> --> 

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
