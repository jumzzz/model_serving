import argparse
import pandas as pd

from preprocess import DataTransformer
from hyper_opt import tune_lgb_hyperparams
from utils import split_ds, feats_label_cols, evaluate_model, save_model_transformer

import lightgbm as lgb


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('src', help='Source CSV File of Adult Census Income dataset.')
    parser.add_argument('dst', help='Destination directory for data_transformer pickle and LGBM Model File')
    args = parser.parse_args()

    return args


def load_transform_ds(path, data_transformer):
    df = pd.read_csv(path)
    df = df.applymap(lambda s:s.lower() if type(s) == str else s)

    df_transform = data_transformer.fit_transform(df)
    df_transform = df_transform.sample(frac=1.0).reset_index(drop=True)

    return split_ds(df_transform)


def train_lgbm(df_tr, df_val, df_ts, opt_hparam, feats_col, label_col):
    
    tr_data = lgb.Dataset(df_tr[feats_col], label=df_tr[label_col])
    val_data = lgb.Dataset(df_val[feats_col], label=df_val[label_col])
    ts_data = lgb.Dataset(df_ts[feats_col], label=df_ts[label_col])

    num_round = 15000

    clf = lgb.train(opt_hparam, 
                    tr_data, 
                    num_round, 
                    valid_sets = [tr_data, val_data, ts_data], 
                    verbose_eval=True, 
                    early_stopping_rounds = 250)

    return clf


def main():
    args = get_args()
    data_transformer = DataTransformer()

    df_tr, df_val, df_ts = load_transform_ds(args.src, data_transformer)
    feats_col, label_col = feats_label_cols(df_tr)

    print('Tuning of LGBM HyperParameters using Bayesian Optimization')
    opt_hparam = tune_lgb_hyperparams(df_tr[feats_col], df_tr[label_col])

    print('')
    print('Training LGBM with Optimized Hyperparameters')

    clf = train_lgbm(df_tr, df_val, df_ts, opt_hparam, feats_col, label_col)

    print('')
    print('Evaluating Model')
    evaluate_model(clf, df_val, df_ts, feats_col, label_col)

    print('')
    print(f'Saving Model and Transformer to Directory {args.dst}')

    pickle_path, model_path = save_model_transformer(clf, data_transformer, args.dst)

    print('Pickle Saved to ', pickle_path)
    print('Model Saved to ', model_path)



if __name__ == '__main__':
    main()