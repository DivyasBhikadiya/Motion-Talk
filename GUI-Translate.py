from keras.models import load_model
import cv2
import numpy as np
import keyboard

REV_CLASS_MAP = {}
c = 0
for i in range(65, 91):
    REV_CLASS_MAP[c] = chr(i)
    c += 1
REV_CLASS_MAP[26] = 'none'
print(REV_CLASS_MAP)

def mapper(val):
    return REV_CLASS_MAP[val]

model = load_model("asl-model2.h5")

cap = cv2.VideoCapture(0)

text_msg = ''

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    cv2.rectangle(frame, (50, 50), (250, 250), (255, 255, 255), 2)
    f = open("output.txt", mode='w', encoding='utf-8')
    f.write(text_msg)
            

    # extract the region of image within the user rectangle
    roi = frame[50:250, 50:250]
    img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (227, 227))

    # predict the move made
    pred = model.predict(np.array([img]))
    sign_code = np.argmax(pred[0])
    sign_name = mapper(sign_code)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Your Sign: " + sign_name,
                (50, 50), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.putText(frame, "Text Message: " + text_msg,
                (750, 50), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("ASL Sign to Text", frame)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break
    if keyboard.is_pressed('b'):
        if sign_name != 'none':
            text_msg += sign_name
            print('b Key was pressed')
        else:
            print('none was captured, so ignored')

f.close()
cap.release()
cv2.destroyAllWindows()