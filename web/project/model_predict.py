import lightgbm as lgb
from utils import load_pickle
import pandas as pd
import numpy as np

class Model:

    def __init__(self, model_file, transformer_file):

        self.model = lgb.Booster(model_file=model_file)
        self.transformer = load_pickle(transformer_file)

    def predict(self, payload: dict):
        df_payload = pd.DataFrame([payload])
        df_transform = self.transformer.transform_features(df_payload)
        pred_raw = self.model.predict(df_transform)
        pred_readable = np.where(pred_raw > 0.5, '>50k', '<=50k')

        pred_raw = pred_raw.tolist()[0]
        pred_readable = pred_readable.tolist()[0]
        
        return {
            'status' : 'success',
            'prediction_raw' : pred_raw,
            'predicted_income_class' : pred_readable 
        }



