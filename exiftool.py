#!/usr/bin/env python3
"""
EXIF Metadata CLI Tool
A command-line tool to read and optionally remove image generation metadata from image files.
"""

import argparse
import glob
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    import exifread
except ImportError as e:
    print(f"Error: Required libraries not installed. Please run:")
    print("pip install Pillow ExifRead")
    sys.exit(1)


class ExifMetadataProcessor:
    """Process EXIF metadata for images"""
    
    # Common AI/generation related tags to look for
    AI_GENERATION_TAGS = [
        'Software',
        'ImageDescription', 
        'UserComment',
        'Artist',
        'Copyright',
        'ProcessingSoftware',
        'OriginalRawFileName',
        'DocumentName',
        # PNG-specific text chunks commonly used by AI tools
        'parameters',
        'prompt',
        'negative_prompt', 
        'workflow',
        'Comment',
        'Description',
        'Title',
        'Author',
        'Software',
        'Creation Time',
        'Source'
    ]
    
    # Keywords that might indicate AI generation
    AI_KEYWORDS = [
        'stable diffusion',
        'midjourney', 
        'dall-e',
        'dalle',
        'ai generated',
        'artificial intelligence',
        'neural network',
        'gan',
        'diffusion',
        'automatic1111',
        'invokeai',
        'comfyui',
        'novelai',
        'swarmui',
        'stableswarmui',
        'stable swarm ui'
    ]

    def __init__(self):
        self.supported_formats = {'.jpg', '.jpeg', '.tiff', '.tif', '.png'}
    
    def get_unique_filename(self, base_path: str) -> str:
        """Generate a unique filename by adding _1, _2, etc. if file exists"""
        if not os.path.exists(base_path):
            return base_path
        
        # Split the path into directory, filename, and extension
        directory = os.path.dirname(base_path)
        filename = os.path.basename(base_path)
        name, ext = os.path.splitext(filename)
        
        counter = 1
        while True:
            new_filename = f"{name}_{counter}{ext}"
            new_path = os.path.join(directory, new_filename)
            if not os.path.exists(new_path):
                return new_path
            counter += 1
    
    def is_json_format(self, text: str) -> bool:
        """Check if text is valid JSON format"""
        try:
            import json
            json.loads(text)
            return True
        except (json.JSONDecodeError, TypeError):
            return False
    
    def copy_to_clipboard(self, text: str) -> bool:
        """Copy text to clipboard using cross-platform method"""
        try:
            # Try Windows first
            import win32clipboard
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            return True
        except ImportError:
            try:
                # Try pyperclip as fallback
                import pyperclip
                pyperclip.copy(text)
                return True
            except ImportError:
                try:
                    # Try using subprocess for cross-platform support
                    import subprocess
                    if sys.platform.startswith('win'):
                        # Windows - use clip command
                        process = subprocess.Popen(['clip'], stdin=subprocess.PIPE, text=True)
                        process.communicate(input=text)
                        return process.returncode == 0
                    elif sys.platform.startswith('darwin'):
                        # macOS - use pbcopy
                        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE, text=True)
                        process.communicate(input=text)
                        return process.returncode == 0
                    elif sys.platform.startswith('linux'):
                        # Linux - try xclip or xsel
                        try:
                            process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE, text=True)
                            process.communicate(input=text)
                            return process.returncode == 0
                        except FileNotFoundError:
                            try:
                                process = subprocess.Popen(['xsel', '--clipboard', '--input'], stdin=subprocess.PIPE, text=True)
                                process.communicate(input=text)
                                return process.returncode == 0
                            except FileNotFoundError:
                                return False
                except Exception:
                    return False
        except Exception:
            return False
        
        return False
    
    def copy_ai_metadata_to_clipboard(self, ai_metadata: Dict[str, Any]) -> bool:
        """Copy AI generation metadata to clipboard in appropriate format"""
        if not ai_metadata:
            print("No AI metadata found to copy")
            return False
        
        try:
            # Check for ComfyUI workflow first
            comfyui_workflow = None
            
            for tag, value in ai_metadata.items():
                value_str = str(value)
                if ('workflow' in tag.lower() or 'comfy' in tag.lower()) and self.is_json_format(value_str):
                    try:
                        import json
                        parsed_json = json.loads(value_str)
                        # Check if it looks like a ComfyUI workflow
                        if isinstance(parsed_json, dict) and ('nodes' in parsed_json or any(isinstance(v, dict) and 'class_type' in v for v in parsed_json.values())):
                            comfyui_workflow = parsed_json
                            break
                    except:
                        continue
            
            if comfyui_workflow:
                # Copy ComfyUI workflow as properly formatted JSON
                import json
                workflow_json = json.dumps(comfyui_workflow, indent=2, ensure_ascii=False)
                if self.copy_to_clipboard(workflow_json):
                    print("✓ ComfyUI workflow copied to clipboard")
                    print("  Can be pasted directly into ComfyUI")
                    return True
                else:
                    print("✗ Failed to copy to clipboard")
                    return False
            
            # Check for other JSON content
            for tag, value in ai_metadata.items():
                value_str = str(value)
                if self.is_json_format(value_str):
                    try:
                        import json
                        parsed_json = json.loads(value_str)
                        formatted_json = json.dumps(parsed_json, indent=2, ensure_ascii=False)
                        if self.copy_to_clipboard(formatted_json):
                            print(f"✓ JSON metadata from '{tag}' copied to clipboard")
                            return True
                    except:
                        continue
            
            # If no JSON found, copy all metadata as formatted text
            text_content = []
            for tag, value in ai_metadata.items():
                text_content.append(f"{tag}: {value}")
            
            combined_text = "\n".join(text_content)
            if self.copy_to_clipboard(combined_text):
                print("✓ AI generation metadata copied to clipboard")
                return True
            else:
                print("✗ Failed to copy to clipboard")
                return False
                
        except Exception as e:
            print(f"✗ Error copying metadata to clipboard: {e}")
            return False
    
    def save_ai_metadata_to_file(self, image_filepath: str, ai_metadata: Dict[str, Any]) -> bool:
        """Save AI generation metadata to separate file"""
        if not ai_metadata:
            print(f"No AI metadata found in {image_filepath} to save")
            return False
        
        try:
            # Get base filename without extension
            base_name = os.path.splitext(image_filepath)[0]
            
            # Combine all AI metadata into a single structure
            combined_metadata = {}
            all_text = ""
            
            for tag, value in ai_metadata.items():
                combined_metadata[tag] = str(value)
                all_text += f"{tag}: {value}\n"
            
            # Check for ComfyUI workflow specifically
            comfyui_workflow = None
            is_comfyui_workflow = False
            
            # Look for ComfyUI workflow in metadata
            for tag, value in ai_metadata.items():
                value_str = str(value)
                if ('workflow' in tag.lower() or 'comfy' in tag.lower()) and self.is_json_format(value_str):
                    try:
                        import json
                        parsed_json = json.loads(value_str)
                        # Check if it looks like a ComfyUI workflow (has nodes structure)
                        if isinstance(parsed_json, dict) and ('nodes' in parsed_json or any(isinstance(v, dict) and 'class_type' in v for v in parsed_json.values())):
                            comfyui_workflow = parsed_json
                            is_comfyui_workflow = True
                            print(f"🎨 Detected ComfyUI workflow in {tag}")
                            break
                    except:
                        continue
            
            if is_comfyui_workflow and comfyui_workflow:
                # Save as ComfyUI workflow JSON
                json_filepath = f"{base_name}.json"
                json_filepath = self.get_unique_filename(json_filepath)
                
                import json
                with open(json_filepath, 'w', encoding='utf-8') as f:
                    json.dump(comfyui_workflow, f, indent=2, ensure_ascii=False)
                
                print(f"💾 Saved ComfyUI workflow: {json_filepath}")
                print(f"   ✓ Can be loaded directly in ComfyUI")
                
            else:
                # Check if any other metadata values contain JSON
                is_json_data = False
                json_content = None
                
                # Look for other JSON-like content
                for tag, value in ai_metadata.items():
                    if self.is_json_format(str(value)):
                        is_json_data = True
                        import json
                        json_content = {
                            "source_file": os.path.basename(image_filepath),
                            "metadata_tags": combined_metadata
                        }
                        break
                
                if is_json_data and json_content:
                    # Save as general JSON file
                    json_filepath = f"{base_name}.json"
                    json_filepath = self.get_unique_filename(json_filepath)
                    
                    import json
                    with open(json_filepath, 'w', encoding='utf-8') as f:
                        json.dump(json_content, f, indent=2, ensure_ascii=False)
                    
                    print(f"💾 Saved AI metadata as JSON: {json_filepath}")
                    
                else:
                    # Save as text file
                    txt_filepath = f"{base_name}.txt"
                    txt_filepath = self.get_unique_filename(txt_filepath)
                    
                    with open(txt_filepath, 'w', encoding='utf-8') as f:
                        f.write(f"AI Generation Metadata for: {os.path.basename(image_filepath)}\n")
                        f.write("=" * 50 + "\n\n")
                        f.write(all_text)
                    
                    print(f"💾 Saved AI metadata as text: {txt_filepath}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error saving metadata for {image_filepath}: {e}")
            return False
    
    def is_supported_format(self, filepath: str) -> bool:
        """Check if file format is supported"""
        return Path(filepath).suffix.lower() in self.supported_formats
    
    def read_exif_data(self, filepath: str) -> Dict[str, Any]:
        """Read EXIF data and PNG metadata from image file"""
        exif_data = {}
        
        try:
            with Image.open(filepath) as img:
                # Read standard EXIF data (JPEG/TIFF)
                if hasattr(img, '_getexif') and img._getexif() is not None:
                    for tag_id, value in img._getexif().items():
                        tag_name = TAGS.get(tag_id, tag_id)
                        exif_data[tag_name] = value
                
                # Read PNG text chunks (PNG metadata)
                if hasattr(img, 'text') and img.text:
                    for key, value in img.text.items():
                        exif_data[f"PNG.{key}"] = value
            
            # Use exifread for more detailed EXIF data (JPEG/TIFF only)
            if not filepath.lower().endswith('.png'):
                with open(filepath, 'rb') as f:
                    detailed_tags = exifread.process_file(f, details=True)
                    for tag, value in detailed_tags.items():
                        if not tag.startswith('JPEGThumbnail'):
                            exif_data[tag] = str(value)
                        
        except Exception as e:
            print(f"Warning: Could not read metadata from {filepath}: {e}")
            
        return exif_data
    
    def find_ai_generation_metadata(self, exif_data: Dict[str, Any]) -> Dict[str, Any]:
        """Find potential AI generation metadata"""
        ai_metadata = {}
        
        for tag, value in exif_data.items():
            # Check if tag is in our list of AI-related tags
            tag_name = tag.split('.')[-1] if '.' in tag else tag
            if tag_name in self.AI_GENERATION_TAGS:
                # Check if value contains AI-related keywords
                value_str = str(value).lower()
                if any(keyword in value_str for keyword in self.AI_KEYWORDS):
                    ai_metadata[tag] = value
                elif tag_name in ['Software', 'ProcessingSoftware']:
                    # Include all software tags as they might indicate generation tools
                    ai_metadata[tag] = value
                elif len(str(value)) > 50:  # Long descriptions might be prompts
                    ai_metadata[tag] = value
            
            # Special handling for JSON-like metadata (SwarmUI format)
            value_str = str(value)
            if (value_str.strip().startswith('{') and value_str.strip().endswith('}')) or \
               ('prompt' in value_str.lower() and ('cfg' in value_str.lower() or 'steps' in value_str.lower())):
                ai_metadata[tag] = value
        
        return ai_metadata
    
    def display_metadata(self, filepath: str, exif_data: Dict[str, Any], ai_metadata: Dict[str, Any]):
        """Display metadata information"""
        print(f"\n{'='*60}")
        print(f"File: {filepath}")
        print(f"{'='*60}")
        
        if not exif_data:
            print("No EXIF data found.")
            return
            
        if ai_metadata:
            print("\n🤖 POTENTIAL AI GENERATION METADATA:")
            print("-" * 40)
            for tag, value in ai_metadata.items():
                print(f"{tag}: {value}")
        
        print(f"\n📊 ALL EXIF DATA ({len(exif_data)} tags):")
        print("-" * 40)
        for tag, value in sorted(exif_data.items()):
            # Truncate very long values
            value_str = str(value)
            if len(value_str) > 100:
                value_str = value_str[:97] + "..."
            print(f"{tag}: {value_str}")
    
    def remove_ai_metadata(self, filepath: str) -> bool:
        """Remove AI generation metadata from image"""
        try:
            # Create backup filename
            backup_path = f"{filepath}.backup"
            
            # Copy original file as backup
            import shutil
            shutil.copy2(filepath, backup_path)
            
            # Open image and remove metadata
            with Image.open(filepath) as img:
                if filepath.lower().endswith('.png'):
                    # For PNG files, remove text chunks but preserve other PNG metadata
                    img_clean = Image.new(img.mode, img.size)
                    img_clean.putdata(list(img.getdata()))
                    
                    # Preserve essential PNG info but remove text chunks
                    if hasattr(img, 'info'):
                        clean_info = {}
                        # Keep essential PNG chunks, exclude text-based ones
                        essential_keys = ['transparency', 'gamma', 'dpi', 'aspect']
                        for key, value in img.info.items():
                            if key in essential_keys:
                                clean_info[key] = value
                        img_clean.info = clean_info
                    
                    img_clean.save(filepath, 'PNG', optimize=True)
                else:
                    # For JPEG/TIFF files, remove EXIF data
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    
                    # Save without EXIF data
                    img.save(filepath, optimize=True, exif=b'')
            
            print(f"✓ Removed metadata from {filepath}")
            print(f"  Backup saved as: {backup_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error removing metadata from {filepath}: {e}")
            return False


def expand_file_patterns(patterns: List[str]) -> List[str]:
    """Expand wildcard patterns to actual file paths"""
    files = []
    for pattern in patterns:
        if '*' in pattern or '?' in pattern:
            # Handle wildcards
            matches = glob.glob(pattern)
            files.extend(matches)
        else:
            # Handle single file
            if os.path.exists(pattern):
                files.append(pattern)
            else:
                print(f"Warning: File not found: {pattern}")
    
    return sorted(list(set(files)))  # Remove duplicates and sort


def main():
    parser = argparse.ArgumentParser(
        description="Read and optionally remove AI generation metadata from image files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s image.jpg                    # Display metadata for single image
  %(prog)s *.jpg                       # Display metadata for all JPG files
  %(prog)s -r generated_*.png          # Remove metadata from matching PNG files
  %(prog)s -s swarm_output.png         # Save AI metadata to separate file
  %(prog)s -c image.png                # Copy AI metadata to clipboard (single file only)
  %(prog)s -s *.jpg --verbose          # Save metadata from all JPG files
  %(prog)s folder/*.tiff --verbose     # Process all TIFF files with verbose output
        """
    )
    
    parser.add_argument(
        'files',
        nargs='+',
        help='Image file(s) or wildcard patterns to process'
    )
    
    parser.add_argument(
        '-r', '--remove',
        action='store_true',
        help='Remove AI generation metadata from images'
    )
    
    parser.add_argument(
        '-s', '--save-metadata',
        action='store_true',
        help='Save AI generation metadata to separate files (.json or .txt)'
    )
    
    parser.add_argument(
        '-c', '--copy',
        action='store_true',
        help='Copy AI generation metadata to clipboard (single file only)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show verbose output'
    )
    
    parser.add_argument(
        '--ai-only',
        action='store_true',
        help='Only display potential AI generation metadata'
    )
    
    args = parser.parse_args()
    
    # Expand file patterns
    file_paths = expand_file_patterns(args.files)
    
    if not file_paths:
        print("No files found matching the specified patterns.")
        return 1
    
    # Check if copy option is used with multiple files
    if args.copy and len(file_paths) > 1:
        print("Error: --copy option can only be used with a single file.")
        return 1
    
    processor = ExifMetadataProcessor()
    
    # Filter supported files
    supported_files = [f for f in file_paths if processor.is_supported_format(f)]
    unsupported_files = [f for f in file_paths if not processor.is_supported_format(f)]
    
    if unsupported_files:
        print(f"Warning: Skipping {len(unsupported_files)} unsupported files:")
        for f in unsupported_files:
            print(f"  {f}")
    
    if not supported_files:
        print("No supported image files found.")
        return 1
    
    print(f"Processing {len(supported_files)} image file(s)...")
    
    for filepath in supported_files:
        try:
            # Read EXIF data
            exif_data = processor.read_exif_data(filepath)
            ai_metadata = processor.find_ai_generation_metadata(exif_data)
            
            if args.remove:
                # Remove metadata
                success = processor.remove_ai_metadata(filepath)
                if args.verbose and success:
                    print(f"Removed {len(exif_data)} EXIF tags from {filepath}")
            elif args.copy:
                # Copy metadata to clipboard
                processor.copy_ai_metadata_to_clipboard(ai_metadata)
            elif args.save_metadata:
                # Save metadata to file
                processor.save_ai_metadata_to_file(filepath, ai_metadata)
            else:
                # Display metadata
                if args.ai_only:
                    if ai_metadata:
                        print(f"\n🤖 AI Generation Metadata in {filepath}:")
                        for tag, value in ai_metadata.items():
                            print(f"  {tag}: {value}")
                    elif args.verbose:
                        print(f"\n{filepath}: No AI generation metadata detected")
                else:
                    processor.display_metadata(filepath, exif_data, ai_metadata)
                    
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())