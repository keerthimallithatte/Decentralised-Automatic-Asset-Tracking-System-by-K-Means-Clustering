
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans
def train_data():
    X, y = make_blobs(n_samples=150, centers=2, cluster_std=0.40, random_state=0)
    plt.scatter(X[:,0], X[:,1])
    wcss = []
    for i in range(1, 3):
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)
    plt.plot(range(1, 3), wcss)
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.show()
    kmeans = KMeans(n_clusters=2, init='k-means++', max_iter=300, n_init=10, random_state=0)
    pred_y = kmeans.fit_predict(X)
    plt.scatter(X[:,0], X[:,1])
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='red')
    plt.show()
    return X,kmeans.cluster_centers_
def test(p,q,X,y):
    distance1= ((((q - p )**2) + ((y[0,0]-y[0,1])**2) )**0.5)
    distance2= ((((q - p )**2) + ((y[1,0]-y[1,1])**2) )**0.5)
    if (p == X[:,0].any() and q == X[:,1].any() ): 
	if(distance1>distance2):
        	print("Home")
	else:
		print("Office")
if __name__ == '__main__':
    X=[]
    y=[]
    X ,y= train_data()
    print(X)
    p = input()
    q = input()
    test(p,q,X,y)
    
    