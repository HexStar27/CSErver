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
    for (var idx in json) 
    {
        let result = await AddStatement(json[idx]);
        if (result == -1) return {info:"Error..."};
    }
    return {info:"Correcto", res:"Registros almacenados con éxito."};
}

async function AddStatement(json)
{
    if (json == undefined) return -1;
    console.log("Buen parse: "+json);

    if (check.SearchForKeyWords(json,"lsr"))
    {
        console.log("Limpio crímenes.");
        let actor = json["actor"];
        if(actor == undefined) return -1;
        else actor = "'"+actor+"'";

        let verb = json["verb"];
        if(verb == undefined) return -1;
        else verb = "'"+verb+"'";

        let obj = json["object"];
        if(obj == undefined) return -1;
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
        actor+", "+verb+", "+obj+", "+res+", "+ctx+", "+time+", '"+json+"')";

        console.log("Valor de la consulta: "+consulta);

        try {
            await db.query(consulta);
            console.log("Terminada lectura de statement correctamente!");
            return 1;
        }
        catch(err) {
            logError("Error de consulta en al intentar almacenar el registro: "+err,'lsr');
            return -1;
        }
    }
    else return -1;
}

module.exports.AddListOfStatements = AddListOfStatements;