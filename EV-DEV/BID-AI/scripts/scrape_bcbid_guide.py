#!/usr/bin/env python3
"""
Scrape BC Bid Supplier Guide including accordion sections
"""

import asyncio
from pathlib import Path

from playwright.async_api import async_playwright


async def scrape_bcbid_guide():
    """Scrape the BC Bid Supplier Guide with all accordion content expanded"""

    url = "https://www2.gov.bc.ca/gov/content/bc-procurement-resources/bc-bid-resources/bc-bid-user-guides/bc-bid-supplier-guide"

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print(f"Loading {url}...")
        await page.goto(url, wait_until="networkidle")

        # Find and click all accordion buttons to expand them
        print("Expanding accordion sections...")
        accordion_buttons = await page.query_selector_all("button[aria-expanded]")

        for button in accordion_buttons:
            try:
                aria_expanded = await button.get_attribute("aria-expanded")
                if aria_expanded == "false":
                    await button.click()
                    await page.wait_for_timeout(500)  # Wait for animation
            except Exception as e:
                print(f"Could not click button: {e}")

        # Wait a bit for all content to load
        await page.wait_for_timeout(1000)

        # Get all text content - try multiple selectors
        print("Extracting content...")

        selectors = [
            "main",
            "article",
            "#main-content",
            ".page-content",
            '[role="main"]',
            "body",
        ]
        main_content = None

        for selector in selectors:
            main_content = await page.query_selector(selector)
            if main_content:
                text_content = await main_content.inner_text()
                if text_content and len(text_content) > 100:
                    print(
                        f"✓ Found content with selector: {selector} ({len(text_content)} chars)"
                    )
                    break

        if main_content and text_content and len(text_content) > 100:
            # Also get structured content
            html_content = await main_content.inner_html()

            # Save both versions
            output_dir = Path(__file__).parent.parent / "docs" / "scraped"
            output_dir.mkdir(exist_ok=True, parents=True)

            # Save text version
            text_file = output_dir / "bcbid_supplier_guide.txt"
            with open(text_file, "w", encoding="utf-8") as f:
                f.write(text_content)
            print(f"✓ Saved text version: {text_file}")

            # Save markdown version (cleaned)
            md_content = format_as_markdown(text_content)
            md_file = output_dir / "bcbid_supplier_guide.md"
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(md_content)
            print(f"✓ Saved markdown version: {md_file}")

            # Print preview
            print("\n" + "=" * 60)
            print("PREVIEW (first 2000 characters):")
            print("=" * 60)
            print(text_content[:2000])
            print("=" * 60)
            print(f"\nTotal length: {len(text_content)} characters")

        else:
            print("❌ Could not find main content area")

        await browser.close()


def format_as_markdown(text):
    """Basic formatting to make text more readable as markdown"""
    lines = text.split("\n")
    formatted = []

    formatted.append("# BC Bid Supplier Guide\n")
    formatted.append(
        "*Scraped from: https://www2.gov.bc.ca/gov/content/bc-procurement-resources/bc-bid-resources/bc-bid-user-guides/bc-bid-supplier-guide*\n"
    )
    formatted.append(
        f"*Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"
    )
    formatted.append("---\n")

    for line in lines:
        line = line.strip()
        if not line:
            formatted.append("")
            continue

        # Detect headings (heuristic: short lines in all caps or title case)
        if len(line) < 100 and (line.isupper() or line.istitle()):
            if len(line) < 50:
                formatted.append(f"\n## {line}\n")
            else:
                formatted.append(f"\n### {line}\n")
        else:
            formatted.append(line)

    return "\n".join(formatted)


if __name__ == "__main__":
    asyncio.run(scrape_bcbid_guide())
