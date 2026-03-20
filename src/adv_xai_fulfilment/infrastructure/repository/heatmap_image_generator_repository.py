import cv2
import uuid
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from YOLOv8_Explainer import yolov8_heatmap

from logger import get_logger

logger = get_logger()


class HeatmapImageGeneratorRepository:
    def generate(self, image_path: str, model_path: str) -> str:
        """
        Generate and save a heatmap visualization for YOLOv8 predictions
        and return file path of the generated heatmap image.
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image from {image_path}")

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Init heatmap generator
        heatmap_generator = yolov8_heatmap(
            weight=model_path,
            method="EigenGradCAM",
            layer=[12, 17, 21],
            conf_threshold=0.01,
            show_box=True,
            renormalize=False,
        )

        logger.debug("Heatmap generator initialized successfully.")

        # Generate heatmap
        logger.debug("Generating heatmap...")
        heatmap_image = heatmap_generator.process(image_path)

        if heatmap_image is None:
            raise ValueError("Heatmap generator returned None")

        logger.debug(f"Raw heatmap type: {type(heatmap_image)}")

        heatmap = self._ensure_numpy_image(heatmap_image)

        logger.debug(
            f"Final heatmap shape: {heatmap.shape}, dtype: {heatmap.dtype}"
        )

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

        # Se era PIL → salva diretto
        if isinstance(heatmap_image, Image.Image):
            heatmap_image.save(heatmap_image_path)
        else:
            Image.fromarray(heatmap).save(heatmap_image_path)

        logger.debug("Heatmap generated successfully!")

        return heatmap_image_path
    
    def _ensure_numpy_image(self, data):
        """
        Ensure data is a valid numpy image (H, W, C) uint8.
        Try smart conversions before failing.
        """
        # Caso 1: PIL Image → converti
        if isinstance(data, Image.Image):
            logger.debug("Converting PIL Image to numpy array")
            data = data.convert("RGB")
            return np.asarray(data, dtype=np.uint8)

        # Caso 2: già numpy
        if isinstance(data, np.ndarray):
            if data.dtype == object:
                raise TypeError("Numpy array has dtype=object, invalid image")

            # Se float → normalizza
            if np.issubdtype(data.dtype, np.floating):
                logger.debug("Converting float image to uint8")
                data = np.clip(data * 255, 0, 255).astype(np.uint8)

            # Se grayscale → espandi a 3 canali
            if len(data.shape) == 2:
                logger.debug("Expanding grayscale to RGB")
                data = np.stack([data] * 3, axis=-1)

            return data

        # Caso 3: lista → prova conversione
        if isinstance(data, list):
            logger.debug("Attempting to convert list to numpy array")
            try:
                return self._ensure_numpy_image(np.array(data))
            except Exception as e:
                raise TypeError(f"Cannot convert list to image: {e}")

        # Caso fallback → KO
        raise TypeError(f"Unsupported heatmap type: {type(data)}")