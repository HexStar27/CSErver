var db = require("./mysql").baseP;
var util = require("./utility");

/**
 * Devuelve las tablas dado una serie de códigos desbloqueables (cadenas).
 * @param {array} codigos
*/
async function GetTablesAvailables(codigos)
{
    let condiciones = "";
    try{
    codigos = JSON.parse(codigos);
    codigos = codigos.codigos;
    codigos.array.forEach(cod => {
        if(!util.SearchForKeyWords(cod,"tableService")) return {info:"Error... Un poco SUSpechoso..."};
        condiciones += "id = '" +cod.substring(1,cod.length-1)+ "' OR ";
    });
    } catch{
        return  {info:"Error..."};
    }
    condiciones = condiciones.substring(0,condiciones.length-3);
    let consulta = "SELECT content FROM tablesUnlockCode " + condiciones;

    try {
        let [rows,fields] = await db.query(consulta);
        return {info:"Correcto", res:rows};
    } catch (err) {
        logError("Error de consulta en GetTablesAvailables: "+err, 'tableService');
        return {info:"Error..."};
    }
}

/**
 * Devuelve las columnas dado una serie de códigos desbloqueables (cadenas).
 * @param {array} codigos
*/
async function GetTableColumns(table)
{
    if(!util.SearchForKeyWords(table)) return {info:"Error... Un poco SUSpechoso..."};
    let consulta = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'csedb_game' AND TABLE_NAME = '" +table+ "'";

    try {
        let [rows,fields] = await db.query(consulta);
        return {info:"Correcto", res:rows};
    } catch (err) {
        logError("Error de consulta en GetTableColumns: "+err, 'tableService');
        return {info:"Error..."};
    }
}

module.exports.GetTablesAvailables = GetTablesAvailables;
module.exports.GetTableColumns = GetTableColumns;