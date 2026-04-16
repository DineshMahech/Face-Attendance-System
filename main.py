# ==========================================
# FACE RECOGNITION ATTENDANCE SYSTEM
#
# 1. Register Student (Capture Images)
# 2. Train Model
# 3. Start Attendance (Face Recognition)
# 4. Delete Employee
# 5. Exit
#
# FLOW:
# Capture → Train → Recognize → Attendance Saved
#
# TECHNOLOGY USED:
# - OpenCV (Face Detection)
# - LBPH Algorithm (Face Recognition)
# - Pandas (CSV Handling)
# ==========================================


from capture import capture_images
from train import train_model
from recognize import recognize_faces

import os
import pandas as pd


# FUNCTION: DELETE EMPLOYEE
def delete_employee(Id):
    file_path = "EmployeeDetails/EmployeeDetails.csv"

    # Check if file exists
    if not os.path.isfile(file_path):
        print(" No employee data found!")
        return

    df = pd.read_csv(file_path)

    # Check if ID exists
    if int(Id) not in df["ID"].values:
        print(" ID not found!")
        return

    # Get employee name
    name = df.loc[df["ID"] == int(Id)]["Name"].values[0]

    # Remove from CSV
    df = df[df["ID"] != int(Id)]
    df.to_csv(file_path, index=False)

    # Remove images
    for file in os.listdir("TrainingImage"):
        try:
            if file.split(".")[1] == str(Id):
                os.remove(os.path.join("TrainingImage", file))
        except:
            continue

    print(f" {name} deleted successfully!")
    print(" Please run training again to update model!")


# MAIN MENU FUNCTION

def main():
    while True:
        print("\n===== FACE ATTENDANCE SYSTEM =====")
        print("1. Register Student (Capture Images)")
        print("2. Train Model")
        print("3. Start Attendance")
        print("4. Delete Employee")
        print("5. Exit")

        choice = input("Enter your choice: ")

        # Option 1: Capture Images
        if choice == "1":
            Id = input("Enter ID: ")
            name = input("Enter Name: ")
            capture_images(Id, name)

        # Option 2: Train Model
        elif choice == "2":
            train_model()

        # Option 3: Start Recognition
        elif choice == "3":
            recognize_faces()

        # Option 4: Delete Employee
        elif choice == "4":
            Id = input("Enter ID to delete: ")
            delete_employee(Id)

        # Option 5: Exit Program
        elif choice == "5":
            print("Exiting system...")
            break

        else:
            print(" Invalid choice! Try again.")


# PROGRAM START
if __name__ == "__main__":
    main()

