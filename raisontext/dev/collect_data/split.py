# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import pandas as pd

import sys
sys.path.append('../../..')

from raisontext import config
# -

# config
DATA_DIR = config.REPO_ROOT / 'data'

train_eval_df = pd.read_parquet(DATA_DIR / 'mgt_dataset.parquet')

train_eval_df.head()

train_eval_df['text']

train_eval_df.drop(columns='text').value_counts()

# +
from sklearn.model_selection import train_test_split

_train, _test = train_test_split(train_eval_df, test_size=0.2, random_state=42, shuffle=True,
                 stratify=train_eval_df['generator'].astype(str) + ' ' + train_eval_df['source'])
# -

_train.shape, _test.shape

_train.to_parquet(DATA_DIR / 'mgt_dataset_train.parquet')
_test.to_parquet(DATA_DIR / 'mgt_dataset_test.parquet')

_train.head()
