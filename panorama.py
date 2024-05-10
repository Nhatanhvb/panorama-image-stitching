import cv2
import numpy as np

image1 = cv2.imread(r'C:\Users\nhata\Desktop\pano\z5383940696177_53f14e83a0d0168040256590d0379f0e.jpg')
image2 = cv2.imread(r'C:\Users\nhata\Desktop\pano\z5383940892486_000b2015b1b9d52eed80f92442801777.jpg')


# Convert the images to grayscale
gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

# Create a SIFT object
sift = cv2.SIFT_create()

# Detect keypoints and compute descriptors
keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

# Match keypoints
matcher = cv2.BFMatcher()
matches = matcher.match(descriptors1, descriptors2)

# Sort matches by distance
matches = sorted(matches, key=lambda x: x.distance)

# Select top matches
top_matches = matches[:50]

# Extract keypoints from top matches
src_points = np.float32([keypoints1[m.queryIdx].pt for m in top_matches]).reshape(-1, 1, 2)
dst_points = np.float32([keypoints2[m.trainIdx].pt for m in top_matches]).reshape(-1, 1, 2)

# Estimate transformation matrix
matrix, _ = cv2.findHomography(src_points, dst_points, cv2.RANSAC, 5.0)

# Warp the images
result = cv2.warpPerspective(image1, matrix, (image1.shape[1] + image2.shape[1], image1.shape[0]))
result[0:image2.shape[0], 0:image2.shape[1]] = image2

# Display the result
cv2.imshow('Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()