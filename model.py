import featureEngineering as fe
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import pandas as pd
from sklearn.model_selection import cross_val_score, KFold
from itertools import combinations
import pprint
from joblib import dump, load

np.set_printoptions(legacy='1.25') 

df = fe.getTable().copy()

df.drop(columns='dev_budget_usd', inplace=True)

# data dropping time :D
# my idea is to comment them in and out as needed
# df.drop(columns='team_size', inplace=True)
# df.drop(columns='platforms_count', inplace=True)
# df.drop(columns='publisher_size', inplace=True)
# df.drop(columns='is_multiplayer', inplace=True)
# df.drop(columns='dev_time_months', inplace=True)
# df.drop(columns='launch_price_usd', inplace=True)
# df.drop(columns='launch_discount', inplace=True)

def splitData(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
    X, y , random_state=104,test_size=0.2, shuffle=True)

    # print(X_train.shape, X_test.shape) 
    # print(y_train.shape, y_test.shape)
    # print()

    return X_train, X_test, y_train, y_test


def trainModel(X_train, y_train):
    model = make_pipeline(StandardScaler(), LinearRegression())
    model.fit(X_train, y_train)
    return model


def regularTest(model, X_test, y_test):
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    reg = model['linearregression']
    print(f"Intercept (b): {reg.intercept_}")
    print(f"Slope/Coefficients (m): {pd.Series(reg.coef_, index=X.columns)}")
    print(f"Mean Squared Error: {mse:.4f}")
    print(f"R-squared Score: {r2:.4f}")


def kFoldTest(model, fieldToDrop=None):
    tempX = X.copy()
    if(fieldToDrop != None):
        tempX.drop(columns=fieldToDrop, inplace=True)
        #print("Model without ", fieldToDrop)
    else:
        pass
        #print("Base Model")

    cv = KFold(n_splits=5, shuffle=True, random_state=0)

    scores = cross_val_score(model, tempX, y, cv=cv, scoring='r2')
    rmse = -cross_val_score(model, tempX, y, cv=cv, scoring='neg_root_mean_squared_error')

    # std here measures how much the values actually vary
    # low std means the model performs consistent across different splits

    # debugging
    # print('r2 values = ', scores)
    # print('r2 mean:', scores.mean())
    # print('r2 std: ', scores.std())
    # print('RMSE = ', rmse) 
    # print('RMSE mean:', rmse.mean())
    # print('RMSE std: ', rmse.std())                      
    # print() 

    return scores, rmse


# the plan to test the models
# first above is our 'base' model
# now below we shd make models without a field that we want to test
# we then compare the r2 values in the array and the rmse values
# we use the formula:
# rmse with field - rmse without field
# r2 with field - r2 without field
# take the average of the array
# first we check this:
# |mean difference| < 0.005
# this means it maKes a difference of 0.5%, which means its bassically insignificant
# if it is we lean towards removing it because the model is simpler then
# for rmse if the value is positive we drop it (because rmse with field is greater and lower rmse is better)
# for r2 if value is positive we keep it (because higher r2 is better)

def CompareModels(baseModel, newModel):
    # first we store the scores and rmse in an array
    baseScores = baseModel[0]    
    baseRmse = baseModel[1]

    newModelScores = newModel[0]
    newModelRmse = newModel[1]

    # rmse values
    #print("RMSE:")
    rmse = baseRmse - newModelRmse
    rmseMean = np.mean(rmse, dtype=float)
    #print(rmse)
    #print(rmseMean)

    # r2 values
    #print("R2: ")
    r2 = baseScores - newModelScores
    r2Mean = np.mean(r2, dtype=float)
    #print(r2)
    #print(r2Mean)

    return rmseMean, r2Mean


X = df.drop(columns='first_year_sales_k')
y = np.log1p(df['first_year_sales_k']) # log transformed sales

fieldsToDrop = ['is_multiplayer', 'team_size', 'platforms_count', 'publisher_size', 'dev_time_months', 'launch_price_usd', 'launch_discount']

# new idea: rather than manually removing and adding we use best subset selection
# its a cool idea where i get all combinations of the array fieldsToDrop, pass that in and get all the rmse and r2 values
model = make_pipeline(StandardScaler(), LinearRegression()) # untrained model

fieldsToDropCombinations = []
for i in range(len(fieldsToDrop) + 1):
    fieldsToDropCombinations.extend(combinations(fieldsToDrop, i)) 

baseR2, baseRmse = kFoldTest(model) # get the base values

# base model
# CompareModels(kFoldTest(models[0]), kFoldTest(model, fieldsToDrop))

# print(len(fieldsToDropCombinations))
#print(fieldsToDropCombinations)

# baseModel = kFoldTest(model)
# modelValuesRmse = {}
# modelValuesR2 = {}
# count = 0

# for i in fieldsToDropCombinations:
#     values = CompareModels(baseModel, kFoldTest(model, list(i)))
#     modelValuesRmse[i] = values[0]
#     modelValuesR2[i] = values[1]
#     count += 1

# here we train all combination models using the kfoldtest
rows = []
for combo in fieldsToDropCombinations:
    r2, rmse = kFoldTest(model, list(combo))
    rows.append({
        'dropped': ', '.join(combo) if combo else '(none - base model)',
        'n_dropped': len(combo),
        'rmse_mean': rmse.mean(),
        'r2_mean': r2.mean(),
        'rmse_vs_base': (baseRmse - rmse).mean(),
        'no_of_better_folds': int((rmse < baseRmse).sum())
    })

results = pd.DataFrame(rows).sort_values('rmse_mean').reset_index(drop=True)

# after we get the results we display them for debugging
# we gotta display the rmse with the lowest rmse
pd.set_option('display.width', 200)
pd.set_option('display.max_colwidth', 90)
print("Top 10 subsets (lowest RMSE first)")
print(results.head(10).round(4).to_string())

# we now choose the subset with the lowest rmse
best = results.iloc[0]
chosenDrop = best['dropped'].split(',')
chosenDrop = [item.strip() for item in chosenDrop] # strips the array of any spaces
print(chosenDrop)

Xfinal = X.drop(columns=chosenDrop)
finalDrop = fe.invalidColumns + chosenDrop

finalModel = make_pipeline(StandardScaler(), LinearRegression())
finalModel.fit(Xfinal, y)

dump(finalModel, "game_model_full.joblib")
dump(Xfinal.columns, "required_inputs.joblib")
dump(finalDrop, "final_drop.joblib")

print("Model and scaler saved successfully!")