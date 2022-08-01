import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report, f1_score
from joblib import dump
from pathlib import Path

folder_path = Path(__file__).parent


def training():
    # import data
    path_data_negative_posologie = folder_path.joinpath(
        'data', 'negative_examples_posology.csv'
    )
    path_data_positive_posologie = folder_path.joinpath(
        'data', 'positive_examples_posology.csv'
    )
    data_negative_posologie = pd.read_csv(
        path_data_negative_posologie,
        header=0, index_col='Id', names=['Id', 'Text']
    )
    data_positive_posologie = pd.read_csv(
        path_data_positive_posologie,
        header=0, index_col='Id', names=['Id', 'Text']
    )

    # add target column : 0 means it is not a posology
    data_negative_posologie['Target'] = 0

    # add target column : 1 means it is a posology
    data_positive_posologie['Target'] = 1

    # concatenate both data_positive_posologie and data_negative_posologie
    # into a dataframe named data
    data = pd.concat(
        [data_positive_posologie, data_negative_posologie],
        ignore_index=True
    )

    # remove a nan row in the dataframe
    data.dropna(inplace=True)

    # prepare trains and tests datasets
    X = data['Text']
    y = data.Target
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=100)
    X_train.shape, X_test.shape, y_train.shape, y_test.shape

    # Transforming Dataset using CountVectorizer
    count_vectorizer = CountVectorizer(binary=True)
    count_vectorizer.fit(X_train)

    # vectorize data
    X_train = count_vectorizer.transform(X_train)
    X_test = count_vectorizer.transform(X_test)

    # logistic regression model
    lr = LogisticRegression()
    lr.fit(X_train,y_train)

    # test model
    y_pred = lr.predict(X_test)
    score = lr.score(X_test,y_test)
    print(f'Accuracy on test data: {score}')

    # compute f1 score
    f1score = f1_score(y_test, y_pred)
    print(f"F1 score on test data: {f1score}")
    # create model pipeline
    pipe = Pipeline([('vectorizer', count_vectorizer), ('model', lr)])

    # export model pipe
    model_path = folder_path.joinpath('models', 'posology-model.joblib')
    dump(pipe, model_path)
    # print()

if __name__ == "__main__":
    training()
