#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 15:36:07 2018

@author: yangyc
"""
#%% import libraries and data
import numpy as np
import pandas as pd
from KindAP import KindAP
from sklearn.manifold import SpectralEmbedding
from numpy import linalg as la
import matplotlib.pyplot as plt
import scipy.io
from munkres import Munkres

from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans,AffinityPropagation

from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn.metrics.cluster import v_measure_score,adjusted_rand_score
from sklearn.metrics.cluster import completeness_score,homogeneity_score
import time

train_data = pd.read_csv('/Users/yangyc/Documents/statML/kaggle/training_data.csv',
                         sep = ',',header = None).as_matrix()
test_data = pd.read_csv('/Users/yangyc/Documents/statML/kaggle/test_data.csv', 
                        sep = ',', header = None).as_matrix()

train_labels = pd.read_csv('/Users/yangyc/Documents/statML/kaggle/training_labels.csv',
                         sep = ',',header = None).as_matrix()
test_labels = pd.read_csv('/Users/yangyc/Documents/statML/kaggle/test_labels.csv').as_matrix()

Data = np.vstack((train_data,test_data))
ground_truth = np.vstack((train_labels,test_labels))[:,0]
print('Data Loading Complete!')

def best_map(L1,L2):
	#L1 should be the labels and L2 should be the clustering number we got
	Label1 = np.unique(L1)
	nClass1 = len(Label1)
	Label2 = np.unique(L2)
	nClass2 = len(Label2)
	nClass = np.maximum(nClass1,nClass2)
	G = np.zeros((nClass,nClass))
	for i in range(nClass1):
		ind_cla1 = L1 == Label1[i]
		ind_cla1 = ind_cla1.astype(float)
		for j in range(nClass2):
			ind_cla2 = L2 == Label2[j]
			ind_cla2 = ind_cla2.astype(float)
			G[i,j] = np.sum(ind_cla2 * ind_cla1)
	m = Munkres()
	index = m.compute(-G.T)
	index = np.array(index)
	c = index[:,1]
	newL2 = np.zeros(L2.shape)
	for i in range(nClass2):
		newL2[L2 == Label2[i]] = Label1[c[i]]
	return newL2

#%% Prepossessing
#pca = PCA(n_components=515)
#Data_t=pca.fit_transform(Data)
N_cluster = 6
embedding = SpectralEmbedding(n_components=N_cluster)
Data_transformed = embedding.fit_transform(Data)

np.save('Data_T', Data_transformed)
#S,D,V=la.svd(Data,full_matrices=False)
#%% Loading
print('Saving and Loading Preprocessed Data......')
np.load('Data_T.npy')
#%% Initializing
kindAP_accuracy = np.zeros(6)
kmeans_accuracy = np.zeros(6)
ward_accuracy = np.zeros(6)
avr_accuracy = np.zeros(6)
complete_accuracy = np.zeros(6)
aff_accuracy = np.zeros(6)
SR_accuracy = np.zeros(6)
kindAPL_accuracy = np.zeros(6)
#%% KindAP
t_start=time.time()
ki = KindAP(n_clusters = N_cluster)
pred_kindAP = ki.fit_predict(Data_transformed)
t_end=time.time()
print('--------------------------------')
kindAP_t = t_end-t_start
print('KindAP timing is ', kindAP_t)
kindAP_accuracy[0] = sum(ground_truth==best_map(ground_truth,pred_kindAP))/ground_truth.shape[0]
kindAP_accuracy[1] = normalized_mutual_info_score(ground_truth,pred_kindAP)
kindAP_accuracy[2] = v_measure_score(ground_truth,pred_kindAP)
kindAP_accuracy[3] = completeness_score(ground_truth,pred_kindAP)
kindAP_accuracy[4] = adjusted_rand_score(ground_truth,pred_kindAP)
kindAP_accuracy[5] = homogeneity_score(ground_truth,pred_kindAP)
print('KindAP matching accuracy is ', kindAP_accuracy[0])
print('KindAP normalized_mutual_info_score is ', kindAP_accuracy[1])
print('KindAP v_measure_score is ', kindAP_accuracy[2])
print('KindAP completeness_score is ', kindAP_accuracy[3])
print('KindAP adjusted_rand_score is ', kindAP_accuracy[4])
print('KindAP homogeneity_score is ', kindAP_accuracy[5])
#%% KindAP+L
t_start=time.time()
ki = KindAP(n_clusters = N_cluster)
pred_kindAPL = ki.fit_predict_L(Data_transformed)
t_end=time.time()
print('--------------------------------')
kindAPL_t = t_end-t_start
print('KindAP+L timing is ', kindAPL_t)
kindAPL_accuracy[0] = sum(ground_truth==best_map(ground_truth,pred_kindAPL))/ground_truth.shape[0]
kindAPL_accuracy[1] = normalized_mutual_info_score(ground_truth,pred_kindAPL)
kindAPL_accuracy[2] = v_measure_score(ground_truth,pred_kindAPL)
kindAPL_accuracy[3] = completeness_score(ground_truth,pred_kindAPL)
kindAPL_accuracy[4] = adjusted_rand_score(ground_truth,pred_kindAPL)
kindAPL_accuracy[5] = homogeneity_score(ground_truth,pred_kindAPL)
print('KindAP+L matching accuracy is ', kindAPL_accuracy[0])
print('KindAP+L normalized_mutual_info_score is ', kindAPL_accuracy[1])
print('KindAP+L v_measure_score is ', kindAPL_accuracy[2])
print('KindAP+L completeness_score is ', kindAPL_accuracy[3])
print('KindAP+L adjusted_rand_score is ', kindAPL_accuracy[4])
print('KindAP+L homogeneity_score is ', kindAPL_accuracy[5])
#%% SR
t_start=time.time()
ki = KindAP(n_clusters = N_cluster,isnrm_row_U=True, do_inner=False,
            isnrm_col_H=False,isbinary_H=True,disp=True)
pred_SR = ki.fit_predict(Data_transformed)
t_end=time.time()
print('--------------------------------')
SR_t = t_end-t_start
print('SR timing is ', SR_t)
SR_accuracy[0] = sum(ground_truth==best_map(ground_truth,pred_SR))/ground_truth.shape[0]
SR_accuracy[1] = normalized_mutual_info_score(ground_truth,pred_SR)
SR_accuracy[2] = v_measure_score(ground_truth,pred_SR)
SR_accuracy[3] = completeness_score(ground_truth,pred_SR)
SR_accuracy[4] = adjusted_rand_score(ground_truth,pred_SR)
SR_accuracy[5] = homogeneity_score(ground_truth,pred_SR)
print('SR matching accuracy is ', SR_accuracy[0])
print('SR normalized_mutual_info_score is ', SR_accuracy[1])
print('SR v_measure_score is ', SR_accuracy[2])
print('SR completeness_score is ', SR_accuracy[3])
print('SR adjusted_rand_score is ', SR_accuracy[4])
print('SR homogeneity_score is ', SR_accuracy[5])
#%% K-means Clustering
t_start=time.time()
kmeans = KMeans(init="random",n_clusters=N_cluster,n_init=1,precompute_distances=False)
#kmeans.fit(Uk)
pred_kmeans = kmeans.fit_predict(Data_transformed)
t_end=time.time()
print('--------------------------------')
kmeans_t = t_end-t_start
print('K-means timing is ', kmeans_t)
kmeans_accuracy[0] = sum(ground_truth==best_map(ground_truth,pred_kmeans))/ground_truth.shape[0]
kmeans_accuracy[1] = normalized_mutual_info_score(ground_truth,pred_kmeans)
kmeans_accuracy[2] = v_measure_score(ground_truth,pred_kmeans)
kmeans_accuracy[3] = completeness_score(ground_truth,pred_kmeans)
kmeans_accuracy[4] = adjusted_rand_score(ground_truth,pred_kmeans)
kmeans_accuracy[5] = homogeneity_score(ground_truth,pred_kmeans)
print('K-means matching accuracy is ', kmeans_accuracy[0])
print('K-means normalized_mutual_info_score is ', kmeans_accuracy[1])
print('K-means v_measure_score is ', kmeans_accuracy[2])
print('K-means completeness_score is ', kmeans_accuracy[3])
print('K-means adjusted_rand_score is ', kmeans_accuracy[4])
print('K-means homogeneity_score is ', kmeans_accuracy[5])
#sp = SpectralClustering(n_clusters=N_cluster)
#pred_sp = sp.fit_predict(Data)
#sp_accuracy[1] = normalized_mutual_info_score(pred_sp,ground_truth)
#sp_accuracy[2] = v_measure_score(pred_sp,ground_truth)
#print('Spectral Clustering normalized_mutual_info_score is ', sp_accuracy[1])
#print('Spectral Clustering v_measure_score is ', sp_accuracy[2])

#%% Hierarchy Clustering
print('--------------------------------')
t_start=time.time()
hier = AgglomerativeClustering(n_clusters=N_cluster,linkage='ward')
pred_ward = hier.fit_predict(Data_transformed)
t_end=time.time()
ward_t = t_end-t_start
print('Ward linkage timing is ', ward_t)
ward_accuracy[0] = sum(ground_truth==best_map(ground_truth,pred_ward))/ground_truth.shape[0]
ward_accuracy[1] = normalized_mutual_info_score(ground_truth,pred_ward)
ward_accuracy[2] = v_measure_score(ground_truth,pred_ward)
ward_accuracy[3] = completeness_score(ground_truth,pred_ward)
ward_accuracy[4] = adjusted_rand_score(ground_truth,pred_ward)
ward_accuracy[5] = homogeneity_score(ground_truth,pred_ward)
print('Ward linkage matching accuracy is ', ward_accuracy[0])
print('Ward linkage normalized_mutual_info_score is ', ward_accuracy[1])
print('Ward linkage v_measure_score is ', ward_accuracy[2])
print('Ward linkage completeness_score is ', ward_accuracy[3])
print('Ward linkage adjusted_rand_score is ', ward_accuracy[4])
print('Ward linkage homogeneity_score is ', ward_accuracy[5])                                

print('--------------------------------')
t_start=time.time()
hier = AgglomerativeClustering(n_clusters=N_cluster,linkage='complete')
pred_complete = hier.fit_predict(Data_transformed)
t_end=time.time()
complete_t = t_end-t_start
print('Complete linkage timing is ', complete_t)
complete_accuracy[0] = sum(ground_truth==best_map(ground_truth,pred_complete))/ground_truth.shape[0]
complete_accuracy[1] = normalized_mutual_info_score(pred_complete,ground_truth)
complete_accuracy[2] = v_measure_score(pred_complete,ground_truth)
complete_accuracy[3] = completeness_score(ground_truth,pred_complete)
complete_accuracy[4] = adjusted_rand_score(ground_truth,pred_complete)
complete_accuracy[5] = homogeneity_score(ground_truth,pred_complete)
print('Complete linkage matching accuracy is ', complete_accuracy[0])
print('Complete linkage normalized_mutual_info_score is ', complete_accuracy[1])
print('Complete linkage v_measure_score is ', complete_accuracy[2])
print('Complete linkage completeness_score is ', complete_accuracy[3])
print('Complete linkage adjusted_rand_score is ', complete_accuracy[4])
print('Complete linkage homogeneity_score is ', complete_accuracy[5])

print('--------------------------------')
t_start=time.time()
hier = AgglomerativeClustering(n_clusters=N_cluster,linkage='average')
pred_avr = hier.fit_predict(Data_transformed)
t_end=time.time()
avr_t = t_end-t_start
print('Average linkage timing is ', avr_t)
avr_accuracy[0] = sum(ground_truth==best_map(ground_truth,pred_avr))/ground_truth.shape[0]
avr_accuracy[1] = normalized_mutual_info_score(pred_avr,ground_truth)
avr_accuracy[2] = v_measure_score(pred_avr,ground_truth)
avr_accuracy[3] = completeness_score(ground_truth,pred_avr)
avr_accuracy[4] = adjusted_rand_score(ground_truth,pred_avr)
avr_accuracy[5] = homogeneity_score(ground_truth,pred_avr)
print('Average linkage matching accuracy is ', avr_accuracy[0])
print('Average linkage normalized_mutual_info_score is ', avr_accuracy[1])
print('Average linkage v_measure_score is ', avr_accuracy[2])
print('Average linkage completeness_score is ', avr_accuracy[3])
print('Average linkage adjusted_rand_score is ', avr_accuracy[4])
print('Average linkage homogeneity_score is ', avr_accuracy[5])


#%% Affinity Propagation
print('--------------------------------')
t_start=time.time()
aff = AffinityPropagation()
aff.fit(Data)
pred_aff = aff.predict(Data_transformed)
t_end=time.time()
aff_t = t_end-t_start
print('Affinity Propagation timing is ', aff_t)
aff_accuracy[0] = sum(ground_truth==best_map(ground_truth,pred_aff))/ground_truth.shape[0]
aff_accuracy[1] = normalized_mutual_info_score(pred_aff,ground_truth)
aff_accuracy[2] = v_measure_score(pred_aff,ground_truth)
aff_accuracy[3] = completeness_score(ground_truth,pred_aff)
aff_accuracy[4] = adjusted_rand_score(ground_truth,pred_aff)
aff_accuracy[5] = homogeneity_score(ground_truth,pred_aff)
print('Affinity Propagation matching accuracy is ', aff_accuracy[0])
print('Affinity Propagation normalized_mutual_info_score is ', aff_accuracy[1])
print('Affinity Propagation v_measure_score is ', aff_accuracy[2])
print('Affinity Propagation completeness_score is ', aff_accuracy[3])
print('Affinity Propagation adjusted_rand_score is ', aff_accuracy[4])
print('Affinity Propagation homogeneity_score is ', aff_accuracy[5])