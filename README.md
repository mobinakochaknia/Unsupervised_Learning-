# Unsupervised Learning - PCA and K-Means Clustering from Scratch

## Overview
This project demonstrates the implementation of **Principal Component Analysis (PCA)** and **K-Means Clustering** from scratch using Python, without relying on scikit-learn or any similar library. The goal of the project is to apply dimensionality reduction using PCA on a credit card dataset and then perform clustering to segment customers based on their usage patterns. The project involves comparing the clustering performance both before and after applying PCA.

## Requirements
To run this project, the following Python libraries are required:
- `numpy`
- `pandas`
- `matplotlib`
- `seaborn`
- `scipy`
- `sklearn` (only for preprocessing with `StandardScaler`)

# Dataset

The dataset used in this project contains information on customers' credit card usage. It includes several features like `BALANCE`, `PURCHASES`, `CREDIT_LIMIT`, and more, which represent different aspects of credit card usage.

### Columns in the Dataset:
- **BALANCE**: Balance amount.
- **CREDIT_LIMIT**: Credit limit for the user.
- **PURCHASES**: Total purchases made.
- **MINIMUM_PAYMENTS**: Minimum payments.
- ... *(add other columns based on your dataset)*

# Project Steps

## 1. Data Preprocessing
   - **Load the Dataset**: Load the data into a pandas DataFrame.
   - **Handle Missing Data**: Missing values in `CREDIT_LIMIT` and `MINIMUM_PAYMENTS` are replaced with their respective column means.
   - **Remove Redundant Features**: Features with high correlation (greater than 0.8) are removed.
   - **Standardize the Data**: The dataset is standardized using z-score normalization to ensure each feature contributes equally to the analysis.

## 2. PCA Implementation
   - **Custom PCA Class**: A custom PCA implementation is provided that calculates the covariance matrix, eigenvalues, and eigenvectors to perform dimensionality reduction.
   - **Explained Variance**: The cumulative explained variance is calculated, and the number of components needed to explain at least 75% of the variance is determined.
   - **Data Transformation**: The data is transformed into the new feature space defined by the principal components.

## 3. K-Means Clustering
   - **Custom K-Means Implementation**: The K-Means algorithm is implemented from scratch to cluster the customers into segments based on their usage patterns.
   - **Clustering Evaluation**: The clustering performance is evaluated using the **Silhouette Score** to measure the quality of the clusters.

## 4. Hierarchical Clustering
   - **Dendrogram**: A hierarchical clustering dendrogram is generated to visualize how customers are grouped based on their features.

## 5. Visualization
   - **Pairplots**: Visualize the pairwise relationships of PCA-reduced features colored by the cluster labels.
   - **Cumulative Explained Variance**: A plot shows how much variance is explained by each principal component.
   - **Clustering Results**: Visualize the clustering results with the first few principal components.
