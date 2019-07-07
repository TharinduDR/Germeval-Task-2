# Germeval Task 2, 2019 — Shared Task on the Identification of Offensive Language

This repository contains the code of RGCL's submission for Germeval Task 2 2019. 

Offensive language is commonly defined as hurtful, derogatory or obscene comments made by one person to another. This type of language can increasingly be found on the web. As a consequence many operators of social media websites no longer manage to manually monitor user posts. Therefore, there is a pressing demand for methods to automatically identify suspicious posts.

This second shared task on the topic is to intensify research on the identification of offensive content in German language microposts. Offensive comments are to be detected from a set of German tweets.

## Sub Task 1
The task is to decide whether a tweet includes some form of offensive language or not.
We used 6 neural network architectures with German fasttext embeddings.
Provide the necessary config in sub_task_1_model_config section in config.txt file and run the run_experiment_sub_task_1.py file.

| Model              | Precision | Recall| F1     |
| :-----------------:|---------: | -----:| -----: |
| Capsule            | 0.774     | 0.767 | 0.743  |
| CNN                | 0.769     | 0.764 | 0.740  |
| Pooled GRU         | 0.762     | 0.756 | 0.728  |
| Attention LSTM     | 0.750     | 0.748 | 0.720  |
| Attention LSTM GRU | 0.764     | 0.756 | 0.720  |
| Attention Capsule  | 0.757     | 0.751 | 0.721  |

