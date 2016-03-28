# coding=utf-8
import cv2;
import numpy as np;
  
#用於製作二維陣列用的function
def zerolistmaker(n):
    return ([0] * n, [0] * n);
	
#用於繪製灰階直方圖的function
def calcAndDrawHist(image, color):    
	hist= cv2.calcHist([image], [0], None, [256], [0.0,255.0]);    
	minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist);    
	histImg = np.zeros([256,256,3], np.uint8);    
	hpt = int(0.9* 256);    
        
	for h in range(256):    
		intensity = int(hist[h]*hpt/maxVal);    
		cv2.line(histImg,(h,256), (h,256-intensity), color);    
            
	return histImg;   
	
#載入圖片
img = cv2.imread('mp1.jpg', 0);  # 0代表灰階圖片 (1用於彩色圖片)

#計算並顯示出原圖的灰階直方圖
histImgG = calcAndDrawHist(img, [255, 255, 255]);     
cv2.imshow("oldGray", histImgG);    
 

#計算圖片的長和寬，並且計算圖片總像素
height = len(img);
width = len(img[0]);
sum = height*width;
bit = 256;

#宣告兩個一維陣列，grayDistribution存放各灰階值的分布數量，newGray則存放各灰階值等化過後的新的對應值
grayDistribution, newGray = zerolistmaker(bit);


#計算各灰階值的分布數量
for i in range(0, height, 1):
	for j in range(0, width, 1):
		grayDistribution[img[i][j]]+=1;
	
#計算灰階值於0~255的分布機率
for i in range(0, bit, 1):
	grayDistribution[i] = float(grayDistribution[i])/sum;

#套用公式並計算出各灰階值新的對應值，並存進陣列newGray
for i in range(0, bit, 1):
	temp = 0;
	for j in range(0, i+1, 1):
		temp = temp + grayDistribution[j];	
	newGray[i] = round((bit-1)*temp);
	
#將灰階的新對應值取代原始灰階值陣列中的值
for i in range(0, height, 1):
	for j in range(0, width, 1):
		newPixel = newGray[img[i][j]];
		img[i][j] = newPixel;
		
#計算並顯示出新的灰階直方圖
histImgG2 = calcAndDrawHist(img, [255, 255, 255]);     
cv2.imshow("newGray", histImgG2); 

#顯示等化後結果
cv2.imshow('newPicture',img);

cv2.waitKey(0);
cv2.destroyAllWindows();


