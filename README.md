# Explicación de Verbos HTTP y Semántica

La diferencia principal entre los métodos **GET, POST, PATCH y DELETE** radica en su **semántica**. 

Aunque técnicamente a nivel de código es posible realizar acciones correspondientes a otro método (por ejemplo, devolver un elemento al hacer POST o enviar un *body* enorme en un DELETE), estos verbos sirven para identificar la intención de la acción de forma estandarizada. Contextualmente tienen funciones distintas. Al respetar esta semántica, garantizamos que las cosas se hagan de forma correcta y predecible, sin importar cómo ni en dónde esté implementado el servidor.

Específicamente, el estándar define que:
*   **GET**: Sirve exclusivamente para **leer** o consultar recursos. Nunca debe modificar el estado de los datos.
*   **POST**: Sirve para **crear** un nuevo recurso en el servidor, enviando los datos a través del cuerpo (*body*) de la petición.
*   **PATCH**: Sirve para **modificar parcialmente** un recurso que ya existe (actualizando solo los campos que se envían).
*   **DELETE**: Sirve para **eliminar** un recurso existente.

### ¿Por qué POST no es idempotente?

Un método HTTP se considera **idempotente** si ejecutarlo una vez tiene el mismo efecto en el estado del servidor que ejecutarlo múltiples veces (por ejemplo, si haces DELETE diez veces sobre la tarea 1, la tarea simplemente "sigue estando borrada").

**POST no es idempotente** porque su función es crear un recurso nuevo. Si un cliente envía exactamente la misma petición POST cinco veces seguidas, el servidor no conservará el estado original, sino que creará cinco recursos distintos (con cinco IDs diferentes). Cada llamada altera el estado del servidor de forma aditiva.