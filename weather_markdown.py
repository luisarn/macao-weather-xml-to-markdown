#!/usr/bin/env python3
"""
Weather Markdown Generator
Convert Macau weather XML data to markdown with customizable templates and multi-language support
"""

import xml.etree.ElementTree as ET
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum

try:
    import requests
except ImportError:
    print("Error: requests library is required. Install with: uv add requests", file=sys.stderr)
    sys.exit(1)


class Language(Enum):
    CHINESE = "zh"
    PORTUGUESE = "pt" 
    ENGLISH = "en"


# Template directory
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")

# Data source URLs
DATA_SOURCES = {
    Language.CHINESE: "https://xml.smg.gov.mo/c_forecast.xml",
    Language.PORTUGUESE: "https://xml.smg.gov.mo/p_forecast.xml",
    Language.ENGLISH: "https://xml.smg.gov.mo/e_forecast.xml"
}

# Language names for display
LANGUAGE_NAMES = {
    Language.CHINESE: "Chinese (中文)",
    Language.PORTUGUESE: "Portuguese (Português)", 
    Language.ENGLISH: "English"
}

# Default template mappings for each language
DEFAULT_TEMPLATES = {
    Language.CHINESE: "default_template.md",
    Language.PORTUGUESE: "default_pt.md", 
    Language.ENGLISH: "default_en.md"
}


def load_template(template_file: str) -> Dict[str, str]:
    """Load markdown template from file"""
    template_path = os.path.join(TEMPLATES_DIR, template_file)
    
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Split main template from forecast item template
        if "<!-- FORECAST_ITEM -->" in content:
            main_template, forecast_item = content.split("<!-- FORECAST_ITEM -->")
            return {
                "main": main_template.strip(),
                "forecast_item": forecast_item.strip(),
            }
        else:
            raise ValueError("Template must contain <!-- FORECAST_ITEM --> separator")

    except FileNotFoundError:
        print(
            f"Template file '{template_path}' not found.",
            file=sys.stderr,
        )
        raise
    except Exception as e:
        print(f"Error loading template: {e}", file=sys.stderr)
        raise


def create_default_template(language: Language) -> Dict[str, str]:
    """Create a default template for a specific language"""
    if language == Language.CHINESE:
        return {
            "main": """
# 澳門天氣預報 Weather Forecast Macau

## 今日天氣情況 Today's Situation
{today_situation}

## 系統資訊 System Information
- **發布機構**: {author}
- **發布時間**: {pubdate}
- **語言**: {language}

## 天氣預報 Weather Forecast

{forecasts}

---
*最後更新 Last Updated: {current_time}*
""",
            "forecast_item": """
### {date}
**潮汐 Astronomical Tide**: {tide}

{description}

---
""",
        }
    elif language == Language.PORTUGUESE:
        return {
            "main": """
# Previsão Meteorológica de Macau

## Situação Meteorológica de Hoje
{today_situation}

## Informação do Sistema
- **Entidade**: {author}
- **Data de Publicação**: {pubdate}
- **Idioma**: {language}

## Previsão Meteorológica

{forecasts}

---
*Última atualização: {current_time}*
""",
            "forecast_item": """
### {date}
**Maré Astronómica**: {tide}

{description}

---
""",
        }
    else:  # ENGLISH
        return {
            "main": """
# Macau Weather Forecast

## Today's Weather Situation
{today_situation}

## System Information
- **Issuing Authority**: {author}
- **Publication Time**: {pubdate}
- **Language**: {language}

## Weather Forecast

{forecasts}

---
*Last Updated: {current_time}*
""",
            "forecast_item": """
### {date}
**Astronomical Tide**: {tide}

{description}

---
""",
        }


def parse_weather_xml(xml_content: str) -> Dict[str, Any]:
    """Parse the XML content and extract weather data"""
    root = ET.fromstring(xml_content)

    # Extract system information
    system_info = {
        "author": root.find(".//SysAuthor").text,
        "pubdate": root.find(".//SysPubdate").text,
        "language": root.find(".//SysLanguage").text,
    }

    # Extract today's situation
    today_situation_element = root.find(".//TodaySituation")
    today_situation = today_situation_element.text if today_situation_element is not None else "No data available"

    # Extract weather forecasts
    forecasts = []
    for forecast in root.findall(".//WeatherForecast"):
        date_element = forecast.find("ValidFor")
        desc_element = forecast.find("WeatherDescription")
        tide_element = forecast.find("AstronomicalTide")
        
        forecasts.append(
            {
                "date": date_element.text if date_element is not None else "Unknown",
                "description": desc_element.text if desc_element is not None else "No description",
                "tide": tide_element.text if tide_element is not None else "NIL",
            }
        )

    return {
        "system": system_info,
        "today_situation": today_situation,
        "forecasts": forecasts,
    }


def generate_markdown(
    weather_data: Dict[str, Any], 
    template: Dict[str, str],
    language: Language
) -> str:
    """Generate markdown using template"""
    # Generate forecasts section
    forecasts_text = ""
    for forecast in weather_data["forecasts"]:
        # Handle tide display based on language
        if forecast["tide"] == "NIL":
            if language == Language.CHINESE:
                tide_display = "無資料"
            elif language == Language.PORTUGUESE:
                tide_display = "Sem dados"
            else:  # ENGLISH
                tide_display = "No data"
        else:
            tide_display = forecast["tide"]

        forecasts_text += template["forecast_item"].format(
            date=forecast["date"],
            tide=tide_display,
            description=forecast["description"],
        )

    # Format the main template
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    markdown_content = template["main"].format(
        today_situation=weather_data["today_situation"],
        author=weather_data["system"]["author"],
        pubdate=weather_data["system"]["pubdate"],
        language=weather_data["system"]["language"],
        forecasts=forecasts_text,
        current_time=current_time,
    )

    return markdown_content


def list_available_templates() -> List[str]:
    """List all available template files"""
    try:
        templates = []
        for file in os.listdir(TEMPLATES_DIR):
            if file.endswith(".md"):
                templates.append(file)
        return sorted(templates)
    except FileNotFoundError:
        return ["default_template.md"]


def get_language_from_url(url: str) -> Language:
    """Determine language from URL"""
    if "c_forecast.xml" in url:
        return Language.CHINESE
    elif "p_forecast.xml" in url:
        return Language.PORTUGUESE
    elif "e_forecast.xml" in url:
        return Language.ENGLISH
    else:
        # Default to Chinese if cannot determine
        return Language.CHINESE


def main():
    """Main entry point for the application"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Convert Macau weather XML to markdown with multi-language support"
    )
    parser.add_argument(
        "--template", 
        "-t", 
        help="Template file to use (from templates directory). If not specified, uses default for language."
    )
    parser.add_argument(
        "--list-templates", 
        "-l", 
        action="store_true",
        help="List available templates"
    )
    parser.add_argument(
        "--url",
        "-u",
        help="URL to fetch XML data from. If not specified, uses Chinese version."
    )
    parser.add_argument(
        "--language",
        "-lang",
        choices=["zh", "pt", "en"],
        help="Language to use (zh: Chinese, pt: Portuguese, en: English). Overrides URL detection."
    )
    
    args = parser.parse_args()
    
    if args.list_templates:
        templates = list_available_templates()
        print("Available templates:")
        for template in templates:
            print(f"  - {template}")
        return

    # Determine language and URL
    if args.language:
        language = Language(args.language)
        url = DATA_SOURCES[language]
    elif args.url:
        url = args.url
        language = get_language_from_url(url)
    else:
        # Default to Chinese
        language = Language.CHINESE
        url = DATA_SOURCES[language]

    # Determine template
    if args.template:
        template_file = args.template
    else:
        template_file = DEFAULT_TEMPLATES[language]

    try:
        # Try to load the specified template
        try:
            template = load_template(template_file)
        except (FileNotFoundError, ValueError):
            print(f"⚠️  Template '{template_file}' not found, using default for {LANGUAGE_NAMES[language]}", file=sys.stderr)
            template = create_default_template(language)

        # Fetch the XML data
        print(f"🌤️  Fetching {LANGUAGE_NAMES[language]} weather data from {url}...", file=sys.stderr)
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Parse the XML
        weather_data = parse_weather_xml(response.content)

        # Generate markdown
        print(f"📝 Generating markdown using template: {template_file}", file=sys.stderr)
        markdown_output = generate_markdown(weather_data, template, language)

        # Output the markdown directly to stdout
        print(markdown_output)

    except requests.RequestException as e:
        print(f"❌ Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)
    except ET.ParseError as e:
        print(f"❌ Error parsing XML: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()