# -*- coding: utf-8 -*-
"""Clustering-PCA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PcbvHzyZm6Ngdhe9lRMcpBakcJciZV8H

<img src="./pic/sharif-main-logo.png" alt="SUT logo" width=345 height=345 align=left class="saturate">


<br>
<font>
<div dir=ltr align=center>
<font color=0F5298 size=7>
    Machine Learning <br>
<font color=2565AE size=5>
    Computer Engineering Department <br>
    Fall 2024<br>
<font color=3C99D size=5>
    Practical Assignment 2 - Unsupervised Learning<br>
<font color=696880 size=4>
    Assignment Supervisor: Niki Sepasian <br>
<font color=696880 size=5>
    Asemaneh Nafe
"""

student_number = 401106396
full_name = 'mobina kochaknia'
assert student_number and full_name is not None, 'please input your information'

#import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import fcluster

"""<font color=red size=3>
notice that you can not use sklearn.decomposition and sklearn.cluster libary in this home work! you should implement pca and kmeans from scratch.

## Overview
In this assignment, you will perform PCA and K-Means clustering on credit card customer data. dataset contains information about customer’s use of credit cards. The goal is to reduce the dataset’s dimensionality using PCA and then apply clustering to segment customers. You will compare the clustering performance both before and after PCA. Additionally, you'll be asked to explain the theory and decisions behind each step.

## Data Preprocessing (15 points)
Read the dataset.CSV file and display a few samples.
"""

# loading data
data = pd.read_csv('dataset.csv')

data.head(5)

"""Display dataset information."""

#Display dataset information
data.info()
data.describe()

"""Which column do you think might be the most irrelevant for PCA and clustering?
<br>
Answer: CUST_ID
"""

# Exclude irrelevant feature
data = data.drop(columns=['CUST_ID'])
data.head()

"""how do you handle missing data, and why did you choose this method?
<br>
Answer:There are many ways to handle missing values. One of them is placement with the median, in this method we are less sensitive to the outlier values, but here, because there is probably a need to standardize the data, I did not choose this method. There is another method that can fill the missing values ​​with its nearest neighbor (using the method KNN), which in my opinion is not optimal because we have to run the algorithm twice. The method I chose was to replace the missing value with the average because it is more efficient in terms of time and can handle outliers well.
"""

#Fill missing data
data['CREDIT_LIMIT'].fillna(data['CREDIT_LIMIT'].mean(), inplace=True)
data['MINIMUM_PAYMENTS'].fillna(data['MINIMUM_PAYMENTS'].mean(), inplace=True)

print(data.isnull().sum())

"""plot the correlation matrix and identify redundant features.remove them from the dataframe."""

# Plot the correlation matrix
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Calculate the correlation matrix
corr_matrix = data.corr()

# Plot the correlation matrix
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title("Correlation Matrix")
plt.show()

# Identify and remove redundant features. use 0.8 threshold.
threshold = 0.8
high_corr_var = set()
for i in range(len(corr_matrix.columns)):
    for j in range(i):
        if abs(corr_matrix.iloc[i, j]) > threshold:  # high correlation (above threshold)
            colname = corr_matrix.columns[i]  # get the column name
            high_corr_var.add(colname)

# Remove highly correlated features from the dataframe
data = data.drop(columns=high_corr_var)

# Verify that redundant features have been removed
print(data.info())

"""## Standardize the Data (5 points)
Standardize the dataset using z-score normalization
"""

# Assuming `data` is  DataFrame with numeric features
scaler = StandardScaler()

# Standardize the DataFrame (fit and transform)
scaled_data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)

"""Why is it important to standardize the data before applying PCA?
<br>
Answer:

What is differnce between Normalizer and StandardScaler classes. which is better for PCA?
<br>
Answer:

## Principal Component Analysis (PCA) (35 points)
Implement PCA from scratch.
"""

import numpy as np

class CustomPCA:
    def __init__(self, n_components=None):
        """
        Initialize the PCA class with the number of components to keep.
        n_components: Number of principal components to keep. If None, all components are kept.
        """
        self.n_components = n_components
        self.components = None  # To store the principal components (eigenvectors)
        self.mean = None        # To store the mean of the data (used for centering the data)
        self.explained_variance_ratio = None  # To store the explained variance ratio of the components

    def fit(self, X):
        """
        Fit the PCA model on the dataset X by calculating the eigenvalues and eigenvectors of the covariance matrix.
        X: Input data (n_samples, n_features)
        """
        # Step 1: Center the data
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean

        # Step 2: Compute the covariance matrix
        cov_matrix = np.cov(X_centered, rowvar=False)

        # Step 3: Calculate the eigenvalues and eigenvectors of the covariance matrix
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

        # Step 4: Sort eigenvalues and eigenvectors in decreasing order of eigenvalues
        sorted_indices = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[sorted_indices]
        eigenvectors = eigenvectors[:, sorted_indices]

        # Step 5: Select the top n_components if specified
        if self.n_components is not None:
            eigenvalues = eigenvalues[:self.n_components]
            eigenvectors = eigenvectors[:, :self.n_components]

        # Store the principal components and explained variance ratio
        self.components = eigenvectors
        total_variance = np.sum(eigenvalues)
        self.explained_variance_ratio = eigenvalues / total_variance

    def transform(self, X):
        """
        Transform the input data X into the new space using the principal components.
        X: Input data (n_samples, n_features)
        """
        # Center the data using the mean from the training set
        X_centered = X - self.mean

        # Project the data onto the principal components (eigenvectors)
        X_transformed = np.dot(X_centered, self.components)
        return X_transformed

    def get_explained_variance_ratio(self):
        """
        Return the explained variance ratio of each principal component.
        """
        return self.explained_variance_ratio

    def get_components(self):
        """
        Return the principal components (eigenvectors).
        """
        return self.components

"""### Visualizing the Cumulative Variance

Plot the cumulative explained variance to visualize the selection of components.  How many components are needed to explain 75% of the variance?
<br>
answer:6
"""

copy_of_scale_data = scaled_data.copy()
pca = CustomPCA()
pca.fit(copy_of_scale_data)

# Calculate cumulative explained variance
cumulative_variance = np.cumsum(pca.get_explained_variance_ratio())

# Plot the cumulative explained variance
plt.figure(figsize=(8, 6))
plt.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, marker='o', linestyle='--')
plt.xlabel('Number of Principal Components')
plt.ylabel('Cumulative Explained Variance')
plt.title('Cumulative Explained Variance vs. Number of Components')
plt.axhline(y=0.75, color='r', linestyle='--', label="75% Variance")
plt.legend()
plt.grid(True)
plt.show()

# Find the number of components needed to explain at least 75% of the variance
components_needed = np.argmax(cumulative_variance >= 0.75) + 1
print(f"Number of components needed to explain 75% of the variance: {components_needed}")

"""Build a new DataFrame with the first slected components. save it to a new CSV file named 'pca_output.csv'"""

from typing_extensions import dataclass_transform
#Build a new DataFrame with the first slected components
data_transformed = pca.transform(scaled_data)[:,:5]
pca = CustomPCA(n_components=5)
pca.fit(scaled_data)


# Step 2: Transform the data using the top 5 components
pca_data = pca.transform(scaled_data)

# Step 3: Create a DataFrame with the first 5 principal components
# Naming the columns as PC1, PC2, ..., PC5
pc_columns = [f'PC{i+1}' for i in range(5)]
pca_df = pd.DataFrame(pca_data[:, :5], columns=pc_columns)

# Save the DataFrame to a CSV file
pca_df.to_csv('pca_output.csv', index=False)
print("Data with the first 5 principal components saved to 'pca_output.csv'")

pca_df.head(5)

"""We expect these new features to be orthogonal to each other. Check this and show the correlation between the features."""

# todo
# Assuming `pca_df` is the DataFrame containing the principal components
# Calculate the correlation matrix of the principal components
correlation_matrix = pca_df.corr()

# Plot the correlation matrix as a heatmap
plt.figure(figsize=(20, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
plt.title("Correlation Matrix of Principal Components")
plt.show()

"""## KMeans (45 points)
Implement kmeans from scratch.
"""

import numpy as np

class CustomKMeans:
    def __init__(self, n_clusters=3, max_iter=100, random_state=42):
        """
        Initialize the KMeans class with the number of clusters and maximum iterations.
        n_clusters: Number of clusters to form.
        max_iter: Maximum number of iterations for convergence.
        random_state: Seed for reproducibility.
        """
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.centroids = None
        self.inertia_ = None
        self.labels_ = None

    def fit(self, X):
        """
        Fit the KMeans model on the dataset X.
        X: Input data (n_samples, n_features)
        """
        np.random.seed(self.random_state)
        n_samples = X.shape[0]

        # Step 1: Initialize centroids randomly from data points
        random_indices = np.random.choice(n_samples, self.n_clusters, replace=False)
        self.centroids = X[random_indices]

        for i in range(self.max_iter):
            # Step 2: Assign clusters
            self.labels_ = self._assign_clusters(X)

            # Step 3: Calculate new centroids
            new_centroids = np.array([X[self.labels_ == j].mean(axis=0) for j in range(self.n_clusters)])

            # Check for convergence (if centroids do not change)
            if np.allclose(self.centroids, new_centroids):
                break

            self.centroids = new_centroids

        # Calculate final inertia
        self.inertia_ = self._calculate_inertia(X)
        return self

    def _assign_clusters(self, X):
        """
        Assign each data point to the nearest centroid.
        X: Input data (n_samples, n_features)
        Returns: Array of cluster assignments for each data point
        """
        distances = np.array([np.linalg.norm(X - centroid, axis=1) for centroid in self.centroids])
        return np.argmin(distances, axis=0)

    def _calculate_inertia(self, X):
        """
        Calculate the within-cluster sum of squared distances (inertia).
        X: Input data (n_samples, n_features)
        Returns: inertia (float)
        """
        inertia = 0.0
        for i in range(self.n_clusters):
            # Sum squared distances between points and their corresponding centroid
            cluster_points = X[self.labels_ == i]
            inertia += np.sum((cluster_points - self.centroids[i]) ** 2)
        return inertia

    def predict(self, X):
        """
        Predict the closest cluster each sample in X belongs to.
        X: Input data (n_samples, n_features)
        Returns: Cluster assignments for each data point
        """
        return self._assign_clusters(X)

"""### Elbow Method
Apply the elbow method to determine the optimal number of clusters for K-Means. what is the best number of clusters?
"""

import matplotlib.pyplot as plt

# Initialize an empty list to store the WCSS values for each number of clusters
WCSS = []
# Apply KMeans for a range of cluster values (from 1 to 30)
for i in range(1, 30):
    # Initialize the CustomKMeans with `i` clusters and a random state of 42
    kmeans_pca = CustomKMeans(n_clusters=i, random_state=42)

    # Fit the model to the PCA-transformed data
    kmeans_pca.fit(pca_df.values)  # Assuming `data_pca` is the PCA-transformed data

    # Append the calculated inertia (WCSS) to the WCSS list
    WCSS.append(kmeans_pca.inertia_)

print('optimal k =', WCSS.index(min(WCSS)))

# Plot the Elbow curve using Matplotlib
plt.figure(figsize=(10, 6))
plt.plot(range(1, 30), WCSS, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Within-Cluster Sum of Squares (WCSS)')
plt.title('Elbow Method for Optimal K')
plt.show()

"""Apply the optimal KMeans clustering on the PCA-transformed data, and assign cluster labels to each observation. Add a new column named segment to the df_pca DataFrame to store these labels."""

# Apply KMeans on PCA-reduced data with the optimal number of clusters based on the elbow method
optimal_k = 28

# Initialize KMeans with the optimal number of clusters
kmeans_optimal = CustomKMeans(n_clusters=optimal_k, random_state=42)

# Fit the model to the PCA-transformed data
kmeans_optimal.fit(pca_df.values)

# Add a new column 'segment' to pca data frame and assign the cluster labels to each observation
# Assign the cluster labels to each observation
cluster_labels = kmeans_optimal.labels_

pca_df['segment'] = cluster_labels
# Display the first few rows of the updated DataFrame
print(pca_df.head())

""" visualize the clustering by plotting the pairwise relationships of the PCA-reduced features, color-coded by the cluster assignments."""

sns.pairplot(pca_df, hue='segment', palette='tab10', diag_kind='kde')

# Show plot
plt.suptitle("Pairwise Relationships of PCA-Reduced Features, Colored by Cluster", y=1.02)
plt.show()

"""So, when we employ PCA prior to using K-means we can visually separate almost the entire data set. That was one of the biggest goals of PCA - to reduce the number of variables by combining them into bigger, more meaningful features.

### Hierarchical Clustering
Perform hierarchical clustering on the reduced dataset after PCA. Use complete linkage method.
"""

import scipy.cluster.hierarchy as sch
# Perform Hierarchical Clustering on the pca dataset
scaler = StandardScaler()
scaled_pca_data = scaler.fit_transform(pca_df)
linked = sch.linkage(scaled_pca_data, method='ward')

# Visualize the dendrogram
plt.figure(figsize=(10, 7))
sch.dendrogram(linked)

plt.title('Dendrogram for Hierarchical Clustering')
plt.xlabel('Samples')
plt.ylabel('Distance')
plt.show()

""""Use scipy.cluster.hierarchy.fcluster to assign clusters from the dendrogram with a specified number of 5 clusters. Then visualize the results using pairplots."""

# Choose threshold and assign clusters
clusters = sch.fcluster(linked, t=5, criterion='maxclust')

# Step 4: Add the cluster labels to the PCA DataFrame
pca_df['hierarchical_cluster'] = clusters

# Step 5: Visualize the clustering results using pairplot (pairwise relationships of PCA components)
sns.pairplot(pca_df, hue='hierarchical_cluster', palette='tab10', diag_kind='kde')

# Show plot with title
plt.suptitle("Pairwise Relationships of PCA-Reduced Features, Colored by Hierarchical Clusters", y=1.02)
plt.show()
