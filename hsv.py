# coding=utf-8
import cv2;
import numpy as np;  

#用於繪製V值直方圖的function
def calcAndDrawHist(image, color):    
	hist= cv2.calcHist([image], [0], None, [256], [0.0,255.0])    
	minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)    
	histImg = np.zeros([256,256,3], np.uint8)    
	hpt = int(0.9* 256);    
        
	for h in range(256):    
		intensity = int(hist[h]*hpt/maxVal)    
		cv2.line(histImg,(h,256), (h,256-intensity), color)    
            
	return histImg;  


#載入圖片
img = cv2.imread('mp1a.jpg');

#將原本圖片的BGR格式轉換為YCbCr格式，並且將值各別取出
img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV);
H, S, V = cv2.split(img2);  
bits = 256;

#計算並顯示出原圖的V值直方圖
histImgV = calcAndDrawHist(V, [255, 255, 255]);  
cv2.imshow("oldV", histImgV)  

#宣告兩個一維陣列，VDis存放V值的分布數量，newV則存放各Y等化過後的新的對應值
VDis = [0]*bits;
newV = [0]*bits;

#圖片的長和寬以及總像素
height = len(img2);
width = len(img2[0]);
sum = width*height;

#計算各V值的分布數量
for i in range(0, height, 1):
	for j in range(0, width, 1):
		VDis[V[i][j]]+=1;
	
#計算V值0~255的分布機率
for i in range(0, bits, 1):
	VDis[i] = float(VDis[i])/sum;

#套用公式並計算出各V新的對應值，並存進陣列newV
for i in range(0, bits, 1):
	temp = 0;
	for j in range(0, i+1, 1):
		temp = temp + VDis[j];	
	newV[i] = round((bits-1)*temp);
	
#將V的新對應值取代原始V值陣列中的值
for i in range(0, height, 1):
	for j in range(0, width, 1):
		newPixel = newV[V[i][j]];
		V[i][j] = newPixel;
		
#計算並顯示出新的V值直方圖
histImgV2 = calcAndDrawHist(V, [255, 255, 255]);  
cv2.imshow("newV", histImgV2)  

#將新的HSV merge成新的圖片
img2 = cv2.merge((H, S, V));

#由於imshow是讀取RGB的格式，因此要將HSV轉回RGB才能正常顯示
img2 = cv2.cvtColor(img2, cv2.COLOR_HSV2BGR);

#顯示等化前 等化後結果
cv2.imshow('original',img);
cv2.imshow('img2',img2);

cv2.waitKey(0);
cv2.destroyAllWindows();