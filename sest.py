import cv2
import numpy as np
from ultralytics import YOLO
import os

class CoffeeDiseaseDetector:
    def __init__(self, model_path='sest.pt'):
        """
        Initialize the Coffee Disease Detector with a YOLOv8 model.
        
        Args:
            model_path (str): Path to the YOLOv8 model weights file (.pt)
        """
        self.model = YOLO(model_path)
        self.class_names = ['enfermo', 'sano']  # Update with your actual class names
        
    def detect(self, image_path, conf_threshold=0.5):
        """
        Detect coffee diseases in an image.
        
        Args:
            image_path (str): Path to the input image
            conf_threshold (float): Confidence threshold for detections
            
        Returns:
            tuple: (image with detections, results)
        """
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image at {image_path}")
            
        # Run inference
        results = self.model(image, conf=conf_threshold)
        
        # Process results
        for result in results:
            boxes = result.boxes.cpu().numpy()
            for box in boxes:
                # Get box coordinates
                x1, y1, x2, y2 = box.xyxy[0].astype(int)
                
                # Get class and confidence
                cls_id = int(box.cls[0])
                conf = box.conf[0]
                
                # Draw bounding box and label
                label = f"{self.class_names[cls_id]} {conf:.2f}"
                color = (0, 255, 0) if cls_id == 1 else (0, 0, 255)  # Green for healthy, Red for diseased
                
                cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                cv2.putText(image, label, (x1, y1 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        return image, results

def main():
    # Initialize detector
    detector = CoffeeDiseaseDetector()
    
    # Example usage
    input_image = "test_image.jpg"  # Replace with your test image
    output_image = "result.jpg"
    
    try:
        # Detect diseases
        result_img, _ = detector.detect(input_image)
        
        # Save the result
        cv2.imwrite(output_image, result_img)
        print(f"Detection complete. Result saved to {output_image}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
