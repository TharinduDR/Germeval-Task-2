import configparser

import numpy as np
import pandas as pd
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing.text import Tokenizer
from numpy.random import seed
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score, recall_score, precision_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow import set_random_seed

from algo.nn.__keras.models import capsule
from algo.nn.__keras.utility import f1_smart
from embeddings import get_emb_matrix
from preprocessing import clean_text, remove_names, entity_recognizing

if __name__ == "__main__":
    seed(726)
    set_random_seed(726)

    print('Reading files')

    # Reading File Section - This should change

    train_2019 = pd.read_csv("data/german/germeval2019.training_subtask3.txt", sep='\t',
                             names=['tweet', 'sub_task_1', 'sub_task_2', 'sub_task_3'])

    train, test = train_test_split(train_2019, test_size=0.2)



    print('Completed reading')

    #############
    print("Train shape : ", train.shape)
    print("Test shape : ", test.shape)

    # Variables

    TEXT_COLUMN = "tweet"
    LABEL_COLUMN = "sub_task_3"

    configParser = configparser.RawConfigParser()
    configFilePath = "config.txt"
    configParser.read(configFilePath)

    EMBEDDING_FILE = configParser.get('sub_task_3_model-config', 'EMBEDDING_FILE')
    MODEL_PATH = configParser.get('sub_task_3_model-config', 'MODEL_PATH')
    PREDICTION_FILE = configParser.get('sub_task_3_model-config', 'PREDICTION_FILE')

    print(train.head())

    # print("Removing usernames")
    # train[TEXT_COLUMN] = train[TEXT_COLUMN].apply(lambda x: remove_names(x))
    # test[TEXT_COLUMN] = test[TEXT_COLUMN].apply(lambda x: remove_names(x))
    # print(train.head())
    #
    # print("Identifying names")
    #
    # train[TEXT_COLUMN] = train[TEXT_COLUMN].apply(lambda x: entity_recognizing(x))
    # test[TEXT_COLUMN] = test[TEXT_COLUMN].apply(lambda x: entity_recognizing(x))
    # print(train.head())

    print("Converting to lower-case")
    train[TEXT_COLUMN] = train[TEXT_COLUMN].str.lower()
    test[TEXT_COLUMN] = test[TEXT_COLUMN].str.lower()
    print(train.head())

    print("Cleaning punctuation marks")
    train[TEXT_COLUMN] = train[TEXT_COLUMN].apply(lambda x: clean_text(x))
    test[TEXT_COLUMN] = test[TEXT_COLUMN].apply(lambda x: clean_text(x))
    print(train.head())

    train['doc_len'] = train[TEXT_COLUMN].apply(lambda words: len(words.split(" ")))
    max_seq_len = np.round(train['doc_len'].mean() + train['doc_len'].std()).astype(int)

    embed_size = 300  # how big is each word vector
    max_features = None  # how many unique words to use (i.e num rows in embedding vector)
    maxlen = max_seq_len  # max number of words in a question to use #99.99%

    # fill up the missing values
    X = train[TEXT_COLUMN].fillna("_na_").values
    X_test = test[TEXT_COLUMN].fillna("_na_").values

    # Tokenize the sentences
    tokenizer = Tokenizer(num_words=max_features, filters='')
    tokenizer.fit_on_texts(list(X))

    X = tokenizer.texts_to_sequences(X)
    X_test = tokenizer.texts_to_sequences(X_test)

    # Pad the sentences
    X = pad_sequences(X, maxlen=maxlen)
    X_test = pad_sequences(X_test, maxlen=maxlen)

    # Get the target values
    Y = train[LABEL_COLUMN].values

    le = LabelEncoder()

    le.fit(Y)
    encoded_Y = le.transform(Y)

    word_index = tokenizer.word_index
    max_features = len(word_index) + 1

    print('Loading Embeddings')

    embedding_matrix = get_emb_matrix(word_index, max_features, EMBEDDING_FILE)

    print('Finished loading Embeddings')

    print('Start Training')

    kfold = StratifiedKFold(n_splits=5, random_state=10, shuffle=True)
    bestscore = []
    y_test = np.zeros((X_test.shape[0],))
    for i, (train_index, valid_index) in enumerate(kfold.split(X, encoded_Y)):
        X_train, X_val, Y_train, Y_val = X[train_index], X[valid_index], encoded_Y[train_index], encoded_Y[valid_index]
        filepath = MODEL_PATH
        checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=2, save_best_only=True, mode='min')
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.6, patience=1, min_lr=0.0001, verbose=2)
        earlystopping = EarlyStopping(monitor='val_loss', min_delta=0.0001, patience=2, verbose=2, mode='auto')
        callbacks = [checkpoint, reduce_lr]
        model = capsule(maxlen, max_features, embed_size, embedding_matrix, 1)
        if i == 0: print(model.summary())
        model.fit(X_train, Y_train, batch_size=64, epochs=20, validation_data=(X_val, Y_val), verbose=2,
                  callbacks=callbacks,
                  )
        model.load_weights(filepath)
        y_pred = model.predict([X_val], batch_size=64, verbose=2)
        y_test += np.squeeze(model.predict([X_test], batch_size=64, verbose=2)) / 5
        f1, threshold = f1_smart(np.squeeze(Y_val), np.squeeze(y_pred))
        print('Optimal F1: {:.4f} at threshold: {:.4f}'.format(f1, threshold))
        bestscore.append(threshold)

    print('Finished Training')

    y_test = y_test.reshape((-1, 1))
    pred_test_y = (y_test > np.mean(bestscore)).astype(int)
    test['predictions'] = le.inverse_transform(pred_test_y)

    # save predictions
    file_path = PREDICTION_FILE
    test.to_csv(file_path, sep='\t', encoding='utf-8')

    print('Saved Predictions')

    # post analysis
    tn, fp, fn, tp = confusion_matrix(test[LABEL_COLUMN], test['predictions']).ravel()
    weighted_f1 = f1_score(test[LABEL_COLUMN], test['predictions'], average='weighted')
    accuracy = accuracy_score(test[LABEL_COLUMN], test['predictions'])
    weighted_recall = recall_score(test[LABEL_COLUMN], test['predictions'], average='weighted')
    weighted_precision = precision_score(test[LABEL_COLUMN], test['predictions'], average='weighted')

    print("Confusion Matrix (tn, fp, fn, tp) {} {} {} {}".format(tn, fp, fn, tp))
    print("Accuracy ", accuracy)
    print("Weighted F1 ", weighted_f1)
    print("Weighted Recall ", weighted_recall)
    print("Weighted Precision ", weighted_precision)
