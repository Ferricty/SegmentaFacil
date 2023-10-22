from flask import json, render_template, flash, redirect, url_for, request,jsonify
from app import app
from app.forms import CustomerForm
import joblib
import numpy as np
import os
from flask_cors import cross_origin

CLUSTER_LABEL = {
                    "0": {"label": "Bajo valor",
                          "suggestions": "Son clientes que compran esporádicamente y cuando lo hacen son ofertas de bajo valor. Se recomienda no dedicarle esfuerzo a este grupo, pues forman parte del churn rate natural de cada empresa."
                        },

                    "1": {"label": "En riesgo",
                          "suggestions": "Son clientes que compraban seguido gastando grandes cantidades, pero no han realizado compras recientemente. Se recomienda enviarles una campaña personalizada para reconectar y ofrecerles productos que puedan contribuir a que realicen otra compra."
                        },

                    "2": {"label": "Leales",
                         "suggestions": "No han comprado tan recientemente como los campeones, pero cuando lo hacen aportan grandes ingresos a las ventas de la empresa. Se recomienda escuchar su opinión sobre la empresa, productos y servicios que la misma brinda y presentarle ofertas tentadoras para convertirlos en los próximos campeones."
                        },

                    "3": {"label":"A punto de perderlos",
                          "suggestions":"Son clientes que compraban y visitaban la empresa seguido, pero no han realizado compras recientemente. Se recomienda traerlos de vuelta con promociones y pedirles que llenen encuestas para conocer la razón del por qué ya no nos visitan y evitar perderlos ante la competencia."},

                    "4": {"label": "Nuevas Pasiones",
                          "suggestions":"Son el grupo de nuevos clientes que poseen el más alto valor monetario de los que recién comienzan. Si son tratados bien pueden convertirse en los próximos **campeones** o **clientes leales**. La clave con ellos es conocerlos mejor e incentivarlos a comprar." },

                    "5":  {"label": "Nuevos clientes",
                           "suggestions": "Son los clientes que tienen una buena puntuación **RFM** pero no son compradores frecuentes. Se recomienda comenzar a construir relaciones con ellos brindándoles apoyo y ofertas especiales para incrementar sus visitas." },

                    "6":  {"label": "Campeones",
                           "suggestions": "Los clientes de este grupo son los mejores clientes, los que más recientemente compraron, más seguido y son los de mayor valor monetario. Se recomienda darle recompensas a este grupo, ofrecerle planes donde sean los primeros en adquirir los productos más novedosos de la empresa y se vuelvan promotores de la marca." }
                    }

my_dir = os.path.dirname(__file__)
my_file_path_model = os.path.join(os.path.dirname(my_dir), 'model/model_1.pkl')
my_file_path_scaler = os.path.join(os.path.dirname(my_dir), 'model/scaler2.pkl')

# Leer modelo de clustering previamente entrenado
KMEANS_MODEL = joblib.load(my_file_path_model)

# Preprocesamiento de datos
SCALER = joblib.load(my_file_path_scaler)

customer_data = []
show_table = False

@app.route('/',methods=['GET','POST'])
def index():
    global show_table
    form = CustomerForm()
    if form.validate_on_submit():
        show_table = True
        recency = form.recency.data
        frequency = form.frequency.data
        monetary_value = form.monetary_value.data

        print("r: {} f: {} m: {}".format(recency,frequency,monetary_value))

        data = [[recency,frequency,monetary_value]]
        scaled_data = SCALER.transform(data)

        # Realizar prediccion
        cluster_id = KMEANS_MODEL.predict(scaled_data)

        #flash("Los datos han sido procesados exitosamente","success")
        
        response = {
                    "input_values":{'recency': recency,
                                   "frequency": frequency,
                                   "monetary_value": monetary_value},
                    "cluster_id":cluster_id[0],
                    "cluster_label": CLUSTER_LABEL[str(cluster_id[0])]["label"],
                    "suggestions": CLUSTER_LABEL[str(cluster_id[0])]["suggestions"],
                    "error": "",
                    "message":"Data processed successfully"
                    }
        customer_data.append(response)
        return redirect(url_for('result'))
    if not show_table or form.is_submitted():
        show_table = False

    return render_template('index.html',form=form,customer_data=customer_data,show_table=show_table)

@app.route('/result')
def result():

    return render_template('result.html',customer_data=customer_data,show_table=show_table)


@app.route('/api/cluster',methods=['POST'])
@cross_origin()
def api_cluster():
    try:
        recency = int(request.args.get("recency"))
        frequency = int(request.args.get("frequency"))
        monetary_value = float(request.args.get("monetary_value"))

        if recency > 365:
            response = {"error": "Invalid input",
                        "message":"The recency value should be less than 365 days. This customer has churned."}

            return jsonify(response), 400

        if recency <= 0 or frequency <= 0 or monetary_value <= 0:
            response = {"error": "Invalid input",
                        "message":"The values of recency, frequency and monetary value must be grater than zero."}

            return jsonify(response), 400

        data = np.array([[recency,frequency,monetary_value]])
        scaled_data = SCALER.transform(data)
        cluster = KMEANS_MODEL.predict(scaled_data)

        cluster_id = cluster.tolist()[0]
        cluster_label = CLUSTER_LABEL[str(cluster_id)]["label"]
        suggestions = CLUSTER_LABEL[str(cluster_id)]["suggestions"]
        response = {
                    "inputValues":{'recency': recency,
                                   "frequency": frequency,
                                   "monetaryValue": monetary_value},
                    "clusterId":cluster_id,
                    "clusterLabel":cluster_label,
                    "suggestions":suggestions,
                    "error": "",
                    "message":"Data processed successfully"
                    }

        return jsonify(response), 200

    except:
        response = {"error":"Invalid input",
                    "message": "Please provide numeric values for recency, frequency and monetary value."}
        return jsonify(response), 400
