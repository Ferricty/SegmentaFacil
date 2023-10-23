# SegmentaFácil

Desarrollo de un proyecto de Data Science end-to-end en el que se segmentan a clientes basándose en los parámetros **RFM**.

Actualmente se encuentra disponible en [https://customersegmentation.pythonanywhere.com/](https://customersegmentation.pythonanywhere.com/)

La segmentación de clientes es el proceso mediante el cual se agrupan los clientes en base a su comportamiento, características y necesidades. Esto ayuda a las empresas de muchas maneras en el lanzamiento de un producto, destacando las propiedades del mismo, adaptándolas a cada grupo de consumidores. Además pueden apuntar a una audiencia específica a partir de su comportamiento. Todo lo anterior influye de forma directa en el valor de mercado de la empresa.

Algunas de las formas más comunes de segmentar a los usuarios son:

* Demográfica: Ejemplos -> edad, género, ingresos y educación.
* Geográfica: Ejemplos -> país, estado y ciudad.
* Comportamiento: Ejemplos -> hábitos, acciones frecuentes y uso de productos.

Para un gerente de marketing directo resulta sumamente útil utilizar un sistema de inteligencia empresarial para informar sobre sus clientes. Al definir con precisión a sus mejores clientes basándose en parámetros como la Recency, Frecuency y Monetary Value (RFM), puede maximizar el retorno de la inversión en sus acciones de marketing. Un cliente que ordena con frecuencia, lo ha hecho recientemente y ha gastado una suma significativa de dinero es más probable que lo haga en el futuro que otros clientes.

## API Endpoint
```
https://customersegmentation.pythonanywhere.com/api/cluster
```

* Método: POST
* Descripción: Devuelve un conjunto de métricas del clúster al que pertenece el cliente
* URL-Params: int: recency int: frequency float: monetary_value
* Todos los valores a introducir tienen que ser mayores que 0.

## Estructura de la URL
```
https://customersegmentation.pythonanywhere.com/api/cluster?recency={recency}&frequency={frequency}&monetary_value={monetary_value}
```

## Ejemplo
```
https://customersegmentation.pythonanywhere.com/api/cluster?recency=64&frequency=32&monetary_value=100924
```

## Ejemplo de respuesta
```javascript
{'clusterId': 1,
 'clusterLabel': 'En riesgo',
 'error': '',
 'inputValues': {'frequency': 32,
                 'monetaryValue': 100924.0,
                 'recency': 64},
 'message': 'Data processed successfully',
 'suggestions': 'Son clientes que compraban seguido gastando grandes cantidades, pero no han realizado compras recientemente. Se recomienda enviarles una campaña personalizada para reconectar y ofrecerles productos que puedan contribuir a que realicen otra compra.'}
```
