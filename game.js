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

        savefileTXT = savefileTXT.substring(1,savefileTXT.length-1);
        let consulta = "INSERT INTO savedfiles(file, player_id) VALUES('"+savefileTXT+"', "+id+")";
        
        try {
            //console.log(consulta);
            let [rows,fields] = await db.query(consulta);
            return {info:"Correcto", res:"Archivo guardado con éxito."};
        } 
        catch {
            try{
            let consulta = "UPDATE savedfiles SET file = '"+savefileTXT+"' WHERE player_id = "+id;
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

/**
 * @param {string} nick apodo
 * @param {string} email email
 * @param {string} password contraseña cifrada
 */
async function CreateAccount(nick,email,password)
{
    if( check.AntiInjectionStringField(nick,'game') &&
        check.AntiInjectionStringField(email,'game') &&
        check.AntiInjectionStringField(password,'game'))
    {
        //1º Comprobar que ni el nickname, ni email estén repetidos.
        let id = await check.UsernameToID(email,false);
        if(id >= 0) return {info:"Incorrecto", res:"Ya existe una cuenta con ese email."};
        else{
            if(await check.NicknameExist(nick))
                return {info:"Incorrecto", res:"Ya existe una cuenta con ese apodo."};
            else{
                //2º Añadimos cuenta a base de datos
                let consulta = "INSERT INTO `players` (`email`, `nickname`, `password`) VALUES ('"+email+"','"+nick+"','"+password+"')";
                try{
                    let [rows,fields] = await db.query(consulta);
                    return {info:"Correcto", res:"Cuenta creada con éxito."};
                }catch(err) {
                    logError("Error inesperado de consulta en CreateAccount:"+err,'game');
                    return {info:"Error..."};
                }
            }
        }
    }
    else return {info:"Incorrecto", res:"No se pudo crear la cuenta."};
}

module.exports.Load = load;
module.exports.Save = Save;
module.exports.CreateAccount = CreateAccount;