import face_recognition
import cv2

# Load your image (the one you want to recognize)
known_image = face_recognition.load_image_file("face.png")

# Encode the known image
known_face_encoding = face_recognition.face_encodings(known_image)[0]

# Create arrays of known face encodings and corresponding labels
known_face_encodings = [known_face_encoding]
known_face_labels = ["Seli"]

# Open the webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Capture each frame from the webcam
    ret, frame = video_capture.read()

    # Find all face locations and face encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop through each face found in the frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check if the face matches any known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # If a match is found, use the label of the known face
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_labels[first_match_index]

            # Display welcome message
            cv2.putText(frame, f"Welcome {name}!", (left + 6, top - 10),
                        cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)

            # Auto-capture: Save the image when a match is found
            cv2.imwrite(f"{name}_captured.jpg", frame)

    # Draw a rectangle around the face
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
video_capture.release()
cv2.destroyAllWindows()


