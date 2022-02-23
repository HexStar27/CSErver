//Funciones para mostrar en consola las cosillas, 
//en un futuro se puede hacer que se guarde en un fichero.

/**
 * Fecha actual
 * @returns fecha en formato yyyy-mm-dd
 */
function logDate()
{
    let ts = Date.now();
    let date_ob = new Date(ts);
    let date = date_ob.getDate();
    let month = date_ob.getMonth() + 1;
    let year = date_ob.getFullYear();

    return year + "-" + month + "-" + date;
}

/**
 * Fecha y hora actual
 * @returns tiempo en formato yyyy-mm-dd, hh:mm:ss.
 */
function logFullDate()
{
    let ts = Date.now();
    let date_ob = new Date(ts);
    let date = date_ob.getDate();
    let month = date_ob.getMonth() + 1;
    let year = date_ob.getFullYear();
    let hour = date_ob.getHours();
    let min = date_ob.getMinutes();
    let sec = date_ob.getSeconds();

    return year+"-"+month+"-"+date+", "+hour+":"+min+":"+sec+".";
}

/**
 * Escribe en el log un aviso de intento de instrusión por inyección SQL
 * @param {String} fileName nombre del módulo en el que ha ocurrido
 * @param {*} data dato afectado
 */
function logSQLInjectionWarning(fileName,data)
{
    console.log("\n! Desde "+fileName+".js: "+logFullDate());
    console.log("    Cuidao, puede que alguien esté intentando hacer una inyección SQL.");
    console.log("    Recivido: "+data);
}

function logError(err, fileName)
{
    console.log("\n! Desde "+fileName+".js: "+logFullDate());
    console.log("   Info: "+err);
}

module.exports.logDate = logDate;
module.exports.logFullDate = logFullDate;
module.exports.logSQLInjectionWarning = logSQLInjectionWarning;
module.exports.logError = logError;