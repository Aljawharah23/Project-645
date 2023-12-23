Project-645
Our project Detection of Duplicate Textual Bug Reports is using SANER-19 dataset available here: Replication package: https://drive.google.com/file/d/1ywH1LqGCXEQ1ij_g-PZAHmvf5Hc-MNo0/view?usp=drivesdk

This project aims to identify duplicate bug reports using machine learning models. It involves preprocessing data, generating embeddings, and fine-tuning models for enhanced accuracy.

Dataset: The dataset is split into training and testing sets using Split_data_80_20.py.

preprocess_data.py scripts clean and prepare the data for model ingestion.

Ground Truth Placeholder: GT_Placeholder.py compiles a list of bug reports and their duplicates.

SentBert Model: The SentBert model generates embeddings for textual data.

Positive-Negative Pairing: Negative-Positive.py constructs pairs for training the model. positive-negative-evaluate.py Used to run the see the Performance Metrics of the model.

Fine-Tuning: Fine_tune.py refines the model parameters for better performance.

Results: The results of the project processes are included within folders. Each folder contains output files relevant to its respective stage of the workflow.
https://github.com/Aljawharah23/Project-645/tree/Output


@Aljawharah
