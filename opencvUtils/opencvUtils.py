import cv2
import numpy as np
import pickle
# test opencv 
"""
print(cv2.__version__)
img=cv2.imread("1.png")
cv2.imshow("output",img)
"""
# 获得灰度图像
def get_Gray(img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#高斯滤波
def get_gaussianBlur(img,size):
    return cv2.GaussianBlur(img,size,0)

#Canny边缘检测
def get_canny(img,low,high):
    return cv2.Canny(img,low,high)

#dilate膨胀
def get_dilate(imgCanny,size,num):
    return cv2.dilate(imgCanny,np.ones(size,np.uint8),iterations=1)

#erode腐蚀
def get_eroded(imgCanny,size,num):
    return cv2.erode(imgCanny,np.ones(size,np.uint8),iterations=1)

#resize放大缩小图像
def get_resize(img,mul):
    return cv2.resize(img,(int(img.shape[1]*mul),int(img.shape[0]*mul)))

#截取图像
def get_cut(img,y_s,y_e,x_s,x_e):
    return img[y_s:y_e,x_s:x_e]

#zeros定义空图像
def get_zeros(w,h,channels):
    return np.zeros((w,h,channels),np.uint8)

#图像置色
def get_setColor(img,b,g,r):
    img[:]=r,g,b
    return img

#line画直线
def get_line(img,start,end,bgr,weight):
    cv2.line(img,start,end,bgr,weight)
    return img

#rectangle画矩形
def get_rect(img,start,end,bgr,weight):
    cv2.rectangle(img,start,end,bgr,weight)
    return img

#circle画圆
def get_circle(img,point,r,bgr,weight):
    cv2.circle(img,point,r,bgr,weight)
    return img

#putText画文字
def get_putText(img,text,point,size,bgr,weight):
    cv2.putText(img,text,point,cv2.FONT_HERSHEY_COMPLEX,size,bgr,weight)
    return img
    
#仿射变换
def get_transformation(img,list,width,height):
    list=np.float32(list)
    size=np.float32([[0,0],[width,0],[0,height],[width,height]])
    matrix=cv2.getPerspectiveTransform(list,size)
    return cv2.warpPerspective(img,matrix,(width,height))

#HSV色彩空间
def get_HSVspace(img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

#namedWindow定义窗口
def get_namedWindow(name):
    cv2.namedWindow(str(name),0)
    #cv2.resizeWindow(str(name),200,200)


#createTrackBar创建滑动条
def get_Trackbar(window,name,min,max,function):
    cv2.createTrackbar(name,window,min,max,function)

#getTrackbarPos获得滑动条的值
def get_TrackbarPos(window,name):
    return cv2.getTrackbarPos(name,window)

#inRange
def get_inRange(img,min_hsv_list,max_hsv_list):
    lower=np.array(min_hsv_list)
    upper=np.array(max_hsv_list)
    return cv2.inRange(img,lower,upper)

#bitwise_and与操作
def get_and(imglist,mask):
    img=imglist[0]
    for i in imglist:
        img=cv2.bitwise_and(img,i,mask=mask)
    return img


#findContours轮廓发现
#检测模式
#cv2.RETR_EXTERNAL：只检测最外层轮廓，并置hierarchy[i][2]=hierarchy[i][3]=-1
#cv2.RETR_LIST：提取所有轮廓并记录在列表中，轮廓之间无等级关系
#cv2.RETR_CCOMP：提取所有轮廓并建立双层结构（顶层为连通域的外围轮廓，底层为孔的内层边界）
#cv2.RETR_TREE：提取所有轮廓，并重新建立轮廓层次结构
#逼近方法
#cv2.CHAIN_APPROX_NONE：获取每个轮廓的每个元素，相邻像素的位置差不超过1，即连续的点，但通常我们并不需要所有的点
#cv2.CHAIN_APPROX_SIMPLE：压缩水平方向、垂直方向和对角线方向的元素，保留该方向的终点坐标，如矩形的轮廓可用4个角点表示，这是一种常用的方法，比第一种方法能得出更少的点
#cv2.CHAIN_APPROX_TC89_L1和cv2.CHAIN_APPROX_TC89_KCOS：对应Tch-Chain链逼近算法
def get_Contours(img):
    contours,hiearchy=cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return (contours,hiearchy)

#轮廓周长
def get_contourLength(cnt):
    return cv2.arcLength(cnt,True)

#轮廓拟合
def get_contourApproxPolyDP(cnt,rate):
    return cv2.approxPolyDP(cnt,rate*get_contourLength(cnt),True)

#drawContours画轮廓
def get_drawContours(img,con_hie):
    for cnt in con_hie[0]:
        cv2.drawContours(img,cnt,-1,(255,0,0),3)
    return img

#二值化threshold
def get_threshold(img,low,high):
    ret,img=cv2.threshold(img,low,high,cv2.THRESH_BINARY,dst=None)
    return img

#通道分离
def get_split(img):
    BGR=cv2.split(img)
    return BGR

#获得图像的长与宽
def get_img_width(img):
    return img.shape[1]
def get_img_height(img):
    return img.shape[0]
def get_img_large_side(img):
    if(img.shape[0]>img.shape[1]):
        return img.shape[0]
    else:
        return img.shape[1]
def get_img_ROI(img,x,y,width,height):
    return img[y:y+height,x:x+width]

def main():
    save_count=0
    with open('./face.model','rb') as fr:
        face_model=pickle.load(fr)

    cap=cv2.VideoCapture(0)
    #width 640 height  480
    get_namedWindow("Video")
    while 1:
        success,img=cap.read()
        if(not success):
            break
        print(img.shape)
        get_rect(img,(204,77),(464,384),(255,0,0),2)
        origin_img=img.copy()
        BGR=get_split(origin_img)
        #cv2.imshow("G",BGR[1])
        img=get_Gray(img)
        #img=get_threshold(img,120,255)
        face=get_img_ROI(img,204,77,464-204,384-77)
        #识别检测
        dp_data=face.reshape(1,-1)
        #dp_data=(dp_data>100)
        print("识别结果 : ",face_model.predict(dp_data))
        origin_img = cv2.putText(origin_img, '{}'.format(face_model.predict(dp_data)), (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        cv2.imshow("Video",face)
        cv2.imshow("origin_img",origin_img)
        key=cv2.waitKey(1)
        if(key&0xFF==ord('q')):
            break
        elif(key&0xFF==ord('s')):
            cv2.imwrite('./nosample/{}.jpg'.format(save_count),face, [int( cv2.IMWRITE_JPEG_QUALITY), 95])
            save_count+=1

if __name__ == "__main__":
    main()
