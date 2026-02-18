from src.parsers.csi_parser_final import CSIParser
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="WARNING")

# Word-level extraction should capture complete titles
parser = CSIParser(column_split_x=320.0)

result = parser.parse_pdf("data/input/MasterFormat_2020 - pgs_17-39 - MasterFormat Groups, Subgroups, and Divisions.pdf")

print(f"=== PARSING RESULTS (Word-Level Extraction) ===")
print(f"Total codes extracted: {len(result)}")

print(f"\n=== First 30 entries (checking title completeness) ===")
for i, code in enumerate(result[:30]):
    print(f"{i+1:3d}. {code['division']} | {code['code']} | {code['title']}")

print(f"\n=== Sample from middle ===")
for i, code in enumerate(result[100:110]):
    print(f"{i+101:3d}. {code['division']} | {code['code']} | {code['title']}")

print(f"\n=== Last 10 entries ===")
for i, code in enumerate(result[-10:]):
    print(f"{len(result)-10+i+1:3d}. {code['division']} | {code['code']} | {code['title']}")
