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

/**
 * Devuelve los datos de los eventos según un criterio alterado por el favor de los dos grupos sociales.
 * @param {Number} fCorpo [-255,255] que indica "lo bien que le caes a las corporaciones"
 * @param {Number} fGente [-255,255] que indica "lo bien que le caes a los ciudadanos"
 */
async function EventoAleatorioSegunFavor(fCorpo, fGente)
{
    //Van a haber como mucho 2 eventos aleatorios a la vez, uno de cada grupo
    var maxProb = 128;
    var prob1 = getRandomInt(maxProb);
    var prob2 = getRandomInt(maxProb);

    let consulta = "";
    let consulta2 = "";

    if(fCorpo > 0   && fCorpo > prob1)
        consulta = "SELECT id from events where tipo = 2";
    else if(fCorpo < 0  && -fCorpo > prob1)
        consulta = "SELECT id from events where tipo = -2";

    if(fGente > 0   && fGente > prob2)
        consulta2 = "SELECT id from events where tipo = 1";
    else if(fGente < 0  && -fGente > prob2)
        consulta2 = "SELECT id from events where tipo = -1";

    let ev1,ev2;
    try {
        if(consulta != "") {
            corpoIDs = [];
            let [rows,fields] = await db.query(consulta);
            rows.forEach(elem => { corpoIDs.push(elem["id"]) });
            if(corpoIDs.length > 0) {
                id1 = getRandomFromArray(corpoIDs);
                ev1 = getEvent(id1)["res"];
            }
        }
        
        if(consulta2 != "") {
            genteIDs = [];
            let [rows,fields] = await db.query(consulta2);
            rows.forEach(elem => { genteIDs.push(elem["id"]) });
            if(genteIDs.length > 0) {
                id2 = getRandomFromArray(genteIDs);
                ev2 = getEvent(id2)["res"];
            }
        }
        return {info:"correcto", res:[ev1,ev2]};
    }
    catch(err) {
        logError("Error de consulta a la hora de obtener los eventos posibles en EventoAleatorioSegunFavor: "+err,'event');
        return {info:"Error..."};
    }
}

function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

function getRandomFromArray(array)
{
    return array[getRandomInt(array.length)];
}

module.exports.getEvent = getEvent;
module.exports.getRandomEvent = getRandomEvent;