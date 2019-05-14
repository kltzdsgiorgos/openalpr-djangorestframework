import sys
import cv2 as cv
from openalpr import Alpr
# import geocoder
# import datetime
import requests

WINDOW_NAME = 'openalpr'

r = requests.get("http://licenceplatebrowser.herokuapp.com/plates/")
data = r.json()
data = data['results']
print(r.status_code)


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

    # g = geocoder.ipinfo('me')
    alpr.set_top_n(20)
    alpr.set_default_region("gr")

    while True:

        ret_val, frame = cap.read()
        frame = cv.flip(frame, 1) # we use flip because the video from android cam is mirrored
        if not ret_val:
            print('VideoCapture.read() failed. Exiting...')
            break

        cv.imshow(WINDOW_NAME, frame)
        results = alpr.recognize_ndarray(frame)

        if cv.waitKey(1) == 27:
            break

        for _ in data:
            for plate in results['results']:
                # print(plate['plate']) # uncomment to display all found plates
                if _['plate'] == plate['plate']:
                    print("Car with Licence Plate:", _['plate'])
                    if _['insurance'] is True:
                        print("INSURED")
                    else:
                        print("NOT INSURED")
                    if _['stolen'] is True:
                        print("STOLEN")

    cv.destroyAllWindows()
    cap.release()
    alpr.unload()


if __name__ == "__main__":
    main()
