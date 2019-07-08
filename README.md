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

## Sub Task 2
In addition to detecting offensive language tweets, we distinguish between three subcategories:

1. PROFANITY: usage of profane words, however, the tweet clearly does not want to insult anyone.

2. INSULT: unlike PROFANITY the tweet clearly wants to offend someone.

3. ABUSE: unlike INSULT, the tweet does not just insult a person but represents the stronger form of abusive language

We used 6 neural network architectures with German fasttext embeddings.
Provide the necessary config in sub_task_2_model_config section in config.txt file and run the run_experiment_sub_task_2.py file.

| Model              | Precision | Recall| F1     |
| :-----------------:|---------: | -----:| -----: |
| Capsule            | 0.705     | 0.732 | 0.698  |
| CNN                | 0.708     | 0.735 | 0.695  |
| Pooled GRU         | 0.688     | 0.724 | 0.679  |
| Attention LSTM     | 0.687     | 0.716 | 0.677  |
| Attention LSTM GRU | 0.687     | 0.721 | 0.684  |
| Attention Capsule  | 0.685     | 0.718 | 0.680  |

## Sub Task 3
In addition to detecting offensive language tweets, we distinguish between two subcategories:

1. EXPLICIT: an offensive tweet which directly expresses hate, condemnation, superiority towards an explicitly or implicitly given target

2. IMPLICIT:  an offensive tweet where the expression of hate, condemnation, superiority etc. as directed towards an explicitly or implicitly given target has to be inferred from the ascription of (hypothesized) target properties that are insulting, degrading, offending, humiliating etc.

 

Subtask III is cast as a two-way classification task where a tweet either is explicit offensive (EXPLICIT) or implicit offensive (IMPLICIT).
We used 6 neural network architectures with German fasttext embeddings.
Provide the necessary config in sub_task_3_model_config section in config.txt file and run the run_experiment_sub_task_3.py file.

| Model              | Precision | Recall| F1     |
| :-----------------:|---------: | -----:| -----: |
| Capsule            | 0.840     | 0.787 | 0.887  |
| CNN                | 0.839     | 0.802 | 0.817  |
| Pooled GRU         | 0.852     | 0.831 | 0.840  |
| Attention LSTM     | 0.828     | 0.803 | 0.813  |
| Attention LSTM GRU | 0.827     | 0.792 | 0.806  |
| Attention Capsule  | 0.823     | 0.771 | 0.792  |


