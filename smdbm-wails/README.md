# MongoDB Manager - Wails Application

A cross-platform MongoDB database and user management tool built with Wails (Go backend + React/Vanilla JS frontend).

## Features

- Create MongoDB databases and collections
- Generate random passwords for database users
- Assign user roles (read, readWrite, dbAdmin, dbOwner)
- Generate connection strings for new users
- Copy connection strings to clipboard
- Multiple theme support
- Cross-platform (Linux & Windows)

## Prerequisites

- Go 1.19 or later
- Node.js (for frontend development)
- GCC compiler (for building)

### Linux Prerequisites

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install libgtk-3-dev libwebkit2gtk-4.0-dev

# Fedora
sudo dnf install gtk3-devel webkit2gtk3-devel
```

### Windows Prerequisites

- Install [WebView2](https://developer.microsoft.com/en-us/microsoft-edge/webview2/)
- Install GCC (via [MinGW](https://www.mingw-w64.org/) or [MSYS2](https://www.msys2.org/))

## Installation

1. Clone or download this project

2. Navigate to the project directory:
```bash
cd smdbm-wails
```

3. Download Go dependencies:
```bash
go mod tidy
```

4. Copy your `smdbm.json` configuration file to the project root (already included as example)

## Configuration

Edit `smdbm.json` to add your MongoDB server connections:

```json
{
  "server lokal": {
    "url": "mongodb://admin:password@localhost:27017"
  },
  "server ga tau dimana": {
    "url": "mongodb://user:password@192.168.1.100:27017"
  }
}
```

## Building

### Development Mode

```bash
wails dev
```

### Production Build

#### Build for current platform:
```bash
wails build
```

#### Build for Linux:
```bash
wails build -platform linux/amd64
```

#### Build for Windows:
```bash
wails build -platform windows/amd64
```

#### Build for both platforms:
```bash
# Linux
GOOS=linux GOARCH=amd64 wails build

# Windows
GOOS=windows GOARCH=amd64 wails build
```

## Project Structure

```
smdbm-wails/
├── main.go              # Wails application entry point
├── app.go               # Backend logic and MongoDB operations
├── go.mod               # Go module definition
├── smdbm.json           # Server configuration
├── frontend/            # Frontend source code
│   ├── dist/            # Built frontend assets
│   │   ├── index.html
│   │   ├── style.css
│   │   └── app.js
│   ├── index.html       # Main HTML template
│   ├── style.css        # Stylesheet
│   ├── app.js           # Frontend JavaScript
│   └── package.json     # Node.js package config
└── build/               # Build output directory
```

## Usage

1. Launch the application
2. Select a theme from the dropdown
3. Enter a database name
4. Enter a username
5. Select a MongoDB server from the dropdown
6. Select a user role (read, readWrite, dbAdmin, dbOwner)
7. Click "Create Database & User"
8. The generated connection string will appear in the text field
9. Click "Copy" to copy the connection string to clipboard

## Themes

Available themes:
- Superhero (default)
- Flatly
- Darkly
- Cyborg
- Lumen
- Solar

## License

MIT License

## Original Project

This is a conversion of the original Python/tkinter application (`smdbm.py`) to a modern cross-platform desktop application using Wails.
