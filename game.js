//Funciones para el guardado y carga de partidas.

var db = require("./mysql").baseP;
const { logError } = require("./debug");
var check = require("./utility");

/**
 * Devuelve los datos guardados de la partida del jugador especificado
 * @param {Number} id 
 */
async function load(id)
{
    if(check.AntiInjectionNumberField(id,"game"))
    {
        let consulta = "SELECT file FROM savedfiles WHERE player_id = "+id;
        
        try {
            let [rows,fields] = await db.query(consulta);
            if (rows.length == 0) return {info:"Correcto", res:""};
            return {info:"Correcto", res:rows[0]["file"]};
        } 
        catch(err) {
            logError("Error de consulta en load: "+err,'game');
            return {info:"Error..."};
        }
    }
    else return {info:"Incorrecto", res:"Usuario no encontrado."};
}

/**
 * Guarda en la base de datos los datos de la partida del jugador especificado
 * @param {Number} id ID del jugador
 * @param {JSON} savefile
 */
async function Save(id,savefile)
{
    if(check.AntiInjectionNumberField(id,"game"))
    {
        //Comprobar que jugador existe
        let existe = await check.PlayerExist(id);
        if(!existe) return {info:"Incorrecto", res:"El jugador no existe..."};

        let savefileTXT = JSON.stringify(savefile);
        //Comprobar que no se esté intentando hacer una inyección SQL dentro del archivo de guardado
        if(!check.SearchForKeyWords(savefileTXT,'game')) return {info:"Incorrecto", res:"Cuidaito conmigo, eh? Qué he encotrao cosas feas en ese archivo de guardado."};

        let consulta = "INSERT INTO savedfiles(player_id, file) VALUES("+id+", '"+savefileTXT+"')";

        try {
            let [rows,fields] = await db.query(consulta);
            return {info:"Correcto", res:"Archivo guardado con éxito."};
        } 
        catch {
            try{
            let consulta = "UPDATE savedfiles SET file = "+savefileTXT+" WHERE player_id = "+id;
            try{
                let [rows,fields] = await db.query(consulta);
                return {info:"Correcto", res:"Archivo sobreescrito con éxito."};
            }
            catch(err){
                logError("Error de consulta en Save: "+err,'game');
                return {info:"Error..."};
            }
            }
            catch{
                logError("Error inesperado de consulta en Save.",'game');
                return {info:"Error..."};
            }
        }
    }
    else return {info:"Incorrecto", res:"Nope..."};
}

module.exports.Load = load;
module.exports.Save = Save;