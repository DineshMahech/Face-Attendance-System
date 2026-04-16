import cv2
import pandas as pd
from datetime import datetime
import os

def recognize_faces():
    print("Starting Recognition...")

    # Load trained model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel/Trainer.yml")

    # Load Haarcascade
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    # Check Employee file
    emp_file = "EmployeeDetails/EmployeeDetails.csv"
    if not os.path.isfile(emp_file):
        print("EmployeeDetails.csv not found! Run capture.py first.")
        return

    df = pd.read_csv(emp_file)

    # Start camera
    cam = cv2.VideoCapture(0)

    os.makedirs("Attendance", exist_ok=True)
    att_file = "Attendance/Attendance.csv"

    marked = set()

    while True:
        ret, im = cam.read()
        if not ret:
            print("Camera error")
            break

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 6)

        for (x, y, w, h) in faces:
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])

            # Check recognition
            if conf < 50 and Id in df['ID'].values:
                name = df.loc[df['ID'] == Id]['Name'].values[0]
            else:
                name = "Unknown"

            # Mark attendance only once
            if name != "Unknown" and name not in marked:
                marked.add(name)

                now = datetime.now()
                data = [[Id, name, now.strftime("%Y-%m-%d %H:%M:%S")]]

                df_att = pd.DataFrame(data, columns=["ID", "Name", "DateTime"])

                if not os.path.isfile(att_file):
                    df_att.to_csv(att_file, index=False)
                else:
                    df_att.to_csv(att_file, mode='a', header=False, index=False)

                print(f"Attendance marked for {name}")

            # Draw rectangle and name
            cv2.rectangle(im, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(im, name, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Face Recognition', im)

        # Press ESC to exit
        key = cv2.waitKey(10) & 0xFF
        
        if key == 27 or key == ord('q'):
            print("Closing camera...")
            break

    #  Proper closing
    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    recognize_faces()
