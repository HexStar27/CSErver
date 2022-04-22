//Funciones relacionadas con los posibles eventos que pueden ocurrir en el juego.

var db = require("./mysql").baseP;
const { logError } = require("./debug");
var check = require("./utility");

/**
 * Devuelve un evento aleatorio
 */
async function getRandomEvent()
{
    //Obtener número de eventos almacenados
    let consulta = "SELECT Count(id) FROM events GROUP BY id";

    let nElem;
    try {
        let [rows,fields] = await db.query(consulta);
        nElem = rows[0]["Count(id)"];
    } 
    catch(err) {
        logError("Error de consulta a la hora de obtener el número de eventos en getRandomEvent: "+err,'event');
        return {info:"Error..."};
    }

    if (nElem > 0){
        //Escoger un número aleatorio entre el 1 y el maximo
        let r = check.randBetween(1,nElem);
        //Mandar consulta pidiendo evento concreto
        return getEvent(r);
    }
    else return {info:"Error...", res:"ups... No hay eventos?"};
}

/**
 * Devuelve el evento especificado
 * @param {Number} id 
 */
async function getEvent(id)
{
    if(check.AntiInjectionNumberField(id,"event"))
    {
        let consulta = "SELECT data from events where id = "+id;

        try {
            let [rows,fields] = await db.query(consulta);
            if(rows.length == 0){
                logError("Error, se ha intentado acceder a un evento inexistente.",'event');
                return {info:"Incorrecto", res:"Ese evento no existe"};
            }
            return {info:"Correcto", res:rows[0]["data"]};
        } 
        catch(algo)
        {
            logError("Error de consulta en getEvent: "+algo, 'event');
            return {info:"Error..."};
        }
    }
    else return {info:"Incorrecto", res:"K COÑO ESTÁS INTENTANTO JOPUTA"};
}

module.exports.getEvent = getEvent;
module.exports.getRandomEvent = getRandomEvent;