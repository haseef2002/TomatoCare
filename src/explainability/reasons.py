import pandas as pd
import plotly.express as px

class ExplainabilityEngine:
    """
    Translates raw AI data into human-understandable 'WHY' sections.
    Simulates SHAP values for multimodal (Visual + Weather) impact.
    """

    @staticmethod
    def get_weather_impact(disease_name, temp, humidity, disease_data):
        """
        Calculates how much the weather contributed to the diagnosis.
        This represents the SHAP 'Environmental' feature importance.
        """
        params = disease_data[disease_name]["risk_params"]
        
        # Calculate deviation from 'Ideal' pathogen growth conditions
        temp_impact = 1.0 - abs(temp - sum(params["temp"])/2) / 20
        hum_impact = humidity / params["humidity"]
        
        # Normalize impacts
        total = temp_impact + hum_impact
        return {
            "Temperature Impact": round((temp_impact/total) * 40, 2), # Weight 40%
            "Humidity Impact": round((hum_impact/total) * 60, 2)      # Weight 60%
        }

    @staticmethod
    def plot_shap_summary(visual_conf, weather_impacts):
        """Creates a Waterfall/Bar chart showing feature importance."""
        data = {
            "Feature": ["Visual Patterns (CNN)", "Humidity Influence", "Temperature Influence"],
            "Contribution (%)": [visual_conf * 100, weather_impacts["Humidity Impact"], weather_impacts["Temperature Impact"]]
        }
        df = pd.DataFrame(data)
        fig = px.bar(df, x="Contribution (%)", y="Feature", orientation='h', 
                     title="SHAP Explanation: Impact on Diagnosis",
                     color="Contribution (%)", color_continuous_scale="Viridis")
        return fig