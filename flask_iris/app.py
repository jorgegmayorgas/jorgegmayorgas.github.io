import joblib
import numpy as np
import os
import pandas as pd
import pickle
import random
import subprocess
import urllib.request
from flask import Flask, jsonify, request,render_template, send_from_directory
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from sklearn.preprocessing import StandardScaler,MinMaxScaler,OneHotEncoder,MultiLabelBinarizer,OneHotEncoder,OrdinalEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report, confusion_matrix,ConfusionMatrixDisplay,r2_score, mean_absolute_error, mean_squared_error,mean_absolute_percentage_error,r2_score
from sklearn.model_selection import train_test_split,GridSearchCV,RandomizedSearchCV
from sklearn.decomposition import PCA

app = Flask(__name__)
app.config['DEBUG'] = True # Parameter for Flask to enable DEBUG mode
label_dict={'setosa':0,'versicolor':1,'virginica':2} # Dictionary of labels
label_dict_reverse={0:'setosa',1:'versicolor',2:'virginica'} # Dictionary of reverse labels
target="species" # target column
features_cat= ['sepal_length_(cm)','sepal_width_(cm)','petal_length_(cm)','petal_width_(cm)'] #features for the ml model
root_path = "/var/www/irismlapi/flask_iris/src/" # ony used when app is executed uder Apache2/Nginx

def validate_params(params_dict):
    # Define each parameter with two error codes: 
    # the first if it is missing, the second if it is non-numeric.
    required_params = {
        "lsepal": ("001", "005"),
        "wsepal": ("002", "006"),
        "lpetal": ("003", "007"),
        "wpetal": ("004", "008"),
    }
    
    # Loop through the required parameters
    for param, (missing_code, non_numeric_code) in required_params.items():
        value = params_dict.get(param, "")  # or `params_dict.get(param, None)`
        
        # 1) Check if parameter is missing or empty
        if not value:
            return jsonify({
                "error": missing_code,
                "message": f"{param} parameter is mandatory"
            })
        
        # 2) Check if parameter is numeric
        if not value.isdigit():
            return jsonify({
                "error": non_numeric_code,
                "message": f"{param} parameter is not a numeric value"
            })
    
    # If everything passes, return None (or you can return True)
    return None


# Routes to landing page (endpoint /)
@app.route('/', methods=['GET'])
def hello(): # Bind to endopoint "/" or home, with GET method

    return render_template('index.html')

# Routes function to endpoint /api/v1/predictrf
@app.route('/api/v1/predictrf', methods=['GET'])
def predictrf(): # Bind to endopoint '/api/v1/predictrf', with GET method

    model = joblib.load(open(root_path + 'random_forest_joblib.pkl','rb'))
    lsepal = request.args.get('lsepal')
    wsepal = request.args.get('wsepal')
    lpetal = request.args.get('lpetal')
    wpetal = request.args.get('wpetal')
    print(lsepal,wsepal,lpetal,wpetal)
    bln_error=False
    params = {
        "lsepal": request.form.get('lsepal'),
        "wsepal": request.form.get('wsepal'),
        "lpetal": request.form.get('lpetal'),
        "wpetal": request.form.get('wpetal'),
    }
    
    error_response = validate_params(params)
    if error_response is not None:
        return error_response

    dict_get_values={'sepal_length_(cm)':[lsepal],
    'sepal_width_(cm)':[wsepal],
    'petal_length_(cm)':[lpetal],
    'petal_width_(cm)':[wpetal]}
    df_get_values=pd.DataFrame(dict_get_values)
    prediction = model.predict(df_get_values)
    #type_of_variable = type(prediction[0])
    result_json={
        'prediction_numeric': int(prediction[0]),
        'prediction_label': label_dict_reverse[int(prediction[0])]
    }
    #return jsonify({'predictions_label': label_dict_reverse[prediction[0]],'predictions': prediction[0]})
    return jsonify(result_json)
@app.route('/api/v1/predictk', methods=['GET'])
def predictk(): # Bind to endopoint '/api/v1/predictk', with GET method
    model = joblib.load(open(root_path + 'knn_joblib.pkl','rb'))
    lsepal = request.args.get('lsepal')
    wsepal = request.args.get('wsepal')
    lpetal = request.args.get('lpetal')
    wpetal = request.args.get('wpetal')
    #print(lsepal,wsepal,lpetal,wpetal)
    bln_error=False
    params = {
        "lsepal": request.form.get('lsepal'),
        "wsepal": request.form.get('wsepal'),
        "lpetal": request.form.get('lpetal'),
        "wpetal": request.form.get('wpetal'),
    }
    
    error_response = validate_params(params)
    if error_response is not None:
        return error_response
    dict_get_values={'sepal_length_(cm)':[lsepal],
    'sepal_width_(cm)':[wsepal],
    'petal_length_(cm)':[lpetal],
    'petal_width_(cm)':[wpetal]}
    df_get_values=pd.DataFrame(dict_get_values)
    prediction = model.predict(df_get_values)
    result_json={
        'prediction_numeric': int(prediction[0]),
        'prediction_label': label_dict_reverse[int(prediction[0])]
    }
    return jsonify(result_json)
# Routes the function to endpoint /api/v1/labelflowerclasses
@app.route('/api/v1/labelflowerclasses', methods=['GET'])
def labelflowerclasses(): #Bind to endopoint '/api/v1/labelflowerclasses', with GET method

    return jsonify(label_dict)
# Enruta la funcion al endpoint /api/v1/labelflowerclasses
@app.route('/api/v1/numericflowerclasses', methods=['GET'])
def numericflowerclasses(): # Ligado al endpoint '/api/v1/predict', con el método GET

    return jsonify(label_dict_reverse)
# Enruta la funcion al endpoint /api/v1/retrainforest
@app.route('/api/v1/retrainforest/', methods=['GET'])
def retrainforest(): # Rutarlo al endpoint '/api/v1/retrain/', metodo GET

    if os.path.exists(root_path + "data/retrain_random_forest.csv"):
        data = pd.read_csv(root_path + 'data/retrain_random_forest.csv')
        X = data[features_cat]
        y = data[target]
        X_train, X_test, y_train, y_test = train_test_split(X,
                                                            y,
                                                            test_size = 0.20,
                                                            random_state=42)
        model = RandomForestClassifier(n_estimators=150,random_state=42)  # 150 trees in the forest
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        filename = f'{root_path}random_forest_joblib.pkl'

        with open(filename, 'wb') as file:
            joblib.dump(model, file)

        message = "Model Random Forest retrained"
        message = message + "<pre>" + str(classification_report(y_test,y_pred)) + "</pre>"
        return message

@app.route('/api/v1/retrainknn/', methods=['GET'])
def retrainknn(): # Rutarlo al endpoint '/api/v1/retrainknn/', metodo GET
    if os.path.exists(root_path + "data/retrain_knn.csv"):
        data = pd.read_csv(root_path + 'data/retrain_knn.csv')
        X = data[features_cat]
        y = data[target]
        X_train, X_test, y_train, y_test = train_test_split(X,
                                                            y,
                                                            test_size = 0.20,
                                                            random_state=42)
        model = KNeighborsClassifier(n_neighbors=12)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        filename = f'{root_path}knn_joblib.pkl'

        with open(filename, 'wb') as file:
            joblib.dump(model, file)

        message = "Model KNN retrained"
        message = message + "<pre>" + str(classification_report(y_test,y_pred)) + "</pre>"
        return message

@app.route('/webhook', methods=['POST'])
def webhook():
    # Ruta al repositorio donde se realizará el pull
    path_repo = '/var/www/irismlapi/flask_iris'
    #servidor_web = '/var/www/jorgegmayorgas_pythonanywhere_com_wsgi.py'
    servidor_web= '/var/www/irismlapi/flask_iris/src/irismlapi.wsgi'
    # Comprueba si la solicitud POST contiene datos JSON
    if request.is_json:
        payload = request.json
        # Verifica si la carga útil (payload) contiene información sobre el repositorio
        if 'repository' in payload:
            # Extrae el nombre del repositorio y la URL de clonación
            repo_name = payload['repository']['name']
            clone_url = payload['repository']['clone_url']

            # Cambia al directorio del repositorio
            try:
                os.chdir(path_repo)
            except FileNotFoundError:
                return jsonify({'message': 'El directorio del repositorio no existe'}), 404

            # Realiza un git pull en el repositorio
            try:
                subprocess.run(['git', 'pull', clone_url], check=True)
                subprocess.run(['touch', servidor_web], check=True) # Trick to automatically reload PythonAnywhere WebServer
                return jsonify({'message': f'Se realizó un git pull en el repositorio {repo_name}'}), 200
            except subprocess.CalledProcessError:
                return jsonify({'message': f'Error al realizar git pull en el repositorio {repo_name}'}), 500
        else:
            return jsonify({'message': 'No se encontró información sobre el repositorio en la carga útil (payload)'}), 400
    else:
        return jsonify({'message': 'La solicitud no contiene datos JSON'}), 400
if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)
