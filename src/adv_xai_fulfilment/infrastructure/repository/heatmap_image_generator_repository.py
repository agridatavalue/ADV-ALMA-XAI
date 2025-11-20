import cv2
import uuid
import numpy as np
import matplotlib.pyplot as plt
from YOLOv8_Explainer import yolov8_heatmap

from logger import get_logger

logger = get_logger()

class HeatmapImageGeneratorRepository:
    def generate(self, image_path: str, model_path: str) -> str:
        """
        Generate and save a heatmap visualization for YOLOv8 predictions and
        return file path of the generated heatmap image.
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image from {image_path}")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Initialize the heatmap generator
        heatmap_generator = yolov8_heatmap(
            weight=model_path,
            method="EigenGradCAM",
            layer=[12, 17, 21],
            conf_threshold=0.25,
            show_box=True,
            renormalize=False,
        )
        logger.debug("Heatmap generator initialized successfully.")  # Debugging

        # Generate heatmap using process method
        logger.debug("Generating heatmap...")
        heatmap_image = heatmap_generator.process(image_path)

        logger.debug("Heatmap generated successfully!")
        # Convert PIL Image to numpy array
        heatmap = np.array(heatmap_image)

        # Create visualization
        plt.figure(figsize=(15, 5))

        # Original image
        plt.subplot(1, 3, 1)
        plt.imshow(image)
        plt.title("Original Image (Crop vs Weed)")
        plt.axis("off")

        # Heatmap visualization
        plt.subplot(1, 3, 2)
        plt.imshow(heatmap)
        plt.title("Model Attribution Heatmap")
        plt.axis("off")

        # Overlay
        plt.subplot(1, 3, 3)
        plt.imshow(image)
        plt.imshow(heatmap, alpha=0.5)
        plt.title("Heatmap Overlay")
        plt.axis("off")

        plt.tight_layout()
        output_path = f"/tmp/heatmap_{uuid.uuid4().hex}.png"
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        # Save the raw heatmap image as well
        file_extension = image_path.split(".")[-1]
        heatmap_image_path = image_path.replace(
            f".{file_extension}", f"_heatmap.{file_extension}"
        )
        heatmap_image.save(heatmap_image_path) # type: ignore

        logger.debug("Heatmap generated successfully!")
        return heatmap_image_path
