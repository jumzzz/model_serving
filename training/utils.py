import pandas as pd

from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
import numpy as np
import os
import cloudpickle


def split_ds(df):

    tr_idx = df.shape[0] * 80 // 100
    val_idx = df.shape[0] * 90 // 100

    df_tr = df[0:tr_idx].reset_index(drop=True)
    df_val = df[tr_idx:val_idx].reset_index(drop=True)
    df_ts = df[val_idx:].reset_index(drop=True)

    return df_tr, df_val, df_ts


def feats_label_cols(df):
    feats = [col for col in df.columns if col != 'income']
    label = 'income'
    return feats, label


def evaluate_on_ds(clf, df, feats_col, label_col, msg):

    y_pred = clf.predict(df[feats_col])
    y_pred = np.where(y_pred > 0.5, 1.0, 0.0)

    acc_score_ = accuracy_score(df[label_col], y_pred)
    prec_score_ = precision_score(df[label_col], y_pred)
    rec_score_ = recall_score(df[label_col], y_pred)
    f1_score_ = f1_score(df[label_col], y_pred)

    print('###########################################################')
    print(f'Accuracy Score for {msg} = {acc_score_}')
    print(f'Precision Score for {msg} = {prec_score_}')
    print(f'Recall Score for {msg} = {rec_score_}')
    print(f'F1 Score for {msg} = {f1_score_}')
    print('###########################################################')
    

def evaluate_model(clf, df_val, df_ts, feats_col, label_col):
    evaluate_on_ds(clf, df_val, feats_col, label_col, msg='Validation Set')
    evaluate_on_ds(clf, df_ts, feats_col, label_col, msg='Test Set')


def make_dir(target_dir):
    if os.path.isdir(target_dir):
        return
    os.mkdir(target_dir)


def save_pickle(obj, path):
    with open(path, 'wb') as f:
        cloudpickle.dump(obj, f)


def save_model(model, path):
    model.save_model(path, num_iteration=model.best_iteration)


def save_model_transformer(clf, data_transformer, dst_dir):
    make_dir(dst_dir)

    pickle_path = os.path.join(dst_dir, 'data_transformer.pkl')
    model_path = os.path.join(dst_dir, 'model.txt')

    save_pickle(data_transformer, pickle_path)
    save_model(clf, model_path)

    return pickle_path, model_path

    
