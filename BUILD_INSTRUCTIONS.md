# Build Instructions for smdbm-wails

This document provides instructions for building the MongoDB Manager application for Linux and Windows.

## Project Location

The converted Wails project is located at: `/workspace/smdbm-wails/`

## Prerequisites Installation

### For Go 1.22+ (Required for latest Wails)

Since the current Go version (1.19) is too old for the latest Wails, you need to upgrade:

```bash
# Download and install Go 1.22
wget https://go.dev/dl/go1.22.0.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
```

### Install Wails CLI

```bash
go install github.com/wailsapp/wails/v2/cmd/wails@latest
export PATH=$PATH:$(go env GOPATH)/bin
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc
```

### Install System Dependencies (Linux)

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y libgtk-3-dev libwebkit2gtk-4.0-dev gcc-mingw-w64-x86-64

# Fedora
sudo dnf install -y gtk3-devel webkit2gtk3-devel mingw64-gcc
```

## Building the Application

### Step 1: Navigate to Project Directory

```bash
cd /workspace/smdbm-wails
```

### Step 2: Initialize Go Modules

```bash
go mod tidy
```

### Step 3: Build for Linux

```bash
wails build -platform linux/amd64
```

The output will be in `build/bin/linux/smdbm-wails`

### Step 4: Build for Windows

```bash
wails build -platform windows/amd64
```

The output will be in `build/bin/windows/smdbm-wails.exe`

### Step 5: Build for Both Platforms

You can create a build script:

```bash
#!/bin/bash
# build-all.sh

echo "Building for Linux..."
wails build -platform linux/amd64

echo "Building for Windows..."
wails build -platform windows/amd64

echo "Build complete!"
echo "Linux binary: build/bin/linux/smdbm-wails"
echo "Windows binary: build/bin/windows/smdbm-wails.exe"
```

## Alternative: Manual Build Without Wails CLI

If you cannot install Wails CLI due to disk space or other constraints, you can build manually:

### For Linux:

```bash
cd /workspace/smdbm-wails
CGO_ENABLED=1 GOOS=linux GOARCH=amd64 go build -o smdbm-wails -ldflags="-s -w"
```

### For Windows (requires cross-compiler):

```bash
cd /workspace/smdbm-wails
CGO_ENABLED=1 GOOS=windows GOARCH=amd64 CC=x86_64-w64-mingw32-gcc go build -o smdbm-wails.exe -ldflags="-s -w"
```

## Running the Application

### Linux:
```bash
./build/bin/linux/smdbm-wails
```

### Windows:
Double-click `smdbm-wails.exe` or run from command prompt:
```cmd
smdbm-wails.exe
```

## Configuration

Before running, ensure `smdbm.json` is in the same directory as the executable with your MongoDB server configurations:

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

## Troubleshooting

### Disk Space Issues

If you encounter "no space left on device" errors:

```bash
# Clean up Go module cache
go clean -modcache

# Clean up build cache
go clean -cache

# Remove old downloads
rm -rf ~/go/pkg/mod/cache
```

### Missing Dependencies

If you get compilation errors about missing packages:

```bash
go mod tidy
go get -u github.com/wailsapp/wails/v2
go get -u go.mongodb.org/mongo-driver
```

### WebView2 Not Found (Windows)

On Windows, users need to have Microsoft WebView2 installed. It comes pre-installed on most modern Windows systems, but can be downloaded from:
https://developer.microsoft.com/en-us/microsoft-edge/webview2/

## File Structure After Build

```
smdbm-wails/
├── main.go              # Entry point
├── app.go               # Backend logic
├── go.mod               # Go module file
├── wails.json           # Wails configuration
├── smdbm.json           # Server configuration
├── frontend/            # Frontend source
│   └── dist/            # Built assets
└── build/               # Build output
    └── bin/
        ├── linux/
        │   └── smdbm-wails
        └── windows/
            └── smdbm-wails.exe
```
