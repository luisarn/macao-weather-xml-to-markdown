# Weather Markdown Generator

A Python tool to convert Macau weather XML data to markdown with customizable templates and multi-language support.

## Features

- 📡 Fetches real-time weather data from Macau Meteorological and Geophysical Bureau
- 🌐 Multi-language support (Chinese, Portuguese, English)
- 📝 Converts XML to beautifully formatted markdown
- 🎨 Multiple template options for different output styles
- 🔧 Easy to customize and extend
- 🐍 Built with modern Python and UV

## Installation

### Using UV (Recommended)

```bash
# Clone the repository
git clone <your-repo>
cd weather-markdown

# Install dependencies
uv sync

# Run directly
uv run weather-markdown
```

## Basic Usage

```bash
# Output Chinese markdown to console (default)
uv run weather-markdown

# Output Portuguese weather data
uv run weather-markdown --language pt

# Output English weather data
uv run weather-markdown --language en

# Save to file
uv run weather-markdown --language en > weather_report.md
```

### Using Different Templates and Languages

```bash
# Use detailed template with Portuguese
uv run weather-markdown --language pt --template detailed_pt.md

# Use minimal template with English
uv run weather-markdown --language en --template minimal_en.md

# Use specific URL
uv run weather-markdown --url https://xml.smg.gov.mo/p_forecast.xml

# List available templates
uv run weather-markdown --list-templates
```

### Command Line Options

```bash
uv run weather-markdown --help

Options:
  -h, --help            show help message and exit
  -t TEMPLATE, --template TEMPLATE
                        Template file to use (from templates directory)
  -l, --list-templates  List available templates
  -u URL, --url URL     URL to fetch XML data from
  -lang {zh,pt,en}, --language {zh,pt,en}
                        Language to use (zh: Chinese, pt: Portuguese, en: English)
```

## Data Sources

Chinese: https://xml.smg.gov.mo/c_forecast.xml

Portuguese: https://xml.smg.gov.mo/p_forecast.xml

English: https://xml.smg.gov.mo/e_forecast.xml

## Project Structure

weather-markdown/
├── pyproject.toml # Project configuration and dependencies
├── README.md # This file
├── weather_markdown.py # Main application code
└── templates/ # Markdown templates
├── default_template.md # Chinese default template
├── detailed_template.md # Chinese detailed template
├── minimal_template.md # Chinese minimal template
├── default_pt.md # Portuguese default template
├── detailed_pt.md # Portuguese detailed template  
 ├── minimal_pt.md # Portuguese minimal template
├── default_en.md # English default template
├── detailed_en.md # English detailed template
└── minimal_en.md # English minimal template

## Templates

Templates are located in the templates/ directory and use the following placeholders:

{today_situation} - Today's weather situation

{author} - Publishing authority (SMG)

{pubdate} - Publication date and time

{language} - System language

{forecasts} - Generated forecast sections

{current_time} - Current generation time

{date} - Forecast date (in forecast item)

{tide} - Tide information (in forecast item)

{description} - Weather description (in forecast item)

## Language-specific Defaults

If you don't specify a template, the system will automatically use:

- default_template.md for Chinese (--language zh)
- default_pt.md for Portuguese (--language pt)
- default_en.md for English (--language en)

## Creating Custom Templates

Create a new .md file in the templates/ directory

Include <!-- FORECAST_ITEM --> to separate main template from forecast item template

Use the placeholders above to position data

Run with: uv run weather-markdown --template your_template.md --language xx

## Examples

### Basic Multi-language Usage

```bash
# Chinese (default)
uv run weather-markdown

# Portuguese
uv run weather-markdown --language pt

# English with detailed template
uv run weather-markdown --language en --template detailed_en.md

### Advanced Usage
# Portuguese minimal template output to file
uv run weather-markdown --language pt --template minimal_pt.md > previsao.md

# Use specific URL with custom template
uv run weather-markdown --url https://xml.smg.gov.mo/e_forecast.xml --template minimal_en.md

# Chain with other commands
uv run weather-markdown --language en | grep "temperature"
```

## Development

### Setting up Development Environment

# Install with development dependencies

uv sync --dev

# Run tests

uv run pytest

# Format code

uv run black weather_markdown.py
uv run isort weather_markdown.py

# Lint code

uv run flake8 weather_markdown.py

# Type checking

uv run mypy weather_markdown.py

## License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request
