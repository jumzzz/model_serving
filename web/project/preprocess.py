from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder

import pandas as pd


class CategoricalTransformer(BaseEstimator, TransformerMixin):
    """Scikit-Learn compatible transformer class for transfroming categorical data of Adult Census Datset

    Args:
        BaseEstimator ([type]): Scikit-Learn BaseEstimator class
        TransformerMixin ([type]): Scikit-Learn TransfromerMixin class
    """

    def __init__(self):
                
        self.transformers = [
            ('education', LabelEncoder()),
            ('workclass', LabelEncoder()),
            ('marital.status', LabelEncoder()),
            ('occupation', LabelEncoder()),
            ('relationship', LabelEncoder()),
            ('race', LabelEncoder()),
            ('sex', LabelEncoder()),
            ('native.country', LabelEncoder()),
            ('income', LabelEncoder())
        ]
    
    def fit(self, df : pd.DataFrame):
        """Fits the data to the list (self.transformers) of LabelEncoders 

        Args:
            df (pd.DataFrame): Dataframe of Adult Census Dataset
        """
        for col_transform in self.transformers:
            col_transform[1].fit(df[col_transform[0]])

 
    def transform(self, df : pd.DataFrame) -> pd.DataFrame:
        """Performs multiple Label Encoding to multiple fields 

        Args:
            df (pd.DataFrame): Dataframe of Adult Census Dataset
        Returns:
            pd.DataFrame: Transformed Dataframe
        """

        df_transform = pd.DataFrame()
        
        for col_transform in self.transformers:
            df_transform[col_transform[0]] = col_transform[1].transform(
                                                  df[col_transform[0]])

        return df_transform

    def transform_features(self, df : pd.DataFrame) -> pd.DataFrame:
        """Performs multiple Label Encoding excluding the actual target/label (income) of Adult Census dataset

        Args:
            df (pd.DataFrame): [description]

        Returns:
            pd.DataFrame: [description]
        """

        df_transform = pd.DataFrame()

        for col_transform in self.transformers[0:-1]:
            df_transform[col_transform[0]] = col_transform[1].transform(
                                                  df[col_transform[0]])

        return df_transform


class OrdinalTransformer(BaseEstimator, TransformerMixin):
    """Performs ordinal transformation to real valued features of Adult Census dataset

    Args:
        BaseEstimator ([type]): Scikit-Learn BaseEstimator class
        TransformerMixin ([type]): Scikit-Learn TransfromerMixin class
    """
    
    def __init__(self):
        self.transformers = [
            ('age', self.get_age_range),
            ('capital.gain', self.get_capital_gain_range),
            ('capital.loss', self.get_capital_loss_range),
            ('fnlwgt', self.get_fnlwgt_range),
            ('hours.per.week', self.get_hours_per_week_range),
        ]
    
    
    def transform(self, df : pd.DataFrame) -> pd.DataFrame:
        """Transforms the real-valued features to ordinal.

        Args:
            df (pd.DataFrame): Dataframe of adult dataset

        Returns:
            pd.DataFrame: Dataframe of transformed dataset
        """

        df_transform = pd.DataFrame() 
        for col_transform in self.transformers:
            df_transform[col_transform[0]] = df[col_transform[0]].apply(col_transform[1])
            
        return df_transform
            
        
    def get_range(self, y, scale, num_range):
        """General implementation of converting number ranges in terms of range. This will be 
           reused consistently throughout OrdinalTransformer class.

        Args:
            y (int/float): Actual value of the number to be transformed (argument in df[col].apply(y))
            scale (float): Scaling factor
            num_range (int): Maximum number range (i.e. num_range=10, then range is from 1-10) 

        Returns:
            int: range/rank result
        """

        for i in range(1,num_range):
            dif = y - scale * i
            if dif < 0:
                continue

            if dif < scale:
                return i  
        return i

    def get_age_range(self, y):
        """Calibrated application of get_range for age feature

        Args:
            y (int/float): Actual value of the number to be transformed (argument in df[col].apply(y))

        Returns:
            int: range/rank result
        """

        num_range = 10
        scale = 100 / num_range
        return self.get_range(y, scale, num_range)

    def get_capital_gain_range(self, y):
        """Calibrated application of get_range for capital.gain feature

        Args:
            y ([type]): Actual value of the number to be transformed (argument in df[col].apply(y))

        Returns:
            int: range/rank result
        """
        num_range = 10
        scale = 100e3 / num_range
        return self.get_range(y, scale, num_range)

    def get_capital_loss_range(self, y):
        """Calibrated application of get_range for capital.loss feature

        Args:
            y ([type]): Actual value of the number to be transformed (argument in df[col].apply(y))

        Returns:
            int: range/rank result
        """
        num_range = 10
        scale = 5000 / num_range
        return self.get_range(y, scale, num_range)

    def get_fnlwgt_range(self, y):
        """Calibrated application of get_range for fnlwgt feature

        Args:
            y ([type]): Actual value of the number to be transformed (argument in df[col].apply(y))

        Returns:
            int: range/rank result
        """
        num_range = 10
        scale = 1484705 / num_range
        return self.get_range(y, scale, num_range)

    def get_hours_per_week_range(self, y):
        """Calibrated application of get_range for hours.per.week feature

        Args:
            y ([type]): [Actual value of the number to be transformed (argument in df[col].apply(y))

        Returns:
            int: range/rank result
        """
        num_range = 10
        scale = 100 / num_range
        return self.get_range(y, scale, num_range)
    
    def fit(self, df : pd.DataFrame):
        pass
        
        
class DataTransformer(BaseEstimator, TransformerMixin):
    """Combines the Transformation of CategoricalTransformer and OrdinalTransformer

    Args:
        BaseEstimator ([type]): Scikit-Learn BaseEstimator class
        TransformerMixin ([type]): Scikit-Learn TransfromerMixin class
    """

    def __init__(self):
        self.cat_transformer = CategoricalTransformer()
        self.ord_transformer = OrdinalTransformer()
     
    def fit(self, df : pd.DataFrame):
        """Fits both cat_transformer & ord_transformer

        Args:
            df (pd.DataFrame): Adult Census dataframe
        """
        self.cat_transformer.fit(df)
        self.ord_transformer.fit(df)
 
    def transform(self, df : pd.DataFrame) -> pd.DataFrame:
        """Transforms the whole dataframe

        Args:
            df (pd.DataFrame): Adult Census dataset

        Returns:
            pd.DataFrame: Transformed Dataset
        """

        df_cat = self.cat_transformer.transform(df)
        df_ord = self.ord_transformer.transform(df)
        
        return pd.concat([df_cat, df_ord], axis=1)

    def transform_features(self, df : pd.DataFrame) -> pd.DataFrame:
        """[summary]

        Args:
            df (pd.DataFrame): [description]

        Returns:
            pd.DataFrame: [description]
        """
        df_cat = self.cat_transformer.transform_features(df)
        df_ord = self.ord_transformer.transform(df)
        
        return pd.concat([df_cat, df_ord], axis=1)

    def fit_transform(self, df : pd.DataFrame) -> pd.DataFrame:
        """[summary]

        Args:
            df (pd.DataFrame): [description]

        Returns:
            pd.DataFrame: [description]
        """
        self.fit(df)
        return self.transform(df)
        