import cv2
import numpy as np
import mediapipe as mp

mp_draw = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

source = "/home/douw.vanniekerk/development/RebelwayAppliedMLDouw.git/computer_vision/mediapipe/dance.mp4"

cap = cv2.VideoCapture(source)

# Get frame properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 30 # Adjust based on your camera

# Define codec and create VideoWriter (MP4 compatible)
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # MPEG-4 codec
out = cv2.VideoWriter('output_dance.mp4', fourcc, fps, (frame_width, frame_height))

with mp_pose.Pose(min_detection_confidence=0.9, min_tracking_confidence=0.9) as pose:
	while cap.isOpened():
		ret, image = cap.read()

		if ret:
			image.flags.writeable = False
			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			results = pose.process(image)

			image.flags.writeable = True

			image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
			mp_draw.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
									landmark_drawing_spec=mp_styles.get_default_pose_landmarks_style())

			print(results.pose_landmarks)

			out.write(image) # Save frame

			cv2.imshow("Pose", image)





			if cv2.waitKey(5) == ord('q'):
				break

		else:
			break

cap.release()
cv2.destroyAllWindows()					