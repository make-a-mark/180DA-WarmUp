import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.spatial import KDTree
import webcolors

'''
References:
https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097
https://medium.com/codex/rgb-to-color-names-in-python-the-robust-way-ec4a9d97a01f

Note: pip instaled webcolors to convert rgb to closest name
Converted finding dominant color on image into video by using a bounding box and converting the knn histogram results into color name to display.
'''

def convert_rgb_to_names(rgb_tuple):
    
    # a dictionary of all the hex and their respective names in css3
    css3_db = webcolors.CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(webcolors.hex_to_rgb(color_hex))
    
    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return f'closest match: {names[index]}'

def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist


def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    color_name = 0
    color_nums = []
    for (percent, color) in zip(hist, centroids):
        color_name = convert_rgb_to_names( (round(color[0]), round(color[1]), round(color[2])))
        color_nums = [round(color[0]), round(color[1]), round(color[2])]
        break

    # return the bar chart
    return color_name, color_nums

cap = cv2.VideoCapture(0)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    frame = cv2.resize(frame, (500, 500))
    bouding_box = cv2.rectangle(frame, (125, 125), (375, 375), (255,0,0), 2)

    img = cv2.cvtColor(bouding_box, cv2.COLOR_BGR2RGB)

    img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number
    clt = KMeans(n_clusters=3) #cluster number
    clt.fit(img)

    hist = find_histogram(clt)
    color_name, color_nums = plot_colors2(hist, clt.cluster_centers_)

    # font
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # org
    org = (0, 125)
    
    # fontScale
    fontScale = 1

    # Blue color in BGR
    color = (color_nums[2], color_nums[1], color_nums[0])

    # Line thickness of 2 px
    thickness = 2

    cv2.putText(frame, "color: " + color_name, org, font, fontScale, color, thickness, cv2.LINE_AA)
    cv2.imshow("Show",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

