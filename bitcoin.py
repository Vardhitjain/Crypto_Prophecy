import pickle


def b_predict(pred):
    b_pred = pickle.load(open('ans.pkl', 'rb'))
    return b_pred[pred][0]


