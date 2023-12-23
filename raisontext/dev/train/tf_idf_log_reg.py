from typing import List
import pickle
import os
from raisontext.dev.train.base import Model
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path
import logging
# import wandb

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class TfIdfLogReg(Model):
    def __init__(self, descr: str, wandb_log=True, run_name: str = ''):
        super().__init__(descr=descr, wandb_log=wandb_log, run_name=run_name)
        if self.wandb:
            # wandb.config.update({
            #     'model': 'TfIdfLogReg',
            #     'descr': self.descr,
            #     'hash': self.hash,
            #     'hyperparams': {'ngram_range': (1, 2), 'min_df': 5, 'max_features': 2**21},
            # })
            pass

        self.model = None

    def __str__(self):
        print(self.descr)

    def fit(self, train_df):
        if self.wandb:
            # wandb.log({'train_size': len(train_df)})
            pass

        train_train_X = train_df['text']
        train_train_Y = train_df["is_generated"]

        vect = TfidfVectorizer(ngram_range=(1, 2), min_df=5, max_features=2**21)
        model = LogisticRegression(solver='liblinear')

        m = Pipeline([('tf-idf', vect), ('log-reg', model)])
        m.fit(train_train_X, train_train_Y)

        self.model = m
        if self.wandb:
            self.wandb_run.finish()

    def predict(self, texts: List[str]) -> List[float]:
        return self.model.predict_proba(texts)[:, 1]

    def save(self, destination: Path):
        dir_path = destination / f'TfIdfLogReg_{self.descr}'
        isExist = os.path.exists(dir_path)
        if not isExist:
            os.makedirs(dir_path)
        file_name = str(self.hash) + '.pkl'
        with open(dir_path / file_name, 'wb') as handle:
            pickle.dump(self, handle, protocol=5)
        logger.info(f'Saved into {str(dir_path / file_name)}')

    def load(self, weights_path: str):
        if self.model is None:
            self.model = pickle.load(open(weights_path, 'rb'))
        print("Model is loaded")
