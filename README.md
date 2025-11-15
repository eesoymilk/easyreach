# EasyReach

A Python launcher for NVIDIA Isaac Sim with WebRTC livestream capabilities, featuring Tailscale support for easy remote access.

## Features

- WebRTC livestream support for headless Isaac Sim instances
- Automatic IP detection (public or Tailscale)
- Configurable GPU and port settings
- Clean CLI interface with `typer`
- ARM64 architecture detection and graceful exit

## Requirements

- NVIDIA Isaac Sim installed locally
- Python 3.8+
- Required Python packages:
  - `typer`
  - `typing-extensions`
- Optional: [Tailscale](https://tailscale.com/) for private network streaming

## Installation

1. Clone the repository:
```bash
git clone https://github.com/eesoymilk/easyreach.git
cd easyreach
```

2. Install Python dependencies:
```bash
pip install typer typing-extensions
```

3. Make sure Isaac Sim is installed and the `isaacsim` Python package is available

## Usage

### Basic Usage

Run with default settings (port 49100, GPU 0, public IP):
```bash
python main.py
```

### Custom Port and GPU

Specify a custom port and GPU:
```bash
python main.py --port 8080 --gpu 1
```

### Using Tailscale

Use Tailscale IP for private network streaming:
```bash
python main.py --tailscale
```

### Command-Line Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--port` | int | 49100 | TCP port for WebRTC streaming |
| `--gpu` | int | 0 | GPU device to use for rendering |
| `--tailscale` | flag | false | Use Tailscale IP instead of public IP |
| `--help` | flag | - | Show help message |

## How It Works

1. **IP Detection**: Automatically detects your public IP (via `ifconfig.me`) or Tailscale IP
2. **Environment Setup**: Configures GPU selection via `CUDA_VISIBLE_DEVICES`
3. **Isaac Sim Launch**: Starts Isaac Sim with headless mode and livestream configuration
4. **Extension Loading**: Enables livestream, stage, and layers extensions
5. **Connection Info**: Displays WebRTC connection details in a formatted box

## Connecting to the Stream

After starting the script, you'll see connection information:

```
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║       Isaac Sim is Ready!                                 ║
║                                                            ║
║  Connect using Isaac Sim WebRTC Streaming Client:         ║
║                                                            ║
║  IP Address:  xxx.xxx.xxx.xxx                             ║
║  Port:        49100                                        ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

Use the **Isaac Sim WebRTC Streaming Client** with these credentials to connect.

## Graceful Shutdown

Press `Ctrl+C` to gracefully shut down Isaac Sim:
```
^C
Shutting down Isaac Sim...
Isaac Sim closed successfully.
```

## Troubleshooting

### Cannot detect public IP
- Check your internet connection
- Ensure `curl` is installed and can reach `ifconfig.me`

### Tailscale IP not found
- Verify Tailscale is installed: `tailscale version`
- Check Tailscale is running: `tailscale status`
- Ensure you're connected to your Tailscale network

### Import errors for `isaacsim`
- Verify Isaac Sim is properly installed
- Ensure you're using the correct Python environment
- You may need to source Isaac Sim's Python environment first

### ARM64 Architecture
This script automatically detects ARM64/aarch64 architecture and exits, as Isaac Sim livestream is not supported on ARM platforms.

## License

Apache-2.0

## Credits

Based on NVIDIA Isaac Sim examples and streaming documentation.
