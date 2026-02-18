from src.parsers.csi_parser_bbox import CSIParser
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="WARNING")  # Less verbose

# Adjusted bbox to capture full titles
parser = CSIParser(
    left_bbox=(0, 0, 340, 792),
    right_bbox=(340, 0, 612, 792)
)

result = parser.parse_pdf("data/input/MasterFormat_2020 - pgs_17-39 - MasterFormat Groups, Subgroups, and Divisions.pdf")

print(f"=== PARSING RESULTS ===")
print(f"Total codes extracted: {len(result)}")
print(f"\n=== Sample entries (checking multi-line merging) ===")

# Look for entries that should have merged titles
for i, code in enumerate(result[:50]):
    if 'Cleaning' in code['title'] or 'Maintenance' in code['title'] or 'Product Delivery' in code['title']:
        print(f"{i+1:3d}. {code['division']} | {code['code']} | {code['title']}")

print(f"\n=== First 30 entries ===")
for i, code in enumerate(result[:30]):
    print(f"{i+1:3d}. {code['division']} | {code['code']} | {code['title']}")

print(f"\n=== Last 10 entries ===")
for i, code in enumerate(result[-10:]):
    print(f"{len(result)-10+i+1:3d}. {code['division']} | {code['code']} | {code['title']}")
