# Deal Flow System Design

## Overview

Every bid opportunity that enters BID-AI flows through a classification system that determines its path - whether to THE PARENT COMPANY or to the partner network.

---

## Flow Diagram

```
                         ┌─────────────────────┐
                         │   BID OPPORTUNITY   │
                         │   DETECTED          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  RELEVANCE FILTER   │
                         │  (Signage/Printing?)│
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
            ┌──────────────┐               ┌──────────────┐
            │   RELEVANT   │               │ NOT RELEVANT │
            │              │               │              │
            └──────┬───────┘               └──────┬───────┘
                   │                              │
                   ▼                              ▼
         ┌─────────────────┐              ┌─────────────┐
         │  CAPABILITY     │              │   ARCHIVE   │
         │  ASSESSMENT     │              │  (Data only)│
         └────────┬────────┘              └─────────────┘
                  │
    ┌─────────────┼─────────────┬─────────────────┐
    │             │             │                 │
    ▼             ▼             ▼                 ▼
┌────────┐  ┌──────────┐  ┌──────────┐    ┌───────────┐
│FULFILL │  │ PARTNER  │  │  ASSIGN  │    │  BROKER   │
│        │  │          │  │          │    │           │
│ 100%   │  │ Partial  │  │ 0% our   │    │ Sell our  │
│ ours   │  │ ours     │  │ capacity │    │ expertise │
└───┬────┘  └────┬─────┘  └────┬─────┘    └─────┬─────┘
    │            │             │                │
    ▼            ▼             ▼                ▼
┌────────┐  ┌──────────┐  ┌──────────┐    ┌───────────┐
│  BID   │  │ FIND     │  │ FIND     │    │ FIND      │
│DIRECTLY│  │ PARTNER  │  │ ASSIGNEE │    │ CLIENT    │
└───┬────┘  └────┬─────┘  └────┬─────┘    └─────┬─────┘
    │            │             │                │
    ▼            ▼             ▼                ▼
┌────────┐  ┌──────────┐  ┌──────────┐    ┌───────────┐
│  WIN   │  │ JOINT    │  │ REFERRAL │    │ CONSULTING│
│CONTRACT│  │ PROPOSAL │  │ FEE      │    │ FEE       │
└────────┘  └──────────┘  └──────────┘    └───────────┘
```

---

## Classification Criteria

### FULFILL (Direct Bid)

**Criteria Matrix:**
| Factor | Threshold |
|--------|-----------|
| Material Capability | ≥ 90% in-house or standard supply |
| Equipment Capability | ≥ 90% in-house |
| Capacity Available | Sufficient for timeline |
| Geographic Fit | Within service area |
| Contract Size | Within bonding/insurance limits |
| Risk Profile | Low to Medium |

**Decision:** THE PARENT COMPANY bids directly, executes fully.

---

### PARTNER (Joint Venture)

**Criteria Matrix:**
| Factor | Threshold |
|--------|-----------|
| Material Capability | 50-89% in-house |
| Equipment Capability | 50-89% in-house |
| Strategic Value | High (relationship, learning, prestige) |
| Partner Available | Known partner with complementary capability |

**Decision:** Form JV with partner who fills gaps. Split work and revenue.

**Structure Options:**
- THE PARENT COMPANY as prime, partner as sub
- Partner as prime, THE PARENT COMPANY as sub
- True JV with shared liability

---

### ASSIGN (Referral)

**Criteria Matrix:**
| Factor | Threshold |
|--------|-----------|
| Material Capability | < 50% in-house |
| Equipment Capability | < 50% in-house |
| Specialty Required | Outside core competency |
| Partner Match | Known partner with full capability |

**Decision:** Package opportunity and refer to capable partner for fee.

**Fee Structure Options:**
- Flat finder's fee ($500 - $5,000 based on contract size)
- Percentage of contract (3-7%)
- Hybrid (flat fee + success bonus)

---

### BROKER (Consulting)

**Criteria Matrix:**
| Factor | Threshold |
|--------|-----------|
| Capability | Cannot fulfill |
| Partner Match | No established partner relationship |
| Opportunity Value | High enough to justify effort |
| Bidder Interest | Potential bidder identified who needs help |

**Decision:** Offer bid preparation consulting services to potential bidder.

**Service Options:**
- Full proposal writing
- Compliance review only
- Requirements analysis
- Pricing strategy

---

## Capability Assessment Framework

### Materials Assessment

For each bid, THE BID MASTER evaluates:

```yaml
materials_assessment:
  specified_materials:
    - material: "3mm ACM Dibond"
      quantity: "50 sqm"
      our_capability: "core"  # core | available | specialty | cannot
      lead_time: "3 days"
      
    - material: "Cast bronze letters"
      quantity: "45 characters"  
      our_capability: "cannot"
      lead_time: "N/A"
      partner_capable: "Company B - Bronze Specialists"
      
  overall_material_score: 0.65  # 65% we can handle
```

### Equipment Assessment

```yaml
equipment_assessment:
  required_processes:
    - process: "CNC routing"
      our_capability: "core"
      
    - process: "Bronze casting"
      our_capability: "cannot"
      partner_capable: "Company B"
      
  overall_equipment_score: 0.70  # 70% we can handle
```

### Capacity Assessment

```yaml
capacity_assessment:
  timeline_required: "6 weeks"
  current_workload: "75%"
  can_accommodate: true
  overtime_required: false
  
  capacity_score: 0.85
```

### Final Classification

```yaml
classification:
  fulfill_score: 0.65  # Weighted average
  
  recommendation: "PARTNER"
  
  reasoning: |
    Material capability at 65% - we can do ACM and aluminum
    but bronze letters require specialty partner.
    Recommend JV with Company B for bronze elements.
    
  proposed_structure:
    prime_contractor: "THE PARENT COMPANY"
    subcontractor: "Company B"
    our_scope: "All signage except bronze letters"
    partner_scope: "Bronze letter fabrication and finishing"
    revenue_split: "75/25"
```

---

## Partner Network Database

### Partner Profile Template

```yaml
partner:
  company_name: ""
  contact_name: ""
  contact_email: ""
  contact_phone: ""
  
  location: ""
  service_area: ""
  
  specialties:
    - specialty: ""
      capability_level: ""  # expert | capable | limited
      
  equipment:
    - ""
    
  certifications:
    - ""
    
  capacity:
    monthly_volume: ""
    current_utilization: ""
    
  relationship:
    status: ""  # prospect | active | preferred
    first_contact: ""
    deals_referred: 0
    deals_completed: 0
    revenue_generated: 0
    
  terms:
    referral_fee: ""
    partnership_split: ""
    exclusivity: ""
```

---

## Revenue Tracking

### Deal Flow Metrics

| Metric | Definition |
|--------|------------|
| Opportunities Detected | All signage/printing bids found |
| Classified as FULFILL | Bids we pursue directly |
| Classified as PARTNER | JV opportunities |
| Classified as ASSIGN | Referral opportunities |
| Classified as BROKER | Consulting opportunities |
| Conversion Rate | Opportunities pursued / detected |
| Win Rate (Direct) | Direct wins / direct bids |
| Referral Success Rate | Referrals that won / referrals made |
| Network Revenue | Total $ from non-direct sources |

### Revenue Attribution

```
Monthly Revenue Report
═══════════════════════════════════════════════════

DIRECT CONTRACTS
├─ Contract: Vancouver Park Wayfinding
│  └─ Value: $45,000 | Margin: $13,500 (30%)
├─ Contract: Surrey Regulatory Signs  
│  └─ Value: $28,000 | Margin: $8,400 (30%)
└─ SUBTOTAL: $21,900

PARTNER CONTRACTS  
├─ Contract: Metro Van Monument Signs (JV with Company B)
│  └─ Total: $120,000 | Our Share: 60% | Revenue: $72,000 | Margin: $21,600
└─ SUBTOTAL: $21,600

REFERRAL FEES
├─ Referral: TransLink Station Signs → Company C
│  └─ Contract: $200,000 | Fee: 5% | Revenue: $10,000
└─ SUBTOTAL: $10,000

CONSULTING FEES
├─ Bid Prep: Chilliwack Trail Signs for Company D
│  └─ Fee: $3,500
└─ SUBTOTAL: $3,500

═══════════════════════════════════════════════════
TOTAL MONTHLY REVENUE: $57,000
├─ Direct: 38%
├─ Partner: 38%  
├─ Referral: 18%
└─ Consulting: 6%
```

---

## System Integration

### THE BID MASTER Decision Tree

When a new opportunity is detected:

1. **Scout Agent** detects and flags opportunity
2. **Analyst Agent** performs capability assessment
3. **Analyst Agent** generates classification recommendation
4. **BID MASTER** reviews and confirms classification
5. Based on classification:
   - FULFILL → Standard bid workflow
   - PARTNER → Partner matching workflow
   - ASSIGN → Referral workflow
   - BROKER → Consulting workflow
6. Track outcome regardless of path
7. Update metrics and partner records

---

*Deal Flow System Version: 1.0*
*Last Updated: December 2025*
