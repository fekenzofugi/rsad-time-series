# Remote Sensing Anomaly Detection in Time-Series Imagery

# Abstract
The use of plastic in agriculture has increased significantly in recent years, bringing both benefits and environmental challenges. While agricultural plastics improve crop yields and resource efficiency, they also lead to the accumulation of plastic waste in rural areas. Remote Sensing (RS) data, combined with advanced machine learning and computer vision techniques, provide an effective means to monitor plasticulture dynamics. Therefore, this research internship aims to explore RS anomaly detection (RSAD) techniques in time-series imagery and apply them to agricultural monitoring, particularly in detecting subtle cases that involve spectral changes such as material deterioration and pest-related disturbances Therefore, I'll join researchers at the University of Sheffield to learn RSAD techniques in the agriculture context and then explore whether they can be applied in plasticulture. In parallel, I'll collaborate with researchers at the University of Sheffield and contribute to the PEZEGO pest-management app. The internship will provide hands-on experience in scalable application design, app optimization, and model integration, which can enhance our ongoing application, GeoHuman. The University of Sheffield was chosen due to its internationally recognized expertise in application development, machine learning, computer vision, and remote sensing. This experience will strengthen our project in Brazil by improving the accuracy and scalability of agricultural monitoring systems. Upon my return, I will disseminate the knowledge gained through workshops and collaborative activities with my research group at UNICAMP to foster innovation and capacity building in remote sensing applications. 

# 1. Short Review of Methods (December 01 - January 01)

On the search of anomaly detection models to use in agriculture to detect plasticulture subtle changes and pest detection in seedcorn.

## 1.1 What is an anomaly?

Anomaly is a somekind of a rare event that occurs in a time-series sequence. In my case, given a Sentinel-2 time-series the anomaly is the ```pest-net``` on plasticulture and the ```pests-attacks``` in the seedcorn.

An anomaly = pest-net damage on plasticulture

An anomaly = pest attacks in seedcorn fields

Ok, we now know the anomalies of our project, but ```HOW DO WE ACTUALLY DETECT THESE ANOMALIES?``` In order to detect these anomalies, we need a anomaly detection model which is trained on labeled anomalies data. We need to first label these anomalies in the satellite image and then train our model.

## 1.2 Anomaly Detection Model
An anomaly detection model is a computational method designed to identify patterns that deviate from what is considered normal in a dataset.

In other words, the model learns the typical (baseline) behavior of the system and then flags anything that does not fit that baseline.

Key characteristics of anomaly detection models:

* They learn “normality.” The model is trained on historical or representative data assumed to be normal.

* They detect deviations.
Anything significantly different from the learned baseline is marked as an anomaly.

* They do not require explicit anomaly labels.
Many anomaly detection methods are unsupervised, meaning they only need normal data.
(Supervised anomaly detection is possible but requires labeled anomalies, which are rare.)

* They can work on images, time series, or multivariate signals.
This includes Sentinel-2 bands, vegetation indices, red-edge temporal profiles, etc.

In remote sensing:

* An anomaly detection model identifies places or times where the satellite signal shows abnormal spectral or temporal behavior, such as:

* sudden drop in NIR reflectance (vegetation stress)

* abnormal increase in red reflectance

* changes in red-edge curvature

* unexpected soil exposure

* subtle changes in plasticulture structure

* spectral signatures inconsistent with historical behavior

An anomaly detection model learns the normal Sentinel-2 signature of these fields and highlights pixels that deviate from that pattern.

# 2. Anomaly Detection Models (December 01 - March 01)
I'm researching armyworm pests in the region of Ghana. I'm having a difficult time finding the pattern of the crops through time-series vegetation indexes such as NDVI and EVI. Therefore, a approach that urged is that we use a unsupervised method to classify each pixel and suppose that its a gaussian distribution and the pixels that deviate we associate with different colors, creating a heatmap of the region, with each color indicating its class.

## 2.1 Pipeline
<ol>
<li><strong>Data Preprocessing</strong></li>

<li><strong>Feature extraction</strong>: is the process of transforming raw, high-dimensional data into a more concise and informative set of numerical features</li>

<li><strong>Normal Behavior (Without Pests)</strong>: Define the normal behavior without any anomalies.</li>

<li><strong>Unsupervised Learning pixel-based time-series</strong>:
1. Normalize the time-series spectral response from the pixels. In that way the climate effects (happens gloabaly) gets reduced and the anomalies (which happens localy) gets preserved in the pixels. That way we can limitate our analysis to anomalies in a single crop field with thw normalized data, increasing the confidence that its anomalies observed are pest-attacks.
2. Create a time-series feature vector of each pixel.
3. Make a clustering in unlabeled data.
</li>

<li><strong>Validation</strong>: Compare the results with our labeled anomalies</li>
</ol>

## 2.2 Unsupervised Learning

```What is Unsupervised Learning?``` Given a dataset, our training set looks like this

$${{x^1, x^2, x^3, ...}}$$

without a target label. Because we don't have a target label in this method, we're not able to tell the algorithm the 'right answser' y that we want to predict. Instead we're going to ask the algorithm to find some interesting structure about the data. This explains why Jefersson suggested the spatial-temporal approach to detect the pest-attacks.

One of the first unsupervised algorithms that we learn is called ```clustering```

### 2.2.1 What is Clutering?
Clustering mainly receives a dataset of unlabeled data and try to separate into clusters, which are group of points that are similar to each other.

### 2.2.2 K-Means Algorithm
Randomly initialize K cluster centroids $${{\mu^1, \mu^2, \mu^3, ... , \mu^K}}$$

```
Repeat{
    # Assign m sample points to cluster centroids
    for i = 1 to m:
        c_i = index of cluster centroid closer to x_i. (distance between two points)
            Where looking for the c_i = min k ||x_i - u_k||^2, value of k that minimizes
            the k value.
    # Move cluster centroids
    for k = 1 to K:
        u_k = mean of points assigned to cluster k.
}
```

## References
https://scijournals.onlinelibrary.wiley.com/doi/pdf/10.1002/ps.6852?utm_source=clarivate&getft_integrator=clarivate