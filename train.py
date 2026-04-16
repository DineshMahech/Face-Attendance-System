import cv2
import numpy as np
from PIL import Image
import os

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    faces = []
    ids = []

    for imagePath in imagePaths:
        # Skip non-image files
        if not imagePath.endswith(('.jpg', '.png', '.jpeg')):
            continue

        try:
            pilImage = Image.open(imagePath).convert('L')  # convert to grayscale
            imageNp = np.array(pilImage, 'uint8')

            # Extract ID from filename: name.ID.sample.jpg
            Id = int(os.path.split(imagePath)[-1].split(".")[1])

            faces.append(imageNp)
            ids.append(Id)

        except Exception as e:
            print(f"Skipping file {imagePath} due to error: {e}")

    return faces, ids


def train_model():
    print("Training started...")

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces, ids = getImagesAndLabels('TrainingImage')

    if len(faces) == 0:
        print("No images found for training!")
        return

    recognizer.train(faces, np.array(ids))

    os.makedirs("TrainingImageLabel", exist_ok=True)
    recognizer.save('TrainingImageLabel/Trainer.yml')

    print("Training Completed Successfully")
    print(f"Total faces trained: {len(faces)}")


# ===== RUN PROGRAM =====
if __name__ == "__main__":
    train_model()