import cv2

print("type 'q' to quit...")

img = cv2.imread("img111.jpg")
cv2.namedWindow("Test", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Test", 1078, 800)
cv2.moveWindow("Test", 0, 0)
cv2.imshow("Test", img)

while True:

	key = cv2.waitKeyEx()

	if key != -1:
		print(key)

	if key == ord('q'):
		break
