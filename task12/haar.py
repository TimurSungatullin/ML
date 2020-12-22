import cv2


def fit(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.IMREAD_GRAYSCALE)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_eye.xml')
    cv2.imwrite('result.jpg', image)
    faces = face_cascade.detectMultiScale(
        gray.copy(),
        scaleFactor=1.15,
        minNeighbors=3,
        minSize=(30, 30),
    )
    return faces, eye_cascade, image, gray


def save(faces, eye_cascade, file_name, image, gray):
    for index, (x, y, w, h) in enumerate(faces):
        image_gray = gray[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(image_gray)
        if len(eyes) > 0:
            # Глаза есть, отмечаем зеленым
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            # Нет глаз у лица, отметим другим цветом (Тёмно-зелёный)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 100, 0), 2)

    cv2.imwrite(f'result_{file_name}.png', image)


def main():
    for file_name in ['test.png', 'test1.png', 'test2.png', 'test3.png']:
        faces, eye_cascade, image, gray = fit(file_name)
        save(faces, eye_cascade, file_name, image, gray)


if __name__ == '__main__':
    main()
