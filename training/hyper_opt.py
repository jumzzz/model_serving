from bayes_opt import BayesianOptimization

import lightgbm as lgb
import pandas as pd


def tune_lgb_hyperparams(X,y, init_round=15, opt_round=25, n_folds=3):
    # prepare data
    train_data = lgb.Dataset(data=X, label=y, free_raw_data=False)
    
    # parameters
    def lgb_eval(learning_rate,num_leaves, feature_fraction, bagging_fraction, max_depth, max_bin, min_data_in_leaf,min_sum_hessian_in_leaf,subsample):
        params = {
            'application':'binary', 
            'metric':'auc',
            'learning_rate' : max(min(learning_rate, 1), 0),
            'num_leaves' : int(round(num_leaves)),
            'feature_fraction' : max(min(feature_fraction, 1), 0),
            'bagging_fraction' : max(min(bagging_fraction, 1), 0),
            'max_depth' : int(round(max_depth)),
            'max_bin' : int(round(max_bin)),
            'min_data_in_leaf' : int(round(min_data_in_leaf)),
            'min_sum_hessian_in_leaf' : min_sum_hessian_in_leaf,
            'subsample' : max(min(subsample, 1), 0)
        }

        cv_result = lgb.cv(params, train_data, nfold=n_folds, stratified=True, verbose_eval=False, metrics=['auc'])
        return max(cv_result['auc-mean'])

    hyper_bounds = {
            'learning_rate': (0.01, 1.0),
            'num_leaves': (24, 80),
            'feature_fraction': (0.1, 0.9),
            'bagging_fraction': (0.8, 1),
            'max_depth': (5, 30),
            'max_bin':(20,90),
            'min_data_in_leaf': (20, 80),
            'min_sum_hessian_in_leaf':(0,100),
            'subsample': (0.01, 1.0)
    }
    
    lgb_bayes_opt = BayesianOptimization(lgb_eval, hyper_bounds)
    lgb_bayes_opt.maximize(init_points=init_round, n_iter=opt_round)
    
    model_auc=[]
    for model in range(len(lgb_bayes_opt.res)):
        model_auc.append(lgb_bayes_opt.res[model]['target'])
    
    # return best parameters

    params = (
        lgb_bayes_opt.res[pd.Series(model_auc).idxmax()]['target'], 
        lgb_bayes_opt.res[pd.Series(model_auc).idxmax()]['params']
    )

    return parse_parameters(params)


def parse_parameters(opt_params):

    opt_params[1]["num_leaves"] = int(round(opt_params[1]["num_leaves"]))
    opt_params[1]['max_depth'] = int(round(opt_params[1]['max_depth']))
    opt_params[1]['min_data_in_leaf'] = int(round(opt_params[1]['min_data_in_leaf']))
    opt_params[1]['max_bin'] = int(round(opt_params[1]['max_bin']))
    opt_params[1]['objective']='binary'
    opt_params[1]['metric']='auc'
    opt_params[1]['is_unbalance']=True
    opt_params[1]['boost_from_average']=False
    opt_params=opt_params[1]
    
    return opt_params

