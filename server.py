from flask import Flask, request
import cv2
import numpy as np
from google_drive_upload import upload_to_drive  # Import Google Drive upload function

app = Flask(__name__)


def segment_and_crop_leaves(image):
    """Apply color-based segmentation to extract and crop leaves."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([25, 40, 40])  # Adjust based on leaf color
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    result = cv2.bitwise_and(image, image, mask=mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cropped_leaves = [image[y:y + h, x:x + w] for (x, y, w, h) in [cv2.boundingRect(cnt) for cnt in contours]]

    return cropped_leaves


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    cropped_leaves = segment_and_crop_leaves(image)

    for leaf in cropped_leaves:
        upload_to_drive(leaf)  # Upload each cropped leaf to Google Drive

    return {"status": "success", "message": "Images processed and uploaded"}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
