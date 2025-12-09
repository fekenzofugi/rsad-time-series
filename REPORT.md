# Remote Sensing Anomaly Detection in Time-Series Imagery

# Abstract
The use of plastic in agriculture has increased significantly in recent years, bringing both benefits and environmental challenges. While agricultural plastics improve crop yields and resource efficiency, they also lead to the accumulation of plastic waste in rural areas. Remote Sensing (RS) data, combined with advanced machine learning and computer vision techniques, provide an effective means to monitor plasticulture dynamics. Therefore, this research internship aims to explore RS anomaly detection (RSAD) techniques in time-series imagery and apply them to agricultural monitoring, particularly in detecting subtle cases that involve spectral changes such as material deterioration and pest-related disturbances Therefore, I'll join researchers at the University of Sheffield to learn RSAD techniques in the agriculture context and then explore whether they can be applied in plasticulture. In parallel, I'll collaborate with researchers at the University of Sheffield and contribute to the PEZEGO pest-management app. The internship will provide hands-on experience in scalable application design, app optimization, and model integration, which can enhance our ongoing application, GeoHuman. The University of Sheffield was chosen due to its internationally recognized expertise in application development, machine learning, computer vision, and remote sensing. This experience will strengthen our project in Brazil by improving the accuracy and scalability of agricultural monitoring systems. Upon my return, I will disseminate the knowledge gained through workshops and collaborative activities with my research group at UNICAMP to foster innovation and capacity building in remote sensing applications. 

# 1. Short Review of Methods (December 01 - January 01)

On the search of anomaly detection models to use in agriculture to detect plasticulture subtle changes and pest detection in seedcorn. I've found out the distance mahalanobis metric. But first, what is an anomaly?

## 1.1 What is an anomaly?

Anomaly is a somekind of a rare event that occurs in a time-series sequence. In my case, given a Sentinel-2 time-series the anomaly is the ```pest-net``` on plasticulture and the ```pests-attacks``` in the seedcorn.

An anomaly = pest-net damage on plasticulture

An anomaly = pest attacks in seedcorn fields

Ok, we now know the anomalies of our project, but ```HOW DO WE ACTUALLY DETECT THESE ANOMALIES?``` In order to detect these anomalies, we need a anomaly detection model which is trained on labeled anomalies data. We need to first label these anomalies in the satellite image and then train our model.

## 1.2 Labeling Data

To label the data we're going to use our application Geohuman which was made to accuratly label Sentinel-2 time-series imagery.

## 1.3 Anomaly Detection Model
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

## 2.1 Pipeline
<ol>
<li><strong>Data Preprocessing</strong></li>
<li><strong>Feature extraction</strong>: is the process of transforming raw, high-dimensional data into a more concise and informative set of numerical features</li>
<li><strong>Normal Behavior (Without Pests)</strong>: Define the normal behavior without any anomalies.</li>
<li><strong>Mahalanobis</strong>:
For instance, let’s consider a scenario where a research team wants to identify potential pest outbreaks in corn crops using Sentinel-2 satellite time-series. The team collects data on various spectral variables such as vegetation indices, reflectance values across multiple bands, temporal growth patterns, and other environmental indicators derived from the satellite imagery. It then uses Mahalanobis Distance to measure how far each observation in the time-series deviates from the expected multivariate behavior of healthy crops. By doing this, it can identify points in time and space that are significantly different from the normal crop conditions — subtle spectral changes that may indicate early pest attacks or crop stress. This allows the team to detect anomalies rapidly and provide early warnings for targeted interventions in the field.

For each pixel i: 

$$D_i = \sqrt{(X_i - \mu)^T \Sigma^{-1} (X_i - \mu)}$$

Where 

$X_i$ is a single sample (image). A temporal feature vector for a single pixel over time. It contains the values you want to test for anomalies.

$\mu$ is the average of all normal observations.

${X_i - \mu}$ It measures how much the sample deviates from normal conditions.

$\Sigma$ Covariance Matrix captures how the variables co-vary.

$\Sigma^{-1}$: Inverse Covariance Matrix

A deviation along a high-variance direction = less suspicious

A deviation along a low-variance direction = more suspicious

**HIGH D** → strange behavior → possibility for pests

**LOW D** → normal behavior
</li>

<li><strong>Validation</strong>: Compare the results with our labeled anomalies</li>
</ol>

## 2.2 Summary

It generates an **anomaly map per pixel**, normally called an **Anomaly Score Map** or **Mahalanobis Heatmap**.

For each Sentinel-2 pixel, the model:

1. looks at that pixel's time series
2. compares it with the learned "normal behavior"
3. calculates the Mahalanobis distance
4. if the distance is high → marks as anomaly
5. if the distance is low → marks as normal

## 2.3 Applied to Agriculture

### Plasticulture / pest-net
* Plastic usually reflects in a stable manner
* If something appears underneath or on top (insect web, etc.) → distorts the pattern → pixel marked as anomaly

### Seedcorn / pests
* Abrupt drop in NDVI
* Early change in phenology
* Alteration in photometric pattern → pixels marked as anomaly

## 🗺️ What the final map looks like

Imagine a raster with values:
* **0** = normal
* **1** = anomaly (regions suspected of pests)

## 2.4 Challenges
Many studies have revealed the effectiveness of satellite
images in monitoring crop diseases and insect pests. Unfortu-
nately, the long revisit period, low spatial resolution, and the
requirements for clear weather of satellite images hampered
monitoring the armyworm damage because the armyworm
would break out in a very short time.

## References
https://scijournals.onlinelibrary.wiley.com/doi/pdf/10.1002/ps.6852?utm_source=clarivate&getft_integrator=clarivate




# 3. Application Development (January 01 - March 01)

# 4. Documentation (March 01 - March 30)