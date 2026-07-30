import json
import re
from pypdf import PdfReader
import os

pdf_path = r"C:\Projects\Lord Diagonstics- AI\server\data\pdf\Lord's Pathology Centre Information.pdf"
out_path = r"C:\Projects\Lord Diagonstics- AI\server\data\centres_chunks.json"

reader = PdfReader(pdf_path)
full_text = ""
for page in reader.pages:
    full_text += page.extract_text() + "\n"

# Standardize "Lord’s Pathology" to "Lord's Pathology"
full_text = full_text.replace("Lord’s Pathology", "Lord's Pathology")
# Normalize multiple spaces (excluding newlines) to a single space
# Actually, just replace multiple spaces with a single space to make splitting easier
import re
full_text = re.sub(r' +', ' ', full_text)

# Let's split by "Centre ID: "
parts = full_text.split("Centre ID: ")

# The first part contains the first state summary or intro, but actually we also need summaries.
# Let's parse centres first
centres = []

for part in parts[1:]:
    # The part starts with the ID, e.g., "AP_001"
    id_match = re.match(r'^([A-Z]+_\d+)', part)
    if not id_match:
        continue
    centre_id = id_match.group(1)
    
    state_code = centre_id.split('_')[0]
    
    # Extract Organization
    org_m = re.search(r'Organization:\s*(.+)', part)
    org = org_m.group(1).strip() if org_m else "Lord's Pathology"
    
    # Extract Centre Name
    name_m = re.search(r'Centre Name:\s*(.+?)(?=\nState:|\nCity:)', part, re.DOTALL)
    if name_m:
        centre_name = name_m.group(1).replace('\n', ' ').strip()
        centre_name = re.sub(r'\s+', ' ', centre_name)
    else:
        centre_name = ""
        
    # Extract State
    state_m = re.search(r'State:\s*(.+)', part)
    state = state_m.group(1).strip() if state_m else ""
    
    # Extract City
    city_m = re.search(r'City:\s*(.+)', part)
    city = city_m.group(1).strip() if city_m else ""
    
    # Extract Service Type
    type_m = re.search(r'Service Type:\s*(.+)', part)
    service_type = type_m.group(1).strip() if type_m else ""
    
    # Extract Trust Indicator
    trust_m = re.search(r'Trust Indicator:\s*(.+)', part)
    trust_indicator = trust_m.group(1).strip() if trust_m else ""
    
    # Extract Address
    addr_m = re.search(r'Address:\s*(.+?)(?=\nContact Numbers:)', part, re.DOTALL)
    if addr_m:
        address = addr_m.group(1).replace('\n', ' ').strip()
        address = re.sub(r'\s+', ' ', address)
    else:
        address = ""
        
    # Extract Contact Numbers
    contact_m = re.search(r'Contact Numbers:\s*(.+?)(?=\nAvailable Services:)', part, re.DOTALL)
    contacts = []
    if contact_m:
        c_text = contact_m.group(1).strip()
        contacts = [c.strip() for c in c_text.split() if c.strip().isdigit()]
        
    # Extract Available Services
    srv_m = re.search(r'Available Services:\s*(.+?)(?=\nKeywords:)', part, re.DOTALL)
    services = []
    if srv_m:
        s_text = srv_m.group(1).strip()
        # Since newlines were removed by spaces, we can split by "  " (double spaces) or "●" if they survived
        # Actually in the normalized string it's all single spaces!
        # Let's use a regex to find known service names
        known_services = ["Home Blood Collection", "Blood Test", "CBC Test", "Full Body Health Checkup", "Preventive Health Checkup", "Blood Testing", "Advanced Diagnostic Services", "Regional Reference Laboratory", "Complete Blood Count", "Routine Blood Testing", "Diagnostic Laboratory Services", "Regional Reference Laboratory Services"]
        for ks in known_services:
            if ks.lower() in s_text.lower():
                services.append(ks)
                
    # Extract Keywords
    kw_m = re.search(r'Keywords:\s*(.+?)(?=\n[A-Z][a-z]+ Summary|\nCentre ID:|\Z)', part, re.DOTALL)
    keywords = []
    if kw_m:
        kw_text = kw_m.group(1).strip()
        kw_text = kw_text.replace('\n', ' ')
        kw_text = re.sub(r' +', ' ', kw_text)
        keywords = [k.strip() for k in kw_text.split(',') if k.strip()]
        
    # Locality heuristic (first part of address usually, or from keywords)
    locality = ""
    if address:
        addr_parts = address.split(',')
        if len(addr_parts) > 1:
            locality = addr_parts[0].strip()
    
    # Build search text
    services_str = ", ".join([s.lower() for s in services])
    search_text = f"{org} {service_type.lower()} in {city} {state} provides {services_str} services near {locality}."
    
    chunk = {
        "chunk_id": centre_id,
        "metadata": {
            "document_type": "diagnostic_centre",
            "organization": org,
            "centre_id": centre_id,
            "state": state,
            "city": city,
            "service_type": service_type,
            "locality": locality
        },
        "content": {
            "centre_name": centre_name,
            "trust_indicator": trust_indicator,
            "address": address,
            "contact_numbers": contacts,
            "services": services,
            "keywords": keywords
        },
        "search_text": search_text
    }
    centres.append(chunk)

# Now extract summaries
# We'll just build a basic network summary and state summaries based on the centres list since parsing them is tricky
state_summaries = {}
for c in centres:
    st = c['metadata']['state']
    if st not in state_summaries:
        state_summaries[st] = {
            "chunk_id": f"SUMMARY_{st.upper().replace(' ', '_')}",
            "metadata": {
                "document_type": "state_summary",
                "state": st,
            },
            "content": {
                "state_name": st,
                "total_centres": 0,
                "cities_covered": set(),
                "services_available": set(),
                "contact_numbers": set()
            },
            "search_text": ""
        }
    state_summaries[st]["content"]["total_centres"] += 1
    state_summaries[st]["content"]["cities_covered"].add(c['metadata']['city'])
    for s in c['content']['services']:
        state_summaries[st]["content"]["services_available"].add(s)
    for cn in c['content']['contact_numbers']:
        state_summaries[st]["content"]["contact_numbers"].add(cn)

for st, summ in state_summaries.items():
    summ["content"]["cities_covered"] = list(summ["content"]["cities_covered"])
    summ["content"]["services_available"] = list(summ["content"]["services_available"])
    summ["content"]["contact_numbers"] = list(summ["content"]["contact_numbers"])
    summ["search_text"] = f"Lord's Pathology state summary for {st}. {summ['content']['total_centres']} centres in cities like {', '.join(summ['content']['cities_covered'][:3])}."

network_summary = {
    "chunk_id": "SUMMARY_NETWORK",
    "metadata": {
        "document_type": "network_summary"
    },
    "content": {
        "total_states": len(state_summaries),
        "total_centres": len(centres),
        "state_wise_distribution": {st: summ["content"]["total_centres"] for st, summ in state_summaries.items()},
        "contact_information": ["8097240775", "8976148530"]
    },
    "search_text": f"Lord's Pathology overall network summary covering {len(state_summaries)} states and {len(centres)} centres."
}

final_output = centres + list(state_summaries.values()) + [network_summary]

with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(final_output, f, indent=2, ensure_ascii=False)

print(f"Extraction complete! Saved {len(centres)} centres, {len(state_summaries)} state summaries, and 1 network summary.")
