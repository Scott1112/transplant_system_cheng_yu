import cv2
import numpy as np
import os
import time

class ImageProcessing:
    def __init__(self, image_path):
        self.cam_id = 1
        self.image_path = image_path
        self.image_crop_path = f"{self.image_path}/crop"
        self.cam = cv2.VideoCapture(self.cam_id, cv2.CAP_DSHOW)
        # self.cam.set(cv2.CAP_PROP_BUFFERSIZE, 0)
        self.cam.set(3,1920)
        self.cam.set(4,1080)
        self.img_count = 0
        self.img_egg_count = 0
        self.motor_egg_count = 0
        # self.test()

    def test(self):
        # cv2.namedWindow("egg", 0)
        # cv2.resizeWindow("egg", 960, 540)
        # self.cam.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, self.img = self.cam.read()
        if not ret:
            print("failed to grab frame")    
        else: self.show(self.img)

    def show(self, img):
        cv2.namedWindow("worm", 0)
        print('shape:',self.img.shape[1], self.img.shape[0])
        cv2.resizeWindow("worm", int(self.img.shape[1]/2), int(self.img.shape[0]/2))    
        while True:
            cv2.imshow("worm",img)
            if cv2.waitKey(10) & 0xff == ord('q'):
                break
        cv2.destroyAllWindows()
        
    def take_photo(self, show=False):
        # self.cam.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, self.img = self.cam.read()
        while not ret:
            print('!!!!!!!!!!camera shut down. reload camera!!!!!!!!!')
            self.cam.release()  
            cv2.destroyAllWindows()    
            self.cam = cv2.VideoCapture(self.cam_id, cv2.CAP_DSHOW)
            # self.cam.set(3,1920)
            # self.cam.set(4,1080)
            ret, self.img = self.cam.read()
            time.sleep(0.1)
        if show:
            self.show(self.img)
        # cv2.destroyAllWindows()
        self.save_img(self.img)
        return self.img

    def save_img(self, img, crop = False):
        if crop:
            folder_path = self.image_crop_path
            count = self.img_egg_count
            self.img_egg_count += 1
        else:
            folder_path = self.image_path
            count = self.img_count
            self.img_count += 1
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = f"{folder_path}/{count}.jpg"
        cv2.imwrite(file_path, img)
        print(f"save images at: {file_path}")
        return self.img
    
    def find_worm_center(self, show=False):
        # self.cam.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.img = self.take_photo()
        self.show(self.img)
        self.img = self.img[48:-55, 490:-480]

        # Convert BGR to GRAY
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('gray', gray)
        # cv2.imwrite('./process_img/gray.jpg', gray)

        ret, th = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
        # cv2.imshow('threshold', th)
        # cv2.imwrite('./process_img/threshold.jpg', th)

        kernel_erosion = np.ones((2, 2), np.uint8)
        eroded = cv2.erode(th, kernel_erosion, iterations=1)
        # cv2.imshow('eroded', eroded)
        # cv2.imwrite('./process_img/eroded.jpg', eroded)
        
        kernel_dilation = np.ones((3, 3), np.uint8)
        dilation = cv2.dilate(eroded, kernel_dilation, iterations = 1)
        cv2.imshow('dilation', dilation)
        # cv2.imwrite('./process_img/dilation.jpg', dilation)

        final_frame = dilation
        contours, hierarchy = cv2.findContours(final_frame,
                                            cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)

        self.img_obj_center = []
        for i, contour in enumerate(contours):
            print(cv2.contourArea(contour))
            if  cv2.contourArea(contour) > 3000 or cv2.contourArea(contour) < 50:
                continue
            
            # x, y, w, h = cv2.boundingRect(contour)
            # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)

            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            xy = "(%d, %d)" % (cX, cY)
            self.img_obj_center.append((cX, cY))
        
            # (a, b), radius = cv2.minEnclosingCircle(contour)
            # centeroid = (int(a), int(b))
            # radius = int(radius)
            
            cv2.drawContours(self.img, contours, i, (255, 0, 0), 2)
            cv2.circle(self.img, (cX, cY), 4, (0, 0, 255), -1)
            cv2.putText(self.img, xy, (cX, cY-20), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)

        if show:
            self.show(self.img)

            self.save_img(self.img)
                # cv2.imwrite('center.jpg', img_center)

            # if self.img_obj_center:
            #     print("egg center at:", self.img_obj_center)

            return self.img_obj_center


if __name__ == '__main__':

    folder_name = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    image_path = f"C:/Users/User/Desktop/transplant_system_cheng_yu/automation/data/img/inhold_worm/{folder_name}"
    print(f"save images at: {image_path}")
    cam = ImageProcessing(image_path)
    cam.find_worm_center(show=True)
