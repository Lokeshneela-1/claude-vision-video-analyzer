#!/usr/bin/env python3
"""
Test script to verify Claude Vision Video Analyzer setup.
"""

import sys
import subprocess
from pathlib import Path


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def check_python():
    """Check Python version."""
    print_section("1. Python Version")
    version = sys.version
    print(f"✓ Python version: {version}")
    return True


def check_ffmpeg():
    """Check if FFmpeg is installed."""
    print_section("2. FFmpeg Installation")
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            # Get version line
            version_line = result.stdout.split('\n')[0]
            print(f"✓ FFmpeg installed: {version_line}")
            return True
        else:
            print("✗ FFmpeg found but errored")
            return False
    except FileNotFoundError:
        print("✗ FFmpeg not found")
        print("  Install with:")
        print("    macOS: brew install ffmpeg")
        print("    Linux: sudo apt-get install ffmpeg")
        print("    Windows: choco install ffmpeg")
        return False


def check_ffprobe():
    """Check if FFprobe is installed."""
    print_section("3. FFprobe Installation")
    try:
        result = subprocess.run(
            ["ffprobe", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✓ FFprobe installed: {version_line}")
            return True
        else:
            print("✗ FFprobe found but errored")
            return False
    except FileNotFoundError:
        print("✗ FFprobe not found (usually comes with FFmpeg)")
        return False


def check_python_packages():
    """Check if required Python packages are installed."""
    print_section("4. Python Packages")
    
    required_packages = {
        "anthropic": "Anthropic API client",
        "cv2": "OpenCV (opencv-python)",
        "PIL": "Pillow",
        "dotenv": "python-dotenv",
        "colorama": "Colorama"
    }
    
    all_installed = True
    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"✓ {package}: {description}")
        except ImportError:
            print(f"✗ {package}: {description} - NOT INSTALLED")
            all_installed = False
    
    return all_installed


def check_api_key():
    """Check if API key is configured."""
    print_section("5. API Key Configuration")
    
    import os
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if api_key:
        masked_key = api_key[:7] + "*" * (len(api_key) - 14) + api_key[-7:]
        print(f"✓ API key found: {masked_key}")
        return True
    else:
        print("✗ ANTHROPIC_API_KEY environment variable not set")
        print("\n  Solution:")
        print("  1. Create .env file with: ANTHROPIC_API_KEY=your_key")
        print("  2. Or set environment variable:")
        print("     export ANTHROPIC_API_KEY=your_key  (Linux/macOS)")
        print("     $env:ANTHROPIC_API_KEY='your_key'  (Windows)")
        return False


def check_imports():
    """Check if main modules can be imported."""
    print_section("6. Module Imports")
    
    try:
        import analyzer
        print("✓ analyzer module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import analyzer: {e}")
        return False
    
    try:
        import utils
        print("✓ utils module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import utils: {e}")
        return False
    
    return True


def test_frame_extraction():
    """Test FFmpeg frame extraction."""
    print_section("7. Frame Extraction Test")
    
    # Create a small test video
    test_video = Path("test_video.mp4")
    
    # Check if we can create a test video
    print("Creating test video...")
    cmd = [
        "ffmpeg",
        "-f", "lavfi",
        "-i", "color=c=blue:s=320x240:d=5",
        "-f", "lavfi",
        "-i", "sine=f=1000:d=5",
        "-pix_fmt", "yuv420p",
        "-y",  # Overwrite
        str(test_video)
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=30
        )
        if result.returncode == 0:
            print(f"✓ Test video created: {test_video}")
            print(f"  Size: {test_video.stat().st_size / 1024:.1f} KB")
            
            # Try extracting a frame
            print("\nExtracting test frame...")
            frames_dir = Path("test_frames")
            frames_dir.mkdir(exist_ok=True)
            
            extract_cmd = [
                "ffmpeg",
                "-i", str(test_video),
                "-vf", "fps=1",
                "-q:v", "2",
                "-y",
                str(frames_dir / "frame_%04d.jpg")
            ]
            
            extract_result = subprocess.run(
                extract_cmd,
                capture_output=True,
                timeout=30
            )
            
            if extract_result.returncode == 0:
                frames = list(frames_dir.glob("frame_*.jpg"))
                print(f"✓ Frames extracted: {len(frames)} frames")
                
                # Cleanup
                for frame in frames:
                    frame.unlink()
                frames_dir.rmdir()
                test_video.unlink()
                
                return True
            else:
                print(f"✗ Frame extraction failed")
                return False
        else:
            print(f"✗ Failed to create test video")
            return False
    
    except subprocess.TimeoutExpired:
        print("✗ Test video creation timed out")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_anthropic_api():
    """Test Anthropic API connection (without using vision)."""
    print_section("8. Anthropic API Test")
    
    import os
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("✗ Skipping - API key not configured")
        return False
    
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        
        print("Testing API connection...")
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=100,
            messages=[
                {
                    "role": "user",
                    "content": "Say 'API working!' in 2 words."
                }
            ]
        )
        
        print(f"✓ API working: {response.content[0].text[:50]}")
        return True
    
    except Exception as e:
        print(f"✗ API test failed: {e}")
        return False


def main():
    """Run all checks."""
    print("\n" + "="*60)
    print("  Claude Vision Video Analyzer - Setup Verification")
    print("="*60)
    
    checks = [
        ("Python Version", check_python),
        ("FFmpeg", check_ffmpeg),
        ("FFprobe", check_ffprobe),
        ("Python Packages", check_python_packages),
        ("API Key", check_api_key),
        ("Module Imports", check_imports),
        ("Frame Extraction", test_frame_extraction),
        ("Anthropic API", test_anthropic_api),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ Error running {name}: {e}")
            results.append((name, False))
    
    # Summary
    print_section("Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"Checks passed: {passed}/{total}\n")
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")
    
    if passed == total:
        print("\n✓ All checks passed! You're ready to use Claude Vision Video Analyzer")
        print("\nRun your first analysis with:")
        print("  python main.py --video your_video.mp4\n")
        return 0
    else:
        print(f"\n✗ {total - passed} check(s) failed. Please fix and try again.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
