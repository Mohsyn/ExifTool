# ExifTool by Mohsyn

A powerful command-line tool for reading, extracting, and removing AI generation metadata from image files. Specifically designed to handle metadata from AI image generation tools like Stable Diffusion, ComfyUI, SwarmUI, Midjourney, and more.

## 🚀 Features

### Core Functionality
- **Read EXIF/Metadata**: Extract and display comprehensive metadata from images
- **AI Metadata Detection**: Automatically identify and highlight AI generation metadata
- **Metadata Removal**: Strip AI generation metadata while preserving image quality
- **Batch Processing**: Handle multiple files with wildcard patterns
- **Cross-Platform**: Works on Windows, macOS, and Linux

### AI Tool Support
- **ComfyUI**: Detects and extracts workflow JSON data
- **Stable Diffusion**: Identifies prompts, parameters, and generation settings
- **SwarmUI/StableSwarmUI**: Handles JSON-formatted metadata
- **Midjourney, DALL-E, NovelAI**: Recognizes generation signatures
- **Automatic1111, InvokeAI**: Extracts generation parameters

### Export Options
- **Clipboard Copy**: Copy metadata directly to clipboard (ComfyUI workflows can be pasted directly)
- **File Export**: Save metadata as JSON or TXT files
- **Workflow Preservation**: ComfyUI workflows saved as importable JSON files

### Windows Integration
- **Context Menu**: Right-click integration for Windows Explorer
- **Easy Installation**: Automated installer with dependency checking
- **Administrator Support**: Proper permission handling for system integration

## 📋 Requirements

### Python Dependencies
- Python 3.6+ 
- PIL (Pillow) - Image processing
- ExifRead - EXIF data extraction

### Optional Dependencies (for clipboard functionality)
- pyperclip (cross-platform)
- win32clipboard (Windows)

## 🔧 Installation

### Quick Install (Windows)

1. **Download** all files to a folder
2. **Run as Administrator**: `install_batch.bat`
3. **Follow prompts** to install Python dependencies
4. **Right-click any image** to access ExifTool options

### Manual Installation

1. **Clone or download** this repository
2. **Install Python dependencies**:
   ```bash
   pip install Pillow ExifRead
   ```
3. **Optional clipboard support**:
   ```bash
   pip install pyperclip
   ```

## 🎯 Usage

### Command Line Interface

#### Basic Usage
```bash
# View metadata for a single image
python exiftool.py image.jpg

# Process multiple images with wildcards
python exiftool.py *.png

# Process all images in a folder
python exiftool.py folder/*.jpg
```

#### Advanced Options
```bash
# Show only AI generation metadata
python exiftool.py --ai-only generated_image.png

# Remove metadata from images (creates backups)
python exiftool.py --remove *.jpg

# Save metadata to separate files
python exiftool.py --save-metadata ai_artwork.png

# Copy metadata to clipboard (single file only)
python exiftool.py --copy workflow_image.png

# Verbose output
python exiftool.py --verbose *.tiff
```

### Windows Context Menu

After installation, right-click any supported image file and select:
- **ExifTool → View MetaData**: Display metadata in command window
- **ExifTool → Extract MetaData**: Save metadata to separate files  
- **ExifTool → Copy MetaData**: Copy metadata to clipboard

### Supported File Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- TIFF (.tiff, .tif)

## 📊 Output Examples

### AI Metadata Detection
```
🤖 POTENTIAL AI GENERATION METADATA:
----------------------------------------
Software: ComfyUI
PNG.parameters: {"prompt": "beautiful landscape", "steps": 20, "cfg": 7.5}
PNG.workflow: {"nodes": [...], "links": [...]}
```

### ComfyUI Workflow Export
```
🎨 Detected ComfyUI workflow in PNG.workflow
💾 Saved ComfyUI workflow: image_workflow.json
   ✓ Can be loaded directly in ComfyUI
✓ ComfyUI workflow copied to clipboard
  Can be pasted directly into ComfyUI
```

### Metadata Removal
```
✓ Removed metadata from generated_image.jpg
  Backup saved as: generated_image.jpg.backup
```

## 🛠️ Command Reference

### Arguments
- `files`: Image file(s) or wildcard patterns to process
- `-r, --remove`: Remove AI generation metadata from images
- `-s, --save-metadata`: Save AI generation metadata to separate files
- `-c, --copy`: Copy AI generation metadata to clipboard (single file only)
- `-v, --verbose`: Show verbose output
- `--ai-only`: Only display potential AI generation metadata


## 🔍 AI Detection Features

### Detected AI Keywords
- stable diffusion, midjourney, dall-e, dalle
- ai generated, artificial intelligence
- neural network, gan, diffusion
- automatic1111, invokeai, comfyui
- novelai, swarmui, stableswarmui

### Monitored Metadata Tags
- Software, ImageDescription, UserComment
- Artist, Copyright, ProcessingSoftware
- PNG text chunks (parameters, prompt, workflow)
- JSON-formatted generation data

### Special Handling
- **ComfyUI Workflows**: Automatically detected and exported as importable JSON
- **JSON Metadata**: Pretty-formatted when copied to clipboard
- **Long Descriptions**: Automatically flagged as potential prompts

## 🔧 Advanced Usage

### Batch Processing
```bash
# Save metadata from all AI-generated images
python exiftool.py --save-metadata --ai-only AI_outputs/*.png
```

### Integration with AI Tools
```bash
# Extract ComfyUI workflow for reuse
python exiftool.py --copy comfyui_image.png
# Then Ctrl+V in ComfyUI to load workflow

# Save Stable Diffusion parameters
python exiftool.py --save-metadata sd_output.jpg
# Creates sd_output.txt with generation parameters
```

## 🗑️ Uninstallation (Windows)

Run as Administrator: `uninstall_batch.bat`

This removes all context menu entries from Windows Explorer.

## 🐛 Troubleshooting

### Common Issues

**"Required libraries not installed"**
```bash
pip install Pillow ExifRead
```

**"Failed to copy to clipboard"**
- Windows: Install `pip install pywin32`
- Linux: Install `xclip` or `xsel`
- macOS: Should work by default

**Made with ❤️ by Mohsyn**

For support or questions, please open an issue on GitHub.
