import cv2
import os
import pandas as pd

def capture_images(Id, name):
    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    sampleNum = 0

    os.makedirs("TrainingImage", exist_ok=True)
    os.makedirs("EmployeeDetails", exist_ok=True)

    while True:
        ret, img = cam.read()
        if not ret:
            print("Camera not working")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            sampleNum += 1

            # Save face image
            cv2.imwrite(f"TrainingImage/{name}.{Id}.{sampleNum}.jpg",
                        gray[y:y+h, x:x+w])

            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        cv2.imshow('Capture Images', img)

        # Stop after 40 images or press 'q'
        if cv2.waitKey(1) == ord('q') or sampleNum >= 40:
            break

    cam.release()
    cv2.destroyAllWindows()

    # Save ID and Name properly (NO ERROR FUTURE)
    file_path = "EmployeeDetails/EmployeeDetails.csv"

    df = pd.DataFrame([[int(Id), name]], columns=["ID", "Name"])

    # Check if file exists
    if not os.path.isfile(file_path):
        df.to_csv(file_path, index=False)
    else:
        existing = pd.read_csv(file_path)

        # Prevent duplicate ID
        if int(Id) in existing["ID"].values:
            print("ID already exists! Try different ID.")
            return

        df.to_csv(file_path, mode='a', header=False, index=False)

    print(f"Images Saved for {name} with ID {Id}")


# ===== RUN PROGRAM =====
if __name__ == "__main__":
    Id = input("Enter ID: ")
    name = input("Enter Name: ")

    capture_images(Id, name)