from src.parsers.csi_parser_bbox import CSIParser
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="INFO")

# Correct bbox: page is 612x792
# Left column: x0=0 to x1=306 (middle), Right column: x1=306 to x1=612
parser = CSIParser(
    left_bbox=(0, 0, 306, 792),
    right_bbox=(306, 0, 612, 792)
)

result = parser.parse_pdf("data/input/MasterFormat_2020 - pgs_17-39 - MasterFormat Groups, Subgroups, and Divisions.pdf")

print(f"\n=== PARSING RESULTS ===")
print(f"Total codes extracted: {len(result)}")
print(f"\n=== First 20 entries ===")
for i, code in enumerate(result[:20]):
    print(f"{i+1:3d}. {code['division']} | {code['code']} | {code['title']}")

print(f"\n=== Last 10 entries ===")
for i, code in enumerate(result[-10:]):
    print(f"{len(result)-10+i+1:3d}. {code['division']} | {code['code']} | {code['title']}")
