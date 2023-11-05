# RaisonText

RaisonText is an open-source AI library for synthetic (e. g. chatGPT-generated) text detection.

## Data

We collected and generated 941k samples of human-written (33%) and AI-generated (67%) texts.

Public datasets used:

- [GPT-wiki-intro](https://huggingface.co/datasets/aadityaubhat/GPT-wiki-intro)
- [DeepfakeTextDetect](https://github.com/yafuly/DeepfakeTextDetect)
- [TuringBench](https://huggingface.co/datasets/turingbench/TuringBench/tree/main)

Generative models used:

- Chat-GPT
- opt-125m
- opt-1.3b
- opt-2.7b
- llama2-7b
- llama2-13b

Source name saved in source column.

Dataset may be downloaded [here](https://drive.google.com/file/d/1PQxFbcEoH7Md7SM5d8fJv1k1B3sfbG-j/view?usp=sharing).

Part of generated data publiched on [HuggingFace](https://huggingface.co/datasets/yatsy/GPT-wiki-intro-extension).

## Prediction baseline

We reached 0.96 roc_auc score with baseline [model](https://drive.google.com/file/d/16_QvtMvPr8CtetFDoFIVIYz7alw520ZQ/view?usp=sharing). Exract archive into repo root folder.
