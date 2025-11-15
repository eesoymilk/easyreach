#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2020-2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import platform
import subprocess
import sys
import os
import typer
from typing_extensions import Annotated


def get_ip_address(use_tailscale: bool = False) -> str:
    """Detect IP address using either Tailscale or public IP."""
    print("Detecting IP address...")

    if use_tailscale:
        try:
            result = subprocess.run(
                ["tailscale", "ip", "-4"], capture_output=True, text=True, check=True
            )
            ip = result.stdout.strip()
            if not ip:
                print("Error: Could not detect Tailscale IP. Is Tailscale running?")
                sys.exit(1)
            print(f"Detected Tailscale IP: {ip}")
            return ip
        except FileNotFoundError:
            print("Error: tailscale command not found. Please install Tailscale.")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"Error running tailscale command: {e}")
            sys.exit(1)
    else:
        try:
            result = subprocess.run(
                ["curl", "-s", "ifconfig.me"],
                capture_output=True,
                text=True,
                check=True,
                timeout=10,
            )
            ip = result.stdout.strip()
            if not ip:
                print("Error: Could not detect public IP")
                sys.exit(1)
            print(f"Detected public IP: {ip}")
            return ip
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            print(f"Error detecting public IP: {e}")
            sys.exit(1)


# Initialize Typer app
app = typer.Typer(
    help="Run Isaac Sim with livestream capabilities",
    add_completion=False,
    rich_markup_mode="rich",
)


def print_connection_info(ip: str, port: int):
    """Print connection information in a formatted box."""
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                                                            ║")
    print("║       Isaac Sim is Ready!                                 ║")
    print("║                                                            ║")
    print("║  Connect using Isaac Sim WebRTC Streaming Client:         ║")
    print("║                                                            ║")
    print(f"║  IP Address:  {ip:<44} ║")
    print(f"║  Port:        {port:<44} ║")
    print("║                                                            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()


@app.command()
def main(
    port: Annotated[int, typer.Option(help="TCP port for streaming")] = 49100,
    gpu: Annotated[int, typer.Option(help="GPU to use for rendering")] = 0,
    tailscale: Annotated[
        bool, typer.Option(help="Use Tailscale IP instead of public IP")
    ] = False,
):
    """
    Run Isaac Sim with livestream capabilities.

    Examples:
        python main.py                          # Run with defaults
        python main.py --port 8080 --gpu 1      # Custom port and GPU
        python main.py --tailscale              # Use Tailscale IP
    """
    # Exit early if running on ARM64 (aarch64) architecture
    if platform.machine().lower() in ["aarch64", "arm64"]:
        print("Livestream is not supported on ARM64 architecture. Exiting.")
        sys.exit(0)

    # Detect IP address
    endpoint_ip = get_ip_address(use_tailscale=tailscale)

    # Set GPU environment variable
    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu)

    print()
    print("Starting Isaac Sim with livestream...")
    print(f"  Port: {port}")
    print(f"  GPU: {gpu}")
    print(f"  Endpoint: {endpoint_ip}")
    print()

    # Import after setting environment variables
    from isaacsim import SimulationApp

    # Configuration for Isaac Sim
    CONFIG = {
        "width": 1280,
        "height": 720,
        "window_width": 1920,
        "window_height": 1080,
        "headless": True,
        "hide_ui": False,  # Show the GUI
        "renderer": "RaytracedLighting",
        "display_options": 3286,  # Set display options to show default grid
    }

    # Start the omniverse application
    kit = SimulationApp(launch_config=CONFIG)

    from isaacsim.core.utils.extensions import enable_extension

    # Configure livestream settings
    kit.set_setting("/app/window/drawMouse", True)
    kit.set_setting("/app/livestream/publicEndpointAddress", endpoint_ip)
    kit.set_setting("/app/livestream/port", port)
    kit.set_setting("/renderer/multiGpu/Enabled", False)
    kit.set_setting("/renderer/activeGpu", gpu)

    # Enable Livestream extension
    enable_extension("omni.services.livestream.nvcf")

    # Enable the layers and stage windows in the UI
    enable_extension("omni.kit.widget.stage")
    enable_extension("omni.kit.widget.layers")

    kit.update()

    # Print connection info
    print_connection_info(endpoint_ip, port)

    # Run until closed
    try:
        while kit._app.is_running() and not kit.is_exiting():
            # Run in realtime mode, we don't specify the step size
            kit.update()
    except KeyboardInterrupt:
        print("\nShutting down Isaac Sim...")
    finally:
        kit.close()
        print("Isaac Sim closed successfully.")


if __name__ == "__main__":
    app()
