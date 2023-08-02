import cv2
from PIL import Image
import numpy as np
from torchvision.transforms import transforms



def loadImage(imageBytes):
    image = np.frombuffer(imageBytes, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def processingImage(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, (256, 256), interpolation=cv2.INTER_AREA)
    image = cv2.GaussianBlur(image, (5, 5), 0)
    image = cv2.convertScaleAbs(image, alpha=1.5, beta=30)

    image = Image.fromarray(np.uint8(image))
    return image


def cvImageToTorch(imageBytes):
    image = loadImage(imageBytes)
    image = processingImage(image)
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=[0.5], std=[0.5])])
    image = transform(image)
    image = image.unsqueeze(0).float()
    return image
