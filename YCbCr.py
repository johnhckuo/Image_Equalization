# coding=utf-8
import cv2
import numpy as np;

#用於繪製YCbCr直方圖的function
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
img = cv2.imread('mp1a.jpg')

#將原本圖片的BGR格式轉換為YCbCr格式，並且將值各別取出
img2 = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
Y, Cb, Cr = cv2.split(img2);  

#計算並顯示出原圖的YCbCr的Y值直方圖
histImgY = calcAndDrawHist(Y, [255, 255, 255]);     
cv2.imshow("oldY", histImgY);   

#Y的公式為0.299*R + 0.587*G + 0.114*B，因此其範圍為0~255
bits = 256;

#宣告兩個一維陣列，YDis存放Y值的分布數量，newY則存放各Y等化過後的新的對應值
YDis = [0]*bits;
newY = [0]*bits;

#圖片的長和寬以及總像素
height = len(img2);
width = len(img2[0]);
sum = width*height;

#計算各Y值的分布數量
for i in range(0, height, 1):
	for j in range(0, width, 1):
		YDis[Y[i][j]]+=1;
	
#計算Y值0~255的分布機率
for i in range(0, bits, 1):
	YDis[i] = float(YDis[i])/sum;

#套用公式並計算出各Y新的對應值，並存進陣列newY
for i in range(0, bits, 1):
	temp = 0;
	for j in range(0, i+1, 1):
		temp = temp + YDis[j];	
	newY[i] = round((bits-1)*temp);
	
#將Y的新對應值取代原始Y值陣列中的值
for i in range(0, height, 1):
	for j in range(0, width, 1):
		newPixel = newY[Y[i][j]];
		Y[i][j] = newPixel;
		
#計算並顯示出全新的YCbCr的Y值直方圖
histImgY2 = calcAndDrawHist(Y, [255, 255, 255]);     
cv2.imshow("newY", histImgY2);   

#將新的YCbCr merge成新的圖片
img2 = cv2.merge((Y, Cb, Cr));

#由於imshow是讀取RGB的格式，因此要將YCbCr轉回RGB才能正常顯示
img2 = cv2.cvtColor(img2, cv2.COLOR_YCR_CB2BGR);

#顯示等化前 等化後結果
cv2.imshow('original',img);
cv2.imshow('new',img2);

cv2.waitKey(0);
cv2.destroyAllWindows();