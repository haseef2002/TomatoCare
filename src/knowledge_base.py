# src/knowledge_base.py

DISEASE_KB = {
    "Tomato___Early_blight": {
        "common": "Early Blight",
        "pathogen": "Alternaria solani",
        "risk_params": {"temp": (22, 32), "hum": 75}, 
        "vulnerable_stage": "Fruiting",
        "impact_factors": {"visual": 0.8, "env": 0.2}, 
        "visual_cues": [
            "Small, dark spots on older leaves first.",
            "Concentric rings (looks like a 'bullseye' or target).",
            "Yellowing (chlorosis) around the spots."
        ],
        "infection_location": "Bottom of the plant (spreads upward).",
        "why": "Fungal spores require free moisture and warm temperatures to germinate, forming target-like concentric lesions on older leaves.",
        "prevention": "Stake plants for better airflow. Use mulch to prevent soil-borne spores from splashing onto lower leaves.",
        "treatment": "Apply protectant fungicides (Chlorothalonil or Copper-based).",
        "natural_treatment": "Prune lower infected leaves immediately. Apply organic Neem oil extract or a baking soda spray (1 tbsp baking soda per gallon of water) to suppress fungal spread.",
        "fatality": "High: Defoliation leads to severe yield loss and fruit sunscald.",
        "dosage_rate_per_acre_ml": 500,
        "ref_source": "Cornell University Vegetable MD Online",
        "ref_url": "https://www.vegetables.cornell.edu/pest-management/disease-factsheets/tomato-disease-identification-key/"
    },
    "Tomato___Late_blight": {
        "common": "Late Blight",
        "pathogen": "Phytophthora infestans",
        "risk_params": {"temp": (12, 26), "hum": 85}, 
        "vulnerable_stage": "Any",
        "impact_factors": {"visual": 0.5, "env": 0.5}, 
        "visual_cues": [
            "Dark, water-soaked patches on leaves.",
            "White, fuzzy mold on the underside of leaves in humid weather.",
            "Large sections of the leaf turn brown and papery."
        ],
        "infection_location": "Anywhere on the plant; spreads extremely fast.",
        "why": "This oomycete (water mold) reproduces explosively in cool, wet conditions via wind-borne zoospores.",
        "prevention": "Plant resistant cultivars (e.g., 'Mountain Magic'). Avoid overhead irrigation.",
        "treatment": "Mancozeb or systemic fungicides (Mefenoxam). Destroy infected plants immediately.",
        "natural_treatment": "There is no highly effective organic cure once late blight is established. Apply Copper octanoate (copper soap) preventatively on remaining healthy plants. Destroy all infected tissue.",
        "fatality": "Extreme: Can destroy entire fields in 7–10 days.",
        "dosage_rate_per_acre_ml": 800,
        "ref_source": "UC IPM Pest Management Guidelines",
        "ref_url": "https://ipm.ucanr.edu/agriculture/tomato/late-blight/"
    },
    "Tomato___Bacterial_spot": {
        "common": "Bacterial Spot",
        "pathogen": "Xanthomonas perforans",
        "risk_params": {"temp": (24, 32), "hum": 80},
        "vulnerable_stage": "Flowering",
        "impact_factors": {"visual": 0.7, "env": 0.3},
        "visual_cues": [
            "Small, water-soaked spots that turn dark brown or black.",
            "Spots do not have concentric rings.",
            "Leaves may turn yellow and drop prematurely."
        ],
        "infection_location": "Throughout the canopy; spread by splashing water.",
        "why": "Bacteria enter through stomata or wounds. Spread is driven by splashing rain and high canopy humidity.",
        "prevention": "Use certified disease-free seeds. Rotate crops with non-solanaceous plants.",
        "treatment": "Copper-based bactericides combined with Mancozeb to break copper resistance.",
        "natural_treatment": "Remove severely affected leaves. Apply an organic copper-based bactericide. Avoid working in the field when plants are wet to prevent mechanical spreading of the bacteria.",
        "fatality": "Moderate: Causes cosmetic fruit blemishes making them unmarketable, and gradual leaf drop.",
        "dosage_rate_per_acre_ml": 600,
        "ref_source": "University of Florida IFAS Extension",
        "ref_url": "https://edis.ifas.ufl.edu/publication/PP200"
    },
    "Tomato___Leaf_Mold": {
        "common": "Leaf Mold",
        "pathogen": "Passalora fulva",
        "risk_params": {"temp": (18, 27), "hum": 85},
        "vulnerable_stage": "Vegetative",
        "impact_factors": {"visual": 0.6, "env": 0.4}, 
        "visual_cues": [
            "Pale green or yellow spots on the upper surface of older leaves.",
            "Olive-green to brown velvety mold on the corresponding lower surface.",
            "Leaves curl, wither, and drop."
        ],
        "infection_location": "Older leaves first, typically in dense canopies.",
        "why": "Fungus thrives in high relative humidity, typical of greenhouse or high-tunnel environments.",
        "prevention": "Improve ventilation/pruning to reduce canopy humidity below 85%.",
        "treatment": "Chlorothalonil or Potassium bicarbonate for organic setups.",
        "natural_treatment": "Aggressively prune lower leaves to increase airflow. Apply Potassium bicarbonate or organic Neem oil. Reduce greenhouse humidity.",
        "fatality": "Low to Moderate: Primarily affects foliage, reducing photosynthetic capacity.",
        "dosage_rate_per_acre_ml": 450,
        "ref_source": "University of Minnesota Extension",
        "ref_url": "https://extension.umn.edu/disease-management/tomato-leaf-mold"
    },
    "Tomato___Septoria_leaf_spot": {
        "common": "Septoria Leaf Spot",
        "pathogen": "Septoria lycopersici",
        "risk_params": {"temp": (20, 28), "hum": 75},
        "vulnerable_stage": "Vegetative",
        "impact_factors": {"visual": 0.8, "env": 0.2},
        "visual_cues": [
            "Numerous small, circular spots with dark borders and gray/tan centers.",
            "Tiny black specks (pycnidia) often visible in the center of the spots.",
            "Heavily infected leaves turn yellow and drop."
        ],
        "infection_location": "Lower leaves first; spreads upward rapidly.",
        "why": "Fruiting bodies (pycnidia) release spores during extended periods of leaf wetness, spreading from the bottom leaves upward.",
        "prevention": "Remove crop debris at the end of the season. Implement a 3-year crop rotation.",
        "treatment": "Fungicides containing Azoxystrobin or Copper.",
        "natural_treatment": "Apply mulch to prevent soil spores from splashing up during rain. Remove infected lower leaves. Treat with Bacillus subtilis (a biological fungicide) or organic copper sprays.",
        "fatality": "Moderate: Causes rapid defoliation but does not directly infect the fruit.",
        "dosage_rate_per_acre_ml": 550,
        "ref_source": "Missouri Botanical Garden",
        "ref_url": "https://www.missouribotanicalgarden.org/gardens-gardening/your-garden/help-for-the-home-gardener/advice-tips-resources/pests-and-problems/diseases/fungal-spots/septoria-leaf-spot-of-tomato"
    },
    "Tomato___Spider_mites_Two-spotted_spider_mite": {
        "common": "Spider Mites",
        "pathogen": "Tetranychus urticae",
        "risk_params": {"temp": (25, 38), "hum": 40}, 
        "vulnerable_stage": "Any",
        "impact_factors": {"visual": 0.6, "env": 0.4}, 
        "visual_cues": [
            "Fine stippling or flecking on leaves (looks like tiny light dots).",
            "Leaves appear dull, bronzed, or yellowish.",
            "Fine webbing may be visible on the undersides of leaves or stems."
        ],
        "infection_location": "Usually begins on the underside of leaves.",
        "why": "Hot, dry conditions accelerate the mite life cycle, allowing populations to explode and extract sap from leaves, causing stippling.",
        "prevention": "Maintain adequate soil moisture. Use overhead misting to increase localized humidity.",
        "treatment": "Horticultural oils, Neem oil, or specific miticides (Abamectin).",
        "natural_treatment": "Spray plants forcefully with water to dislodge mites and instantly raise humidity. Introduce predatory mites (Phytoseiulus persimilis) into the crop. Apply insecticidal soap or Neem oil.",
        "fatality": "High: Unchecked populations spin dense webs and kill plants via extreme fluid loss.",
        "dosage_rate_per_acre_ml": 300,
        "ref_source": "Texas A&M AgriLife Extension",
        "ref_url": "https://extensionentomology.tamu.edu/publications/spider-mites/"
    },
    "Tomato___Target_Spot": {
        "common": "Target Spot",
        "pathogen": "Corynespora cassiicola",
        "risk_params": {"temp": (22, 30), "hum": 85},
        "vulnerable_stage": "Fruiting",
        "impact_factors": {"visual": 0.7, "env": 0.3},
        "visual_cues": [
            "Small, brown lesions with a yellow halo.",
            "Lesions expand to form circular spots with light brown centers.",
            "Centers of older lesions may crack or fall out (shot-hole appearance)."
        ],
        "infection_location": "Starts on older leaves; can affect stems and fruit.",
        "why": "Spores infect wet leaves, creating lesions with subtle concentric rings that eventually drop out, leaving 'shot-holes'.",
        "prevention": "Maximize air circulation. Avoid excess nitrogen fertilization which creates dense canopies.",
        "treatment": "Systemic fungicides (Boscalid or Pyraclostrobin).",
        "natural_treatment": "Improve air circulation through aggressive pruning. Avoid excessive nitrogen fertilizers. Apply organic copper-based fungicides as a preventative measure.",
        "fatality": "Moderate: Reduces yield through defoliation and fruit spotting.",
        "dosage_rate_per_acre_ml": 500,
        "ref_source": "NC State Extension",
        "ref_url": "https://content.ces.ncsu.edu/target-spot-of-tomato"
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "common": "Yellow Leaf Curl Virus (TYLCV)",
        "pathogen": "Begomovirus (Vector: Whiteflies)",
        "risk_params": {"temp": (25, 36), "hum": 60},
        "vulnerable_stage": "Seedling",
        "impact_factors": {"visual": 0.9, "env": 0.1}, 
        "visual_cues": [
            "Leaves curl upward and inward (cupping).",
            "Strong yellowing (chlorosis) at the leaf edges and between veins.",
            "Severe stunting of the plant; new leaves are very small."
        ],
        "infection_location": "New growth/Top of the plant.",
        "why": "The virus is transmitted exclusively by the Silverleaf Whitefly. Warm conditions increase vector feeding and reproduction.",
        "prevention": "Use UV-reflective mulches to disorient whiteflies. Use fine-mesh insect netting.",
        "treatment": "No cure for the virus. Apply insecticides (Imidacloprid) to control the whitefly vector.",
        "natural_treatment": "There is no cure. Pull out and destroy infected plants immediately. Control the whitefly vectors by applying Neem oil, using yellow sticky traps, and deploying reflective silver mulch.",
        "fatality": "Extreme: Can cause 100% yield loss if plants are infected before the flowering stage.",
        "dosage_rate_per_acre_ml": 250, 
        "ref_source": "World Vegetable Center (WorldVeg)",
        "ref_url": "https://avrdc.org/tomato-yellow-leaf-curl/"
    },
    "Tomato___Tomato_mosaic_virus": {
        "common": "Tomato Mosaic Virus (ToMV)",
        "pathogen": "Tobamovirus",
        "risk_params": {"temp": (15, 35), "hum": 60}, 
        "vulnerable_stage": "Any",
        "impact_factors": {"visual": 0.9, "env": 0.1}, 
        "visual_cues": [
            "Light and dark green mottled areas (mosaic pattern) on leaves.",
            "Leaves may be distorted, fern-like, or puckered.",
            "Plants may appear stunted with reduced fruit set."
        ],
        "infection_location": "Systemic; affects the entire plant.",
        "why": "A highly stable virus transmitted mechanically (tools, hands, clothing) or via infected seeds. Does not require an insect vector.",
        "prevention": "Strict sanitation. Wash hands with soap/milk. Disinfect pruning tools with 10% bleach.",
        "treatment": "None. Infected plants must be uprooted and burned immediately.",
        "natural_treatment": "There is no cure. Pull out and destroy infected plants immediately to save the rest of the crop. Thoroughly wash hands with soap or milk, and disinfect all pruning tools with a 10% bleach solution.",
        "fatality": "High: Causes severe stunting, leaf mottling, and unmarketable distorted fruit.",
        "dosage_rate_per_acre_ml": 0,
        "ref_source": "Penn State Extension",
        "ref_url": "https://extension.psu.edu/tomato-mosaic-virus"
    },
    "Tomato___healthy": {
        "common": "Healthy Plant",
        "pathogen": "None",
        "risk_params": {"temp": (18, 28), "hum": 60},
        "vulnerable_stage": "Any",
        "impact_factors": {"visual": 0.9, "env": 0.1},
        "visual_cues": [
            "Even green coloration across the leaf surface.",
            "No holes, spots, webbing, or structural distortion.",
            "Vigorous growth appropriate for the crop stage."
        ],
        "infection_location": "N/A",
        "why": "Visual features show uniform chlorophyll distribution, no necrotic lesions, and absence of pest damage.",
        "prevention": "Maintain current Integrated Pest Management (IPM) practices.",
        "treatment": "Maintain current irrigation, pruning, and nutrient schedule.",
        "natural_treatment": "Maintain current organic practices. Ensure consistent watering at the base of the plant, provide adequate spacing for airflow, and apply compost tea to boost natural immunity.",
        "fatality": "N/A",
        "dosage_rate_per_acre_ml": 0,
        "ref_source": "FAO Agricultural Standards",
        "ref_url": "https://www.fao.org/land-water/databases-software/cropwat/en/"
    }
}

def get_risk_assessment(disease, temp, humidity):
    """Logic for Disease-specific weather risk mapping."""
    data = DISEASE_KB.get(disease)
    if not data: return "Normal", 0
    
    score = 0
    if data["risk_params"]["temp"][0] <= temp <= data["risk_params"]["temp"][1]:
        score += 50
        
    hum_val = data["risk_params"]["hum"]
    if isinstance(hum_val, tuple):
        if hum_val[0] <= humidity <= hum_val[1]: score += 50
    else:
        # Adjusted logic for spider mites which prefer LOW humidity
        if disease == "Tomato___Spider_mites_Two-spotted_spider_mite":
             if humidity <= hum_val: score += 50
        elif humidity >= hum_val: score += 50
        
    status = "Critical" if score >= 100 else "Warning" if score >= 50 else "Stable"
    return status, score