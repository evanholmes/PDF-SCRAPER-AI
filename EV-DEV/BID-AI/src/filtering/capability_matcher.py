"""
Equipment & Capability Matcher for BID-AI
Verifies opportunities against ALL-PRO SIGNS & WESTCOAST CNC equipment capabilities
Integrates with keyword_matcher.py for comprehensive bid classification
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple

from loguru import logger


class CapabilityPhase(Enum):
    """Phases for capability activation"""

    CURRENT = "current"  # Active now - Signage & Printing
    PHASE_2 = "phase_2"  # Future - CNC Millwork
    PARTNER = "partner"  # Via partner network


@dataclass
class Equipment:
    """Represents a piece of equipment and its capabilities"""

    name: str
    category: str
    phase: CapabilityPhase
    max_width: Optional[float] = None  # inches
    max_length: Optional[float] = None  # inches
    max_thickness: Optional[float] = None  # inches
    precision: Optional[float] = None  # tolerance in inches
    materials: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)


@dataclass
class CapabilityMatch:
    """Result of capability matching"""

    can_fulfill: bool
    equipment_matched: List[str]
    capabilities_matched: List[str]
    materials_matched: List[str]
    phase: CapabilityPhase
    confidence: float  # 0-100
    notes: List[str]
    recommended_tier: str
    tier_rationale: str


class CapabilityMatcher:
    """
    Matches opportunity requirements against company equipment capabilities
    """

    def __init__(self):
        """Initialize with ALL-PRO SIGNS & WESTCOAST CNC equipment"""
        self.equipment = self._load_equipment()
        self.capability_keywords = self._build_keyword_map()
        logger.info(f"Loaded {len(self.equipment)} equipment profiles")

    def _load_equipment(self) -> List[Equipment]:
        """Load equipment configuration"""
        return [
            # === PRINTING & GRAPHICS ===
            Equipment(
                name="Roland VS 540 Eco Solvent Print & Cut",
                category="printing",
                phase=CapabilityPhase.CURRENT,
                max_width=54,  # inches
                materials=[
                    "vinyl",
                    "banner material",
                    "reflective film",
                    "translucent media",
                    "adhesive vinyl",
                    "vehicle wrap vinyl",
                    "window film",
                    "floor graphic vinyl",
                ],
                capabilities=[
                    "eco solvent printing",
                    "print and cut",
                    "contour cutting",
                    "outdoor graphics",
                    "indoor graphics",
                    "vehicle wraps",
                    "window graphics",
                    "wall graphics",
                    "decals",
                    "stickers",
                    "floor graphics",
                    "banners",
                    "reflective signs",
                ],
                keywords=[
                    "vinyl graphics",
                    "vehicle wrap",
                    "decals",
                    "banners",
                    "window graphics",
                    "floor graphics",
                    "wall murals",
                    "reflective",
                    "outdoor signage",
                    "stickers",
                ],
            ),
            Equipment(
                name='Epson SureColor P9570 (44" Wide Format)',
                category="printing",
                phase=CapabilityPhase.CURRENT,
                max_width=44,
                materials=[
                    "photo paper",
                    "fine art paper",
                    "canvas",
                    "presentation paper",
                    "poster paper",
                    "proofing media",
                ],
                capabilities=[
                    "high resolution printing",
                    "color accurate proofs",
                    "presentation graphics",
                    "architectural renderings",
                    "fine art reproduction",
                    "display graphics",
                    "posters",
                ],
                keywords=[
                    "posters",
                    "presentation",
                    "display graphics",
                    "high quality print",
                    "color proof",
                    "architectural",
                ],
            ),
            Equipment(
                name='Epson SureColor F570 Dye Sublimation (24")',
                category="printing",
                phase=CapabilityPhase.CURRENT,
                max_width=24,
                materials=[
                    "polyester fabric",
                    "fabric banner",
                    "textile",
                    "sublimation blanks",
                    "coated substrates",
                ],
                capabilities=[
                    "dye sublimation",
                    "fabric printing",
                    "soft signage",
                    "textile graphics",
                    "heat transfer",
                    "fabric banners",
                    "table covers",
                    "tension fabric displays",
                ],
                keywords=[
                    "fabric",
                    "soft signage",
                    "textile",
                    "sublimation",
                    "table cover",
                    "fabric banner",
                    "backdrop",
                ],
            ),
            # === CNC ROUTING & FABRICATION ===
            Equipment(
                name="Large Format CNC Router (5' x 10')",
                category="cnc",
                phase=CapabilityPhase.CURRENT,  # For signage; PHASE_2 for millwork
                max_width=60,  # 5 feet
                max_length=120,  # 10 feet
                max_thickness=7,  # inches
                precision=0.005,  # ±0.005"
                materials=[
                    "wood",
                    "plywood",
                    "mdf",
                    "hdu",
                    "foam",
                    "eps foam",
                    "acrylic",
                    "plexiglas",
                    "pvc",
                    "polycarbonate",
                    "petg",
                    "composite",
                    "dibond",
                    "aluminum composite",
                    "hdpe",
                    "aluminum plate",  # limited, case-by-case
                ],
                capabilities=[
                    "precision cutting",
                    "cnc routing",
                    "3d carving",
                    "v-carving",
                    "dimensional letters",
                    "sign faces",
                    "channel letter backs",
                    "monument components",
                    "wayfinding panels",
                    "custom shapes",
                    "drilling",
                    "milling",
                    "engraving",
                ],
                keywords=[
                    "dimensional letters",
                    "cnc",
                    "router",
                    "carved",
                    "acrylic",
                    "wood",
                    "mdf",
                    "hdu",
                    "foam",
                    "pvc",
                    "monument sign",
                    "wayfinding",
                    "custom shape",
                    "millwork",
                    "architectural",
                ],
            ),
            # === CHANNEL LETTER PRODUCTION ===
            Equipment(
                name="Automatic Channel Letter Bending Machine",
                category="channel_letters",
                phase=CapabilityPhase.CURRENT,
                materials=["aluminum coil", "aluminum return"],
                capabilities=[
                    "channel letter fabrication",
                    "aluminum return bending",
                    "illuminated letters",
                    "halo-lit letters",
                    "reverse channel",
                    "front-lit letters",
                    "dimensional letters",
                    "building signage",
                ],
                keywords=[
                    "channel letters",
                    "illuminated sign",
                    "illuminated letters",
                    "building signage",
                    "exterior signage",
                    "led sign",
                    "halo lit",
                    "backlit",
                ],
            ),
            # === 3D PRINTING ===
            Equipment(
                name='Large Format 3D Printer (24" x 24" x 24")',
                category="3d_printing",
                phase=CapabilityPhase.CURRENT,
                max_width=24,
                max_length=24,
                max_thickness=24,
                materials=["pla", "petg", "abs", "asa"],
                capabilities=[
                    "3d printing",
                    "additive manufacturing",
                    "prototyping",
                    "custom brackets",
                    "decorative elements",
                    "small letters",
                    "specialty shapes",
                    "mounting hardware",
                ],
                keywords=[
                    "3d print",
                    "prototype",
                    "custom",
                    "bracket",
                    "decorative",
                    "specialty",
                ],
            ),
            # === LASER ENGRAVING ===
            Equipment(
                name="Laser Engraver (In-House)",
                category="laser",
                phase=CapabilityPhase.CURRENT,
                materials=["wood", "wood products"],
                capabilities=[
                    "laser engraving",
                    "logo engraving",
                    "branding",
                    "decorative detail",
                    "personalization",
                    "name plates",
                ],
                keywords=[
                    "laser engrav",
                    "engrav",
                    "etch",
                    "name plate",
                    "branding",
                    "logo",
                ],
            ),
            Equipment(
                name="Large Format CO2 Laser (Partner Network)",
                category="laser",
                phase=CapabilityPhase.PARTNER,
                materials=["acrylic", "wood", "fabric", "leather", "paper"],
                capabilities=[
                    "laser cutting",
                    "large format laser",
                    "intricate cutting",
                    "specialty laser work",
                ],
                keywords=["laser cut", "intricate", "precision cut"],
            ),
            # === FINISHING ===
            Equipment(
                name="Wide Format Laminator",
                category="finishing",
                phase=CapabilityPhase.CURRENT,
                materials=["printed graphics", "vinyl", "paper"],
                capabilities=[
                    "lamination",
                    "protective coating",
                    "uv protection",
                    "anti-graffiti",
                    "matte finish",
                    "gloss finish",
                ],
                keywords=[
                    "laminate",
                    "lamination",
                    "protective",
                    "coating",
                    "finish",
                    "uv resistant",
                ],
            ),
            Equipment(
                name="Panel Saw / Substrate Cutter",
                category="finishing",
                phase=CapabilityPhase.CURRENT,
                materials=[
                    "plywood",
                    "mdf",
                    "acrylic",
                    "aluminum composite",
                    "pvc sheet",
                    "foam board",
                ],
                capabilities=[
                    "sheet cutting",
                    "substrate preparation",
                    "material breakdown",
                ],
                keywords=[],  # Support equipment, not directly bid-matched
            ),
            # === FUTURE PHASE 2: MILLWORK ===
            Equipment(
                name="CNC Millwork Capabilities",
                category="millwork",
                phase=CapabilityPhase.PHASE_2,
                materials=["hardwood", "plywood", "mdf", "veneer"],
                capabilities=[
                    "architectural millwork",
                    "cabinetry",
                    "decorative panels",
                    "moldings",
                    "trim",
                    "furniture components",
                ],
                keywords=[
                    "millwork",
                    "cabinetry",
                    "cabinet",
                    "architectural millwork",
                    "molding",
                    "trim",
                    "furniture",
                    "woodwork",
                ],
            ),
        ]

    def _build_keyword_map(self) -> Dict[str, List[Equipment]]:
        """Build reverse lookup: keyword -> equipment that can handle it"""
        keyword_map = {}

        for equip in self.equipment:
            for keyword in equip.keywords:
                keyword_lower = keyword.lower()
                if keyword_lower not in keyword_map:
                    keyword_map[keyword_lower] = []
                keyword_map[keyword_lower].append(equip)

        return keyword_map

    def match_opportunity(
        self, title: str, description: str = "", keywords_matched: List[str] = None
    ) -> CapabilityMatch:
        """
        Match an opportunity against equipment capabilities

        Args:
            title: Opportunity title
            description: Opportunity description
            keywords_matched: Pre-matched keywords from KeywordMatcher

        Returns:
            CapabilityMatch with equipment and capability details
        """
        title_lower = title.lower()
        description_lower = description.lower() if description else ""
        combined_text = f"{title_lower} {description_lower}"

        # Track matches
        equipment_matched: Set[str] = set()
        capabilities_matched: Set[str] = set()
        materials_matched: Set[str] = set()
        phases_found: Set[CapabilityPhase] = set()
        notes: List[str] = []

        # Check each equipment
        for equip in self.equipment:
            equip_matches = False

            # Check keywords
            for keyword in equip.keywords:
                if keyword.lower() in combined_text:
                    equip_matches = True
                    break

            # Check capabilities
            for capability in equip.capabilities:
                if capability.lower() in combined_text:
                    equip_matches = True
                    capabilities_matched.add(capability)

            # Check materials
            for material in equip.materials:
                if material.lower() in combined_text:
                    equip_matches = True
                    materials_matched.add(material)

            # Also check against pre-matched keywords
            if keywords_matched:
                for kw in keywords_matched:
                    if kw.lower() in [k.lower() for k in equip.keywords]:
                        equip_matches = True
                    for cap in equip.capabilities:
                        if kw.lower() in cap.lower():
                            equip_matches = True
                            capabilities_matched.add(cap)

            if equip_matches:
                equipment_matched.add(equip.name)
                phases_found.add(equip.phase)

        # Determine overall phase
        if CapabilityPhase.CURRENT in phases_found:
            primary_phase = CapabilityPhase.CURRENT
        elif CapabilityPhase.PHASE_2 in phases_found:
            primary_phase = CapabilityPhase.PHASE_2
        elif CapabilityPhase.PARTNER in phases_found:
            primary_phase = CapabilityPhase.PARTNER
        else:
            primary_phase = CapabilityPhase.CURRENT  # Default

        # Calculate confidence
        match_count = (
            len(equipment_matched) + len(capabilities_matched) + len(materials_matched)
        )
        if match_count > 10:
            confidence = 100.0
        elif match_count > 5:
            confidence = 80.0
        elif match_count > 2:
            confidence = 60.0
        elif match_count > 0:
            confidence = 40.0
        else:
            confidence = 0.0

        # Determine tier and fulfillment
        can_fulfill = len(equipment_matched) > 0

        if can_fulfill and primary_phase == CapabilityPhase.CURRENT:
            tier = "A"
            rationale = f"Direct fulfillment - Equipment matched: {', '.join(list(equipment_matched)[:3])}"
        elif can_fulfill and primary_phase == CapabilityPhase.PHASE_2:
            tier = "B"
            rationale = (
                f"Phase 2 capability (CNC Millwork) - Defer or assign to partner"
            )
        elif can_fulfill and primary_phase == CapabilityPhase.PARTNER:
            tier = "C"
            rationale = f"Partner fulfillment required - {', '.join(list(equipment_matched)[:2])}"
        elif keywords_matched and len(keywords_matched) > 0:
            tier = "B"
            rationale = f"Relevant but no direct equipment match - consider assignment"
            can_fulfill = False
        else:
            tier = "E"
            rationale = "No equipment or capability match - Archive"
            can_fulfill = False

        # Add phase notes
        if (
            CapabilityPhase.PHASE_2 in phases_found
            and primary_phase != CapabilityPhase.PHASE_2
        ):
            notes.append(
                "Some Phase 2 (millwork) capabilities also match - potential future expansion"
            )
        if CapabilityPhase.PARTNER in phases_found:
            notes.append("Partner network may be required for some aspects")

        return CapabilityMatch(
            can_fulfill=can_fulfill,
            equipment_matched=list(equipment_matched),
            capabilities_matched=list(capabilities_matched),
            materials_matched=list(materials_matched),
            phase=primary_phase,
            confidence=confidence,
            notes=notes,
            recommended_tier=tier,
            tier_rationale=rationale,
        )

    def get_equipment_for_capability(self, capability: str) -> List[Equipment]:
        """Find equipment that can handle a specific capability"""
        results = []
        capability_lower = capability.lower()

        for equip in self.equipment:
            for cap in equip.capabilities:
                if capability_lower in cap.lower():
                    results.append(equip)
                    break
            for kw in equip.keywords:
                if capability_lower in kw.lower():
                    if equip not in results:
                        results.append(equip)
                    break

        return results

    def get_current_capabilities(self) -> List[str]:
        """Get list of all current phase capabilities"""
        capabilities = set()
        for equip in self.equipment:
            if equip.phase == CapabilityPhase.CURRENT:
                capabilities.update(equip.capabilities)
        return sorted(list(capabilities))

    def get_materials_processable(self) -> List[str]:
        """Get list of all materials we can process (current phase)"""
        materials = set()
        for equip in self.equipment:
            if equip.phase == CapabilityPhase.CURRENT:
                materials.update(equip.materials)
        return sorted(list(materials))


# Global instance for convenience
_capability_matcher: Optional[CapabilityMatcher] = None


def get_capability_matcher() -> CapabilityMatcher:
    """Get global capability matcher instance"""
    global _capability_matcher
    if _capability_matcher is None:
        _capability_matcher = CapabilityMatcher()
    return _capability_matcher


if __name__ == "__main__":
    # Test the capability matcher
    matcher = get_capability_matcher()

    print("=" * 60)
    print("ALL-PRO SIGNS & WESTCOAST CNC - Capability Matcher Test")
    print("=" * 60)

    # Test cases
    test_opportunities = [
        {
            "title": "RFP for Wayfinding Signage System",
            "description": "Design and install interior wayfinding signage including dimensional letters, directional signs, and ADA-compliant room signs in acrylic and aluminum.",
        },
        {
            "title": "Large Format Printing Services",
            "description": "Provide large format vinyl graphics, vehicle wraps, and banner printing services.",
        },
        {
            "title": "Channel Letter Fabrication and Installation",
            "description": "Fabricate and install illuminated channel letters for building identification signage.",
        },
        {
            "title": "Custom CNC Millwork for Library Renovation",
            "description": "Architectural millwork including custom cabinetry, decorative panels, and moldings.",
        },
        {
            "title": "Road Paving Services",
            "description": "Asphalt paving and road maintenance for municipal roads.",
        },
    ]

    for i, opp in enumerate(test_opportunities, 1):
        print(f"\n📋 Test {i}: {opp['title']}")
        result = matcher.match_opportunity(opp["title"], opp["description"])

        print(f"   Can Fulfill: {'✅ Yes' if result.can_fulfill else '❌ No'}")
        print(f"   Tier: {result.recommended_tier}")
        print(f"   Confidence: {result.confidence}%")
        print(f"   Phase: {result.phase.value}")
        if result.equipment_matched:
            print(f"   Equipment: {', '.join(result.equipment_matched[:3])}")
        if result.capabilities_matched:
            print(
                f"   Capabilities: {', '.join(list(result.capabilities_matched)[:3])}"
            )
        if result.materials_matched:
            print(f"   Materials: {', '.join(list(result.materials_matched)[:3])}")
        print(f"   Rationale: {result.tier_rationale}")
        if result.notes:
            for note in result.notes:
                print(f"   📝 {note}")

    print("\n" + "=" * 60)
    print("Current Capabilities Count:", len(matcher.get_current_capabilities()))
    print("Processable Materials Count:", len(matcher.get_materials_processable()))
    print("=" * 60)
