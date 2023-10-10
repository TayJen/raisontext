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
# %load_ext autoreload
# %autoreload 2
import pandas as pd

import sys
sys.path.append('../../..')

from raisontext import config
from raisontext.dev.train.tf_idf_log_reg import TfIdfLogReg
# -

DATA_DIR = config.REPO_ROOT / 'data'
MODELS_DIR = config.REPO_ROOT / 'models'

train_df = pd.read_parquet(DATA_DIR / 'mgt_dataset_train.parquet')
test_df = pd.read_parquet(DATA_DIR / 'mgt_dataset_test.parquet')

baseline_m = TfIdfLogReg('first silly baseline')
baseline_m.fit(train_df.head(100))
baseline_m.predict(test_df.head(5)['text'].to_list())

baseline_m.save(MODELS_DIR)
