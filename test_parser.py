from src.parsers.csi_parser import CSIParser
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="DEBUG")

parser = CSIParser()

# Test on page 3 (index 2)
result = parser.parse_pdf("data/input/MasterFormat_2020 - pgs_17-39 - MasterFormat Groups, Subgroups, and Divisions.pdf")

print(f"\n=== PARSING RESULTS ===")
print(f"Total codes extracted: {len(result)}")
print(f"\n=== First 10 entries ===")
for i, code in enumerate(result[:10]):
    print(f"{i+1}. {code['division']} | {code['code']} | {code['title']}")

print(f"\n=== Last 5 entries ===")
for i, code in enumerate(result[-5:]):
    print(f"{i+1}. {code['division']} | {code['code']} | {code['title']}")
