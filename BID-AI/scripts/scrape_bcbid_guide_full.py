#!/usr/bin/env python3
"""
Comprehensive BC Bid Supplier Guide scraper
Expands all accordions and captures full content
"""

import asyncio
import time
from pathlib import Path

from playwright.async_api import async_playwright


async def scrape_bcbid_guide_full():
    """Scrape BC Bid guide with all content expanded"""

    url = "https://www2.gov.bc.ca/gov/content/bc-procurement-resources/bc-bid-resources/bc-bid-user-guides/bc-bid-supplier-guide"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Show browser for debugging
        page = await browser.new_page()

        print(f"📄 Loading {url}...")
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # Try to find and click "Expand all" button
        print("🔍 Looking for 'Expand all' button...")
        expand_buttons = await page.get_by_text("Expand all").all()

        if expand_buttons:
            print(f"✓ Found {len(expand_buttons)} 'Expand all' button(s)")
            for btn in expand_buttons:
                try:
                    await btn.click()
                    print("✓ Clicked 'Expand all'")
                    await page.wait_for_timeout(2000)  # Wait for expansion
                except Exception as e:
                    print(f"Could not click expand button: {e}")
        else:
            print("⚠️  No 'Expand all' button found, trying individual accordions...")

            # Try clicking individual accordion buttons
            accordion_selectors = [
                'button[aria-expanded="false"]',
                ".accordion-button",
                '[role="button"][aria-expanded="false"]',
                "summary",
            ]

            for selector in accordion_selectors:
                buttons = await page.query_selector_all(selector)
                if buttons:
                    print(
                        f"Found {len(buttons)} accordion buttons with selector: {selector}"
                    )
                    for i, button in enumerate(buttons):
                        try:
                            await button.click()
                            await page.wait_for_timeout(300)
                            print(f"  ✓ Expanded accordion {i + 1}/{len(buttons)}")
                        except Exception as e:
                            print(f"  ✗ Could not expand {i + 1}: {e}")
                    break

        # Wait for all animations to complete
        await page.wait_for_timeout(3000)

        # Extract all content
        print("\n📝 Extracting content...")

        # Get the whole body
        body = await page.query_selector("body")
        full_text = await body.inner_text()

        # Also try to get just the main content area
        main_area = await page.query_selector("main") or await page.query_selector(
            '[role="main"]'
        )
        if main_area:
            main_text = await main_area.inner_text()
        else:
            main_text = full_text

        print(f"✓ Extracted {len(main_text)} characters")

        # Save the content
        output_dir = Path(__file__).parent.parent / "docs" / "scraped"
        output_dir.mkdir(exist_ok=True, parents=True)

        # Save full text
        text_file = output_dir / "bcbid_supplier_guide_full.txt"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(main_text)
        print(f"✓ Saved: {text_file}")

        # Create AI-optimized markdown
        md_content = create_ai_optimized_markdown(main_text)
        md_file = output_dir / "bcbid_supplier_guide_ai.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"✓ Saved: {md_file}")

        # Show preview
        print("\n" + "=" * 60)
        print("PREVIEW (first 1500 chars):")
        print("=" * 60)
        print(main_text[:1500])
        print("=" * 60)
        print(f"\nTotal content: {len(main_text)} characters")
        print(f"Estimated tokens: ~{len(main_text) // 4}")

        # Keep browser open for a moment to verify
        print("\n✓ Scraping complete! Check the output files.")
        await page.wait_for_timeout(2000)

        await browser.close()


def create_ai_optimized_markdown(text):
    """Format text for optimal AI consumption"""

    lines = text.split("\n")

    output = []
    output.append("# BC Bid Supplier Guide - AI Reference\n")
    output.append(
        f"**Source**: https://www2.gov.bc.ca/gov/content/bc-procurement-resources/bc-bid-resources/bc-bid-user-guides/bc-bid-supplier-guide\n"
    )
    output.append(f"**Scraped**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    output.append(
        "**Purpose**: Complete reference for BC Bid portal supplier operations\n"
    )
    output.append("---\n\n")

    # Clean and structure the content
    in_section = False
    section_depth = 0

    for line in lines:
        line = line.strip()

        # Skip navigation and headers
        if any(
            skip in line.lower()
            for skip in ["skip to main", "menu", "search", "accessibility statement"]
        ):
            continue

        if not line:
            output.append("")
            continue

        # Detect section headings
        if any(
            keyword in line
            for keyword in [
                "Step ",
                "General interface",
                "Prepare & register",
                "Supplier dashboard",
                "Account management",
                "Explore",
            ]
        ):
            output.append(f"\n## {line}\n")
            section_depth = 2
        elif line.isupper() and len(line) < 60:
            output.append(f"\n### {line}\n")
        elif line.endswith(":") and len(line) < 80:
            output.append(f"\n**{line}**\n")
        else:
            output.append(line)

    return "\n".join(output)


if __name__ == "__main__":
    asyncio.run(scrape_bcbid_guide_full())
