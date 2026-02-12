#!/usr/bin/env python3
import re
import subprocess
from pathlib import Path
import base64
import requests

def convert_mermaid_to_png(mermaid_code, output_path):
    """Convert mermaid diagram to PNG using Mermaid API"""
    try:
        url = "https://mermaid.ink/img/"
        encoded = base64.b64encode(mermaid_code.encode()).decode()
        img_url = url + encoded
        
        response = requests.get(img_url, timeout=10)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"Error: {e}")
    return False

def generate_pdf():
    """Generate PDF with Mermaid diagrams converted to PNG images"""
    work_dir = Path("/root/Holberton/holbertonschool-hbnb/part1")
    md_file = work_dir / "TECHNICAL_DOCUMENTATION.md"
    
    # Read original markdown
    with open(md_file, 'r') as f:
        content = f.read()
    
    # Create images directory
    images_dir = work_dir / "mermaid_diagrams"
    images_dir.mkdir(exist_ok=True)
    
    diagram_counter = 0
    
    def replace_mermaid(match):
        nonlocal diagram_counter
        diagram_counter += 1
        mermaid_code = match.group(1)
        png_path = images_dir / f"diagram_{diagram_counter}.png"
        
        print(f"Converting diagram {diagram_counter}...", end=" ")
        if convert_mermaid_to_png(mermaid_code, png_path):
            print("✓")
            rel_path = f"mermaid_diagrams/diagram_{diagram_counter}.png"
            return f"![Mermaid Diagram {diagram_counter}]({rel_path})"
        else:
            print("✗")
            return match.group(0)
    
    # Replace all mermaid blocks with image references
    pattern = r'```mermaid\n(.*?)\n```'
    modified_content = re.sub(pattern, replace_mermaid, content, flags=re.DOTALL)
    
    # Write temporary markdown with image references
    temp_md = work_dir / "TECHNICAL_DOCUMENTATION_WITH_IMAGES.md"
    with open(temp_md, 'w') as f:
        f.write(modified_content)
    
    # Generate PDF
    output_pdf = work_dir / "TECHNICAL_DOCUMENTATION.pdf"
    print(f"\nGenerating PDF: {output_pdf}")
    
    cmd = [
        'pandoc',
        str(temp_md),
        '-o', str(output_pdf),
        '--from=markdown',
        '--to=pdf',
        '-V', 'geometry:margin=1in',
        '--toc'
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✓ PDF generated successfully!")
        print(f"  File size: {output_pdf.stat().st_size / 1024:.1f} KB")
        
        # Cleanup
        temp_md.unlink()
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e.stderr}")
        return False

if __name__ == "__main__":
    generate_pdf()
