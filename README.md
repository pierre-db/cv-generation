# CV Generator

A Python CLI tool to generate professional HTML resumes from YAML data and Jinja2 templates, with automatic PDF export via Chromium.

## Features

- **YAML-based data** - Separate your content from presentation
- **Jinja2 templates** - Flexible, customizable templates
- **PDF export** - Automatic PDF generation via headless Chromium

## Quick Start

### Installation

```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

### Generate Your CV

```bash
# Generate HTML in temp folder, PDF in ./export/
python generate_cv.py -t templates/template.html -d yaml/default.yaml --pdf

# Specify custom output paths
python generate_cv.py -t templates/example.html -d yaml/example.yaml -o my_cv.html --pdf my_cv.pdf
```

## Project Structure

```
cv_generation/
├── generate_cv.py          # Main CLI tool
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates
│   ├── template.html       # Template with external resources
│   ├── example.html        # Minimalist self-contained template
│   ├── cv_template.html    # Alternative template
│   └── resources/          # CSS, fonts, images for template.html
│       ├── styles.css
│       └── img/
└── yaml/                   # CV data files
    └── example.yaml        # Example CV with fictional data
```

## Usage

### Command Line Arguments

```
python generate_cv.py -t TEMPLATE -d DATA [-o OUTPUT] [--pdf [PDF_PATH]]

Required:
  -t, --template TEMPLATE  Path to HTML template file
  -d, --data DATA          Path to YAML data file

Optional:
  -o, --output OUTPUT      Path to output HTML file (default: temp folder)
  --pdf [PDF_PATH]         Generate PDF. Optionally specify path (default: ./export/<yaml-name>.pdf)
```

## YAML Data Structure

Your YAML file should include:

```yaml
name: Your Name
firstname: Your
lastname: Name
title: Your Job Title
location: City, State
phone: (555)-123-4567
email: your.email@example.com
linkedin: https://www.linkedin.com/in/yourprofile/
github: https://github.com/yourusername
website: https://yourwebsite.com  # Optional

description: |
  Brief professional summary highlighting your experience and expertise.

skills:
  technical:
    - Python
    - JavaScript
  cloud:
    - AWS
    - Docker
  # Add as many skill categories as needed

languages:
  - name: English
    level: Native
  - name: Spanish
    level: B2

interests:
  - name: Coding
  - name: Photography
  - name: Traveling
    details:
      - Europe (10 countries)
      - Asia (5 countries)

experience:
  - title: Job Title
    company: Company Name
    company_url: https://company.com
    location: City, State
    period: Jan 2020 - Present
    description: Brief role description
    highlights:
      - Achievement or responsibility
      - Another key accomplishment

education:
  - degree: Degree Name
    school: University Name
    school_url: https://university.edu
    location: City, State
    period: Sep 2015 - Jun 2019
    description: Program description
    details:
      - "GPA: 3.8/4.0"
      - "Relevant coursework"

meta:
  description: SEO/ATS-friendly description
  keywords: Keyword1, Keyword2, Keyword3
```

## Templates

### template.html
- Professional design with external CSS
- Custom fonts (Montserrat)
- Icons for contact info
- Requires `resources/` folder

### example.html
- Minimalist, self-contained
- Embedded CSS
- No external dependencies
- System fonts only
- Great for sharing/emailing

## PDF Generation

The tool uses Chromium's headless mode for PDF generation:

- **Requirements**: Chromium, Chrome, or Google Chrome installed
- **Output**: Zero-margin PDFs (Letter size)
- **Quality**: Pixel-perfect rendering with proper fonts and CSS

The script automatically detects available browsers: `chromium`, `chromium-browser`, `google-chrome`, or `chrome`.

## Tips & Best Practices

1. **Multiple CVs**: Create different YAML files for different job applications
   ```bash
   cp yaml/default.yaml yaml/software_engineer.yaml
   cp yaml/default.yaml yaml/data_scientist.yaml
   ```

2. **Version Control**: Use Git to track changes to your CV data
   ```bash
   git add yaml/default.yaml
   git commit -m "Update experience section"
   ```

3. **Template Customization**:
   - Edit CSS in templates for different styles
   - Use Jinja2 conditionals to show/hide sections
   - Loop through skill categories dynamically

4. **ATS Optimization**:
   - YAML structure includes ATS-friendly metadata
   - Both templates generate semantic HTML
   - PDF export maintains text selectability

## Development

### Dependencies

- Python 3.8+
- PyYAML - YAML parsing
- Jinja2 - Template rendering
- Chromium/Chrome - PDF generation (optional)

### Adding New Templates

1. Create new HTML file in `templates/`
2. Use Jinja2 syntax for dynamic content
3. Reference `{{ resources_path }}` for external resources (or embed CSS)
4. Test with example data: `python generate_cv.py -t templates/your_template.html -d yaml/example.yaml --pdf`

## License

Feel free to use and modify for your personal CV needs!

## Contributing

Contributions welcome! Feel free to:
- Add new templates
- Improve existing templates
- Enhance the CLI tool
- Fix bugs or improve documentation
