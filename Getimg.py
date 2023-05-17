import os
import rosbag
import cv2
from cv_bridge import CvBridge
from tqdm import tqdm

class BagToImage(object):

    def __init__(self, bagfile_path, camera_topic, root):
        self.bagfile_path = bagfile_path  # bag路径
        self.camera_topic = camera_topic  # 准备工作中获取的topic
        self.root = root  # 用于组成存放照片的路径
        self.image_dir = os.path.join(root, "images")  # 存放照片的路径

        # 检查路径是否存在，否则创建
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

    def extractFromCamera(self):
        bag = rosbag.Bag(self.bagfile_path, "r")  # 读取bag
        bridge = CvBridge()  # 用于将图像消息转为图片
        bag_data_imgs = bag.read_messages(self.camera_topic)  # 读取图像消息

        index = 0

        pbar = tqdm(bag_data_imgs)
        for topic, msg, t in pbar:
            pbar.set_description("Processing extract image id: %s" % (index + 1))
            # 消息转为图片
            #cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
            # 如果提取的是压缩图片格式，使用这一句
            cv_image = bridge.compressed_imgmsg_to_cv2(msg, "bgr8")  
            # 存储图片
            cv2.imwrite(os.path.join(self.image_dir, str(index) + ".bmp"), cv_image)
            index += 1


if __name__ == '__main__':
    bagfile_path = "/home/xh_cai/Project/Github/Getimgfrombag/src/rosbag/img_imu_2023-04-26-14-49-39_1.bag"  # 此处为绝对路径

    camera_topic = "/image_raw0/compressed"  # 准备工作中得到的topic

    extract_image = BagToImage(bagfile_path, camera_topic, "/home/xh_cai/Project/Github/Getimgfrombag/src/img")  # xxx处路径就是存放照片的路径

    extract_image.extractFromCamera()
