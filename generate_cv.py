#!/usr/bin/env python3
"""
Resume Generator - Generate HTML resumes from YAML data and templates
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, Template
from pypdf import PdfReader, PdfWriter


def load_yaml(yaml_path: Path) -> dict:
    """Load and parse YAML data file."""
    try:
        with open(yaml_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: YAML file not found: {yaml_path}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}", file=sys.stderr)
        sys.exit(1)


def render_template(template_path: Path, data: dict) -> str:
    """Render the HTML template with provided data."""
    try:
        if template_path.is_file():
            # Load template from file
            env = Environment(loader=FileSystemLoader(template_path.parent))
            template = env.get_template(template_path.name)
        else:
            print(f"Error: Template file not found: {template_path}", file=sys.stderr)
            sys.exit(1)
        
        return template.render(**data)
    except Exception as e:
        print(f"Error rendering template: {e}", file=sys.stderr)
        sys.exit(1)


def save_html(content: str, output_path: Path):
    """Save rendered HTML to file."""
    try:
        with open(output_path, 'w') as f:
            f.write(content)
        print(f"HTML saved to: {output_path}")
    except IOError as e:
        print(f"Error saving HTML: {e}", file=sys.stderr)
        sys.exit(1)


def add_pdf_metadata(pdf_path: Path, data: dict):
    """Add metadata to PDF file."""
    try:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        # Copy all pages
        for page in reader.pages:
            writer.add_page(page)

        # Extract metadata from YAML data
        name = data.get('name', 'Resume')
        title = data.get('title', 'Resume')
        meta = data.get('meta', {})
        description = meta.get('description', f"{name} - {title}")
        keywords = meta.get('keywords', '')

        # Add metadata
        writer.add_metadata({
            '/Title': f"{name} - {title}",
            '/Author': name,
            '/Subject': description,
            '/Keywords': keywords,
            '/Creator': 'CV Generator (Chromium + pypdf)',
        })

        # Write to temporary file first, then replace original
        temp_pdf = pdf_path.with_suffix('.tmp.pdf')
        with open(temp_pdf, 'wb') as f:
            writer.write(f)

        # Replace original with metadata-enhanced version
        temp_pdf.replace(pdf_path)

    except Exception as e:
        print(f"Warning: Could not add PDF metadata: {e}", file=sys.stderr)


def convert_to_pdf(html_path: Path, pdf_path: Path, data: dict):
    """Convert HTML to PDF using Chromium and add metadata."""
    try:
        # Try common chromium binary names
        chromium_bins = ['chromium', 'chromium-browser', 'google-chrome', 'chrome']
        chromium_cmd = None

        for bin_name in chromium_bins:
            if subprocess.run(['which', bin_name], capture_output=True).returncode == 0:
                chromium_cmd = bin_name
                break

        if not chromium_cmd:
            print("Warning: Chromium/Chrome not found. Skipping PDF conversion.", file=sys.stderr)
            print("Install chromium to enable PDF export.", file=sys.stderr)
            return

        cmd = [
            chromium_cmd,
            '--headless',
            '--disable-gpu',
            '--no-sandbox',
            '--no-pdf-header-footer',
            '--print-to-pdf-no-header',
            '--run-all-compositor-stages-before-draw',
            f'--print-to-pdf={pdf_path.absolute()}',
            html_path.absolute().as_uri()
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"PDF saved to: {pdf_path}")
            # Add metadata to the generated PDF
            add_pdf_metadata(pdf_path, data)
        else:
            print(f"Error converting to PDF: {result.stderr}", file=sys.stderr)

    except Exception as e:
        print(f"Error during PDF conversion: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description='Generate HTML resumes from YAML data and templates',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -t template.html -d resume.yaml -o output.html
  %(prog)s -t template.html -d resume.yaml -o output.html --pdf output.pdf
        """
    )
    
    parser.add_argument(
        '-t', '--template',
        type=Path,
        required=True,
        help='Path to HTML template file'
    )
    
    parser.add_argument(
        '-d', '--data',
        type=Path,
        required=True,
        help='Path to YAML data file'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        required=False,
        help='Path to output HTML file (default: temp folder)'
    )
    
    parser.add_argument(
        '--pdf',
        nargs='?',
        const='default',
        type=str,
        help='Optional: Generate PDF (requires Chromium). Optionally specify output path (default: ./export/resume.pdf)'
    )
    
    args = parser.parse_args()

    # Load YAML data
    data = load_yaml(args.data)

    # Add resources path to template data
    resources_path = (args.template.parent / 'resources').absolute().as_uri()
    data['resources_path'] = resources_path

    # Render template
    html_content = render_template(args.template, data)

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        # Create temp directory and generate output filename using YAML name
        temp_dir = Path(tempfile.gettempdir()) / 'cv_generation'
        temp_dir.mkdir(exist_ok=True)
        html_filename = args.data.stem + '.html'
        output_path = temp_dir / html_filename

    # Save HTML
    save_html(html_content, output_path)

    # Convert to PDF if requested
    if args.pdf:
        if args.pdf == 'default':
            # Use default export folder with YAML name
            export_dir = Path('./export')
            export_dir.mkdir(exist_ok=True)
            pdf_filename = args.data.stem + '.pdf'
            pdf_path = export_dir / pdf_filename
        else:
            pdf_path = Path(args.pdf)
        convert_to_pdf(output_path, pdf_path, data)


if __name__ == '__main__':
    main()
