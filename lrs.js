//Funciones relacionadas con los registros de e-learning.

var db = require("./mysql").baseP;
const { logError } = require("./debug");
var check = require("./utility");

/**
 * Introduce en la base de datos todos los registros recibidos
 * @param {string} json
 */
async function AddListOfStatements(rawJSON)
{
    let json = JSON.parse(rawJSON);
    json = json["lista"];
    for (var elem in json) await AddStatement(elem);
}

async function AddStatement(rawJSON)
{
    let json;
    try{
        json = JSON.parse(rawJSON);
    }
    catch(err)
    {
        logError("Error al parsear JSON: "+err, 'lsr');
        return {info:"Error..."};
    }

    if (json == undefined) return {info:"Error..."};
    if (check.SearchForKeyWords(rawJSON,"lsr"))
    {
        let actor = json["actor"];
        if(actor == undefined) return {info:"Error..."};
        else actor = "'"+actor+"'";

        let verb = json["verb"];
        if(verb == undefined) return {info:"Error..."};
        else verb = "'"+verb+"'";

        let obj = json["object"];
        if(obj == undefined) return {info:"Error..."};
        else obj = "'"+obj+"'";

        let res = json["result"];
        if(res == undefined) res = "null";
        else res = "'"+res+"'";

        let ctx = json["context"];
        if(ctx == undefined) ctx = "null";
        else ctx = "'"+ctx+"'";

        let time = json["timestamp"];
        if(time == undefined) time = "null";
        else time = "'"+time+"'";

        let consulta = "INSERT INTO learningRecord (actor, verb, object, result, context, timestamp, whole_statement) VALUES ("+
        actor+", "+verb+", "+obj+", "+res+", "+ctx+", "+time+", '"+rawJSON+"')";

        try {
            await db.query(consulta);
            return {info:"Correcto", res:"Registro almacenado con éxito."};
        }
        catch(err) {
            logError("Error de consulta en al intentar almacenar el registro: "+err,'lsr');
                    return {info:"Error..."};
        }
    }
    else return {info:"Error..."};
}

module.exports.AddListOfStatements = AddListOfStatements;