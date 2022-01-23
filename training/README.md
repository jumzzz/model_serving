# Training Module 

To install the dependencies first

```
pip install -r requirements.txt
```

Then to start training a model and generating preprocessing pickle, simply

```
python train.py adult.csv model/
```
The model and preprocessing pickle will be located at 

```
model/model.txt
model/data_transformer.pkl
```

## The training script roughly does the following
- Preprocess/Transform Dataframe (Feature Engineered Transformation)
- Perform Hyperparameter Tuning (With the help of Bayesian Optimization)
- Train LightBGM Model with Tuned Hyperparameters
- Evaluate the Model
- Dump the Model and Serialized Preprocessing class


## Model Evaluation Results

```
Evaluating Model
###########################################################
Accuracy Score for Validation Set = 0.7994471744471745
Precision Score for Validation Set = 0.5587510271158587
Recall Score for Validation Set = 0.8542713567839196
F1 Score for Validation Set = 0.6756085444610034
###########################################################
###########################################################
Accuracy Score for Test Set = 0.8044212465459011
Precision Score for Test Set = 0.5647058823529412
Recall Score for Test Set = 0.8495575221238938
F1 Score for Test Set = 0.6784452296819788
###########################################################

```