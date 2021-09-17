import cv2
import numpy as np

# Read source image.
img_src = cv2.imread('cat.png')

# Four corners of source image
# Coordinates are in x,y system with x horizontal to the right and y vertical downward
pts_src = np.float32([[0,0], [359,0], [379,333], [0,333]])

# Four corners of destination image.
pts_dst = np.float32([[0, 0], [359,0], [306,376], [0,333]])

# Get perspecive matrix if only 4 points
m = cv2.getPerspectiveTransform(pts_src,pts_dst)

# Warp source image to destination based on matrix
# size argument is width x height
# compute from max output coordinates
print(m)
img_out = cv2.warpPerspective(img_src, m, (359+1,376+1), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
print(img_out)
# Save output


# Display result
cv2.imshow("Warped Source Image", img_out)
cv2.waitKey(0)
cv2.destroyAllWindows()