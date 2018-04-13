import numpy as np
import csv

from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


# define base model
def baseline_model(X=None, Y=None, fit=True, nb_epoch=100, batch_size=5):
    # create model
    model = Sequential()

    shape = list(X.shape)

    dims = int(shape[1]) if len(shape) == 2 else 1

    model.add(Dense(dims, input_dim=dims, kernel_initializer='normal', activation='relu'))
    model.add(Dense(int(dims / 2), kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam')

    if fit == True:

        model.fit(X, Y, nb_epoch=100, batch_size=5)
        loss = model.evaluate(X, Y)
        return [model, loss]

    else:
        return model

# baseline_model = baseline_model()
#
# baseline_model.fit(X, Y, nb_epoch=100, batch_size=5)
#
# predictions = baseline_model.predict(xx)
#
# print(predictions)
#
# print(yy)
#
# baseline_model.save_weights("my_model.h5")
#
# Loss = baseline_model.evaluate(X, Y)
#
# print(Loss)

# fix random seed for reproducibility
# seed = 7
# numpy.random.seed(seed)
# evaluate model with standardized dataset
# estimator = KerasRegressor(build_fn=baseline_model, epochs=100, batch_size=5, verbose=0)

# kfold = KFold(n_splits=10, random_state=seed)
# results = cross_val_score(estimator, X, Y, cv=kfold)
# print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))

# evaluate model with standardized dataset


# numpy.random.seed(seed)
# estimators = []
# estimators.append(('standardize', StandardScaler()))
# estimators.append(('mlp', KerasRegressor(build_fn=baseline_model, epochs=50, batch_size=5, verbose=0)))
# pipeline = Pipeline(estimators)
# kfold = KFold(n_splits=10, random_state=seed)
# results = cross_val_score(pipeline, X, Y, cv=kfold)
# print("Standardized: %.2f (%.2f) MSE" % (results.mean(), results.std()))


### model.save_weights("my_model.h5")

### model.load_weights('my_model_weights.h5')
