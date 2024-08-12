# Clustering of Electronic Health Records for Speeding Medical Analysis Using NLP Techniques

## Overview

This project, conducted as a part of my Bachelor of Science degree with a double major in Mathematics and Computer Science, focuses on the clustering of Electronic Health Records (EHRs) to expedite medical analysis. The project was completed under the supervision of PhD Marwa Dridi and Mr. Amine Ferdjaoui at SogetiLabs, a research lab within Capgemini.

## Objective

The primary objective of this project was to develop a Natural Language Processing (NLP) pipeline capable of analyzing and clustering EHRs. By grouping records from patients with similar conditions, the goal was to accelerate the examination process by medical professionals, thereby reducing patient wait times and improving hospital workflow efficiency.

## Data

The dataset used in this project was sourced from the N2C2 (National NLP Clinical Challenges) hosted by Harvard Medical School. The data consists of deidentified EHRs spanning multiple years and various medical challenges. In total, the dataset includes over 8,000 records from diverse medical contexts.

## Methodology

The project was structured into three main phases:

1. **Data Preprocessing:**
   - **Data Cleaning:** The EHRs were cleaned using the SpaCy library to remove stop words, punctuation, and other irrelevant data.
   - **Word Embeddings:** Techniques such as Bag of Words (BoW), Term Frequency-Inverse Document Frequency (TF-IDF), and Word2Vec were employed to convert textual data into numerical representations that a machine learning model can understand.

2. **Clustering:**
   - **Latent Dirichlet Allocation (LDA):** This unsupervised machine learning technique was used to identify topics within the documents and group them accordingly. The model was fine-tuned using the Elbow Method to determine the optimal number of clusters.
   - **K-Means Clustering:** To validate the results from LDA, K-Means clustering was also applied, yielding similar groupings of the documents.

3. **Evaluation:**
   - The effectiveness of the clustering was evaluated based on the coherence of the topics and their relevance to specific medical conditions, such as surgical procedures or pregnancy.

## Results

The project successfully clustered the EHRs into coherent groups, which can be used by healthcare professionals to quickly access records of patients with similar conditions. This clustering mechanism has the potential to significantly reduce the time taken to examine patients, thus improving overall hospital efficiency.

## Future Work

Future work could expand the scope of this project by:
- Extending the analysis to include EHRs from other countries.
- Implementing supervised learning models for more accurate classification.
- Predicting patient Length of Stay (LOS) using the clustered data, which could aid in hospital resource management.

## Conclusion

This project demonstrates the potential of NLP techniques in the healthcare sector, particularly in speeding up medical analysis through effective clustering of patient records. The pipeline developed in this study can be scaled and adapted for broader applications, potentially benefiting various other sectors beyond healthcare.



## Repository Structure
This repository contains the following files and folders:

- /Data/: This folder contains the processed datasets used in the project. The data has been preprocessed and cleaned to ensure consistency across all records.

- /HeXplore/: This folder contains the files used to process the data from raw .txt files to csv files.

- /Discovery/: This folder contains Jupyter Notebooks that were used to conduct some Exploratory Data Analysis and tests on the data.

- /Models/: Saved models generated during the training process. This folder includes the trained LDA and K-Means models that can be used to cluster new data.

- README.md: The file you are currently reading, which provides an overview of the project, its objectives, methodology, and instructions for using the repository.

requirements.txt: A list of Python packages and dependencies required to run the code in this repository. You can install them using pip install -r requirements.txt.

LICENSE: The license under which this project is distributed. Make sure to review it before using or distributing the code.