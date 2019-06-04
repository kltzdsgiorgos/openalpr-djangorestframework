import sys
import cv2 as cv
from openalpr import Alpr
import sqlite3

WINDOW_NAME = 'LicencePlate'
conn = sqlite3.connect('plates.db')
c = conn.cursor()


def main():
    cap = cv.VideoCapture(-1)
    if not cap.isOpened():
        sys.exit('Failed to open Camera/Video File')

    cv.namedWindow(WINDOW_NAME, cv.WINDOW_AUTOSIZE)
    cv.setWindowTitle(WINDOW_NAME, 'OpenALPR')

    alpr = Alpr("eu", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data/")
    if not alpr.is_loaded():
        print('Error loading OpenALPR')
        sys.exit(1)

    alpr.set_top_n(20)
    alpr.set_default_region("gr")

    while True:

        ret_val, frame = cap.read()
        frame = cv.flip(frame, 1)  # we use flip because the video from android cam is mirrored
        if not ret_val:
            print('VideoCapture failed. Exiting...')
            break

        cv.imshow(WINDOW_NAME, frame)
        results = alpr.recognize_ndarray(frame)

        for plate in results['results']:
            item = plate['plate']
            c.execute("SELECT * FROM plates WHERE PlateNumber = (?)", (item,))
            x = c.fetchone()
            if x != None:
                print(f"Car with Plate {x[0]} INSURED:{x[1]} STOLEN:{x[2]}")

        if cv.waitKey(1) == 27:
            break

    cv.destroyAllWindows()
    cap.release()
    alpr.unload()


if __name__ == "__main__":
    main()
