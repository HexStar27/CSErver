var db = require("./mysql").baseP;
var util = require("./utility");

/**
 * Devuelve las tablas y columnas dado una serie de códigos desbloqueables (cadenas).
 * @param {array} codigos
*/
async function GetTablesAvailables(codigos)
{
    let condiciones = "";
    codigos.array.forEach(cod => {
        if(!util.SearchForKeyWords(cod,"tableService")) return;
        condiciones += "id = '" +cod.substring(1,cod.length-1)+ "' OR ";
    });
    condiciones = condiciones.substring(0,condiciones.length-3);
    let consulta = "SELECT content FROM tablesUnlockCode " + condiciones;

    try {
        let [rows,fields] = await db.query(consulta);
        return {info:"Correcto", res:rows};
    } catch (err) {
        logError("Error de consulta en GetTablesAvailable: "+err, 'tableService');
        return {info:"Error..."};
    }
}

module.exports.GetTablesAvailables = GetTablesAvailables;