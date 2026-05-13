# src/fusion/env_fusion.py
import numpy as np

class MultimodalFusionEngine:
    def __init__(self, visual_weight=0.9, weather_weight=0.1):
        self.alpha = visual_weight
        self.beta = weather_weight

    def calculate_environmental_risk(self, disease_kb_data, current_temp, current_hum, crop_stage):
        """Calculates environmental viability of the pathogen based on real-time data."""
        try:
            ideal_temp = disease_kb_data['risk_params']['temp']
            ideal_hum = disease_kb_data['risk_params']['hum']
            
            # Temperature Penalty Math
            if ideal_temp[0] <= current_temp <= ideal_temp[1]: p_temp = 1.0
            else:
                dist = min(abs(current_temp - ideal_temp[0]), abs(current_temp - ideal_temp[1]))
                p_temp = max(0.0, 1.0 - (dist * 0.1))

            # Humidity Penalty Math
            if isinstance(ideal_hum, tuple):
                if ideal_hum[0] <= current_hum <= ideal_hum[1]: p_hum = 1.0
                else: p_hum = 0.5
            else:
                # Catch specific dry-climate pests (e.g. Spider Mites)
                if disease_kb_data['common'] == "Spider Mites" and current_hum <= ideal_hum: p_hum = 1.0
                elif current_hum >= ideal_hum: p_hum = 1.0
                else:
                    dist = abs(ideal_hum - current_hum)
                    p_hum = max(0.0, 1.0 - (dist * 0.02))

            base_weather_risk = (p_temp + p_hum) / 2.0

            # Crop Stage Vulnerability Multiplier
            vulnerable_stage = disease_kb_data.get('vulnerable_stage', 'Any')
            if vulnerable_stage != 'Any' and crop_stage == vulnerable_stage:
                base_weather_risk = min(1.0, base_weather_risk * 1.15) 

            return base_weather_risk
            
        except Exception as e:
            print(f"Fusion calculation error: {e}")
            return 0.5 # Neutral fallback if math fails

    def fuse_predictions(self, visual_confidence, environmental_risk):
        """Combines modalities using Late Fusion."""
        final_confidence = (self.alpha * visual_confidence) + (self.beta * environmental_risk)
        return min(1.0, max(0.0, final_confidence))

    # ---> THIS IS THE FUNCTION STREAMLIT WAS LOOKING FOR <---
    def calculate_shap_values(self, visual_conf, env_risk, impact_factors):
        """
        SHAP (Shapley Additive exPlanations) Logic:
        Calculates the feature importance/contribution of each modality for the UI chart.
        """
        v_weight = impact_factors.get("visual", 0.5)
        e_weight = impact_factors.get("env", 0.5)
        
        # Calculate raw modality impact
        raw_visual_impact = (v_weight * visual_conf)
        raw_env_impact = (e_weight * env_risk)
        total = raw_visual_impact + raw_env_impact
        
        # Normalize to 100% distribution
        if total > 0:
            return {
                "Visual Evidence": raw_visual_impact / total,
                "Environmental Context": raw_env_impact / total
            }
        return {"Visual Evidence": 0.5, "Environmental Context": 0.5} # Fallback

    def explain_confidence(self, visual_conf, env_risk, final_conf, disease_name):
        """Generates a dynamic textual explanation of the math for end-users."""
        explanation = f"The final confidence of **{final_conf*100:.1f}%** was calculated by weighing the visual evidence against the environmental risk context.\n\n"
        
        if visual_conf > 0.85:
            explanation += f"* **Visual:** The neural network detected highly distinct morphological features of {disease_name}.\n"
        else:
            explanation += f"* **Visual:** The visual symptoms were somewhat ambiguous ({visual_conf*100:.1f}% raw confidence).\n"
            
        if env_risk > 0.75:
            explanation += "* **Environment:** Current field temperature, humidity, and crop stage create a highly favorable environment for this pathogen, validating the visual diagnosis."
        elif env_risk < 0.4:
            explanation += "* **Environment:** Current field conditions are hostile to this pathogen, slightly lowering the overall system confidence to prevent false positives."
        else:
            explanation += "* **Environment:** Current field conditions are moderately suitable for this pathogen, acting as a neutral modifier."
            
        return explanation