import cv2
import numpy as np

class AdvancedImageValidator:
    """
    Defensive Software Engineering Layer.
    Uses physics, lighting, and morphological heuristics to prevent 'Garbage-In, Garbage-Out'.
    """
    
    # --- Scientific Validation Thresholds ---
    IMAGE_BLUR_THRESHOLD = 40.0      # Variance of Laplacian for sharpness
    MIN_RMS_CONTRAST = 20.0          # Root Mean Square contrast
    MIN_MEAN_BRIGHTNESS = 40         # Average pixel intensity
    MAX_GLARE_PERCENTAGE = 0.05      # Clipping threshold (5% max)
    MIN_BIOLOGICAL_AREA = 15.0       # Minimal required HSV mask coverage
    MIN_RESOLUTION = 224             # Standard input size for MobileNetV2
    
    @staticmethod
    def calculate_rms_contrast(gray_img):
        """Calculates global contrast to detect foggy or washed-out images."""
        return gray_img.std()

    @staticmethod
    def validate(image_array):
        """
        Executes a 6-tier quality check. 
        Returns (Bool, String Message).
        """
        try:
            # Check 0: Resolution Check 
            h, w = image_array.shape[:2]
            if h < AdvancedImageValidator.MIN_RESOLUTION or w < AdvancedImageValidator.MIN_RESOLUTION:
                return False, f"Resolution too low ({w}x{h}). The AI requires at least 224x224 pixels."

            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            total_pixels = gray.shape[0] * gray.shape[1]
            
            # --- Tier 1: Sharpness & Focus ---
            focus_measure = cv2.Laplacian(gray, cv2.CV_64F).var()
            if focus_measure < AdvancedImageValidator.IMAGE_BLUR_THRESHOLD:
                return False, "Motion Blur Detected. **Pro-Tip:** Stabilize your camera or use a tripod."
                
            # --- Tier 2: Exposure & Brightness ---
            mean_brightness = np.mean(gray)
            if mean_brightness < AdvancedImageValidator.MIN_MEAN_BRIGHTNESS:
                return False, "Image too dark. **Pro-Tip:** Move out of the shade. Indirect sunlight or a flashlight will boost contrast."
                
            # --- Tier 3: Contrast & Clarity ---
            contrast = AdvancedImageValidator.calculate_rms_contrast(gray)
            if contrast < AdvancedImageValidator.MIN_RMS_CONTRAST:
                return False, "Low Contrast. **Pro-Tip:** Place the leaf on a solid white piece of paper to help the AI isolate features."
                
            # --- Tier 4: Specular Reflection (Glare) ---
            # Glare creates 'white holes' in data that hide disease spots
            white_pixels = np.sum(gray > 240)
            if (white_pixels / total_pixels) > AdvancedImageValidator.MAX_GLARE_PERCENTAGE:
                return False, "Severe Sun Glare. **Pro-Tip:** Shade the leaf with your hand to remove harsh reflections."
                
            # --- Tier 5: Biological Content (HSV Segmentation) ---
            hsv_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2HSV)
            
            # Masks for Green (Healthy), Yellow (Chlorosis), and Brown (Necrosis)
            lower_green_yellow = np.array([20, 40, 40])
            upper_green_yellow = np.array([90, 255, 255])
            lower_brown = np.array([10, 50, 20])
            upper_brown = np.array([20, 255, 200])
            
            mask_gy = cv2.inRange(hsv_image, lower_green_yellow, upper_green_yellow)
            mask_br = cv2.inRange(hsv_image, lower_brown, upper_brown)
            biological_mask = cv2.bitwise_or(mask_gy, mask_br)
            
            bio_percent = (cv2.countNonZero(biological_mask) / total_pixels) * 100
            
            if bio_percent < AdvancedImageValidator.MIN_BIOLOGICAL_AREA:
                return False, f"Invalid Specimen (Only {bio_percent:.1f}% plant matter). **Pro-Tip:** Zoom in closer to the leaf."

            # --- Final Approval ---
            return True, "Quality Optimal for Neural Analysis."
            
        except Exception as e:
            return False, f"Validator System Error: {str(e)}"