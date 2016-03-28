# coding=utf-8
import cv2;
import numpy as np;  


#用於製作二維陣列用的function
def zerolistmaker(n):
    return ([0] * n, [0] * n, [0] * n, [0] * n, [0] * n, [0] * n);
	
#用於繪製RGB直方圖的function
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
img = cv2.imread('mp1a.jpg', 1);   # 1代表彩色圖片 (0用於灰階圖片)

#將顏色RGB各別取出並丟給b,g,r三個二維陣列存放
b,g,r = cv2.split(img);   

#計算並顯示出原圖的RGB直方圖
histImgB = calcAndDrawHist(b, [255, 0, 0]);    
histImgG = calcAndDrawHist(g, [0, 255, 0]);    
histImgR = calcAndDrawHist(r, [0, 0, 255]);    
        
cv2.imshow("oldB", histImgB)    
cv2.imshow("oldG", histImgG)    
cv2.imshow("oldR", histImgR)    


#計算圖片的長和寬，並且計算圖片總像素
height = len(b);
width = len(b[0]);
sum = height*width;

#RGB各別的範圍為0~255
bit = 256;

#宣告兩個一維陣列，bdis, rdis, gdis存放B, R, G值的分布數量，newB, newR, newG則存放各B, R, G等化過後的新的對應值
bdis, rdis, gdis, newB, newR, newG = zerolistmaker(bit);


#計算各RGB值的分布數量
for i in range(0, height, 1):
	for j in range(0, width, 1):
		bdis[b[i][j]]+=1;
		rdis[r[i][j]]+=1;
		gdis[g[i][j]]+=1;
	

#計算RGB值0~255的分布機率
for i in range(0, bit, 1):
	bdis[i] = float(bdis[i])/sum;
	rdis[i] = float(rdis[i])/sum;
	gdis[i] = float(gdis[i])/sum;

#套用公式並計算出各RGB新的對應值，並存進陣列newR, newG, newB
for i in range(0, bit, 1):
	temp = 0;
	temp2 = 0;
	temp3 = 0;
	for j in range(0, i+1, 1):
		
		temp = temp + bdis[j];	
		temp2 = temp2 + rdis[j];
		temp3 = temp3 + gdis[j];
		
	newB[i] = round((bit-1)*temp);
	newR[i] = round((bit-1)*temp2);
	newG[i] = round((bit-1)*temp3);
	



#將RGB的新對應值取代原始RGB值陣列中的值
for i in range(0, height, 1):
	for j in range(0, width, 1):
		newPixel = newB[b[i][j]];
		b[i][j] = newPixel;
		
		newPixel = newR[r[i][j]];
		r[i][j] = newPixel;
		
		newPixel = newG[g[i][j]];
		g[i][j] = newPixel;
		
#計算並顯示出新圖片的RGB直方圖
histImgB2 = calcAndDrawHist(b, [255, 0, 0])    
histImgG2 = calcAndDrawHist(g, [0, 255, 0])    
histImgR2 = calcAndDrawHist(r, [0, 0, 255])    
        
cv2.imshow("newB", histImgB2)    
cv2.imshow("newG", histImgG2)    
cv2.imshow("newR", histImgR2)  
		
		
#將新的RGB merge成新的圖片
img2 = cv2.merge((b,g,r));

#顯示等化前 等化後結果
cv2.imshow('original',img);
cv2.imshow('new',img2);

cv2.waitKey(0);
cv2.destroyAllWindows();


