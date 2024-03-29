const debug = require("./debug");
var db = require("./mysql");

/**
 * Devuelve verdadero si hay un jugador con esa ID en la BD
 * @param {Number} id 
 * @param {*} checkInjection indica si buscar o no inyecciones en la id
 * @returns {boolean}
 */
async function PlayerExist(id,checkInjection)
{
    let valid = true;
    if(checkInjection) valid = AntiInjectionNumberField(id,'utility');

    if(valid)
    {
        let consulta = "SELECT id FROM players WHERE id = "+id;
        try{
            let [rows,fields] = await db.baseP.query(consulta);
            return rows.length != 0;
        }
        catch(err){
            debug.logError("Error de consulta en PlayerExist: "+err,'utility');
            return false;
        }
    }
    return false;
}

/**
 * Devuelve la id del usuario con el nombre indicado (o null si no existe)
 * @param {string} username (email)
 * @param {boolean} checkInjection 
 * @returns id del usuario o -1 si no se ha encontrado.
 */
async function UsernameToID(username,checkInjection,verbose = true)
{
    let valid = true;
    if(checkInjection) valid = AntiInjectionStringField(username,'utility');

    if(valid)
    {
        let consulta = "SELECT id FROM players WHERE email = '"+username+"'";
        try{
            let [rows,fields] = await db.baseP.query(consulta);
            if(rows.length == 0){
                if(verbose) debug.logError("No se ha encontrado una id para el usuario "+username,'utility');
                return -1;
            }
            else return rows[0]["id"];
        }
        catch(err){
            debug.logError("Error de consulta en UsernameToID: "+err,'utility');
            return null;
        }
    }
    return null;
}

/**
 * Cambia el nickname de un jugador...
 * @param {string} email 
 * @param {string} newNick 
 * @returns 
 */
async function ChangeNickname(email, newNick)
{
    if(!SearchForKeyWords(newNick)) {
        debug.logError("Error de petición, es sospechoso el valor "+newNick,'utility');
        return {info:"Error..."};
    }
    let id = await UsernameToID(email,true);
    if(id == -1) return {info:"Error... Usuario no encontrado"}

    //Comprobar que no exista ya un usuario con ese nickname.
    let consulta = "SELECT id FROM players WHERE nickname = '"+newNick+"'"
    try {
        let [rows,fields] = await db.baseP.query(consulta);
        if(rows.length != 0) return {info:"Error... Ya existe un jugador con ese nickname."}
    } catch (err) {
        debug.logError("Error de consulta en ChangeNickname al comprobar si ya existía: "+err, 'utility');
        return {info:"Error..."};
    }

    //Cambiar el nickname
    consulta = "UPDATE players SET nickname = '"+newNick+"' WHERE id = "+id;
    try {
        let [rows,fields] = await db.baseP.query(consulta);
        return {info:"Correcto", res:"Nickname cambiado correctamente." };
    } catch (err) {
        debug.logError("Error de consulta en ChangeNickname: "+err, 'utility');
        return {info:"Error..."};
    }
}

/**
 * Devuelve el nickname del jugador...
 * @param {string} email 
 * @returns 
 */
 async function GetNickname(email)
 {
     if(!SearchForKeyWords(email)) {
         debug.logError("Error de petición, es sospechoso el valor "+email,'utility');
         return {info:"Error..."};
     }
     //Cambiar el nickname
     let consulta = "SELECT nickname FROM players WHERE email = '"+email+"'";
     try {
         let [rows,fields] = await db.baseP.query(consulta);
         return {info:"Correcto", res:rows[0]['nickname'] };
     } catch (err) {
         debug.logError("Error de consulta en GetNickname: "+err, 'utility');
         return {info:"Error..."};
     }
 }

 async function NicknameExist(nick)
 {
    if(!SearchForKeyWords(email)) {
        debug.logError("Error de petición, es sospechoso el valor "+nick,'utility');
        return {info:"Error..."};
    }
    
    let consulta = "SELECT COUNT(nickname) AS val FROM players WHERE nickname = '"+nick+"'";
    try {
        let [rows,fields] = await db.baseP.query(consulta);
        return rows[0]['val'] > 0;
    } catch (err) {
        debug.logError("Error de consulta en NicknameExist: "+err, 'utility');
        return false;
    }

 }

/**
 * Devuelve verdadero si el usuario y la contraseña coinciden con los de la BD
 * @param {*} username 
 * @param {*} password 
 * @param {*} checkInjection indica si buscar o no inyecciones en las cadenas pasadas
 * @returns 
 */
async function ValidLogin(username,password,checkInjection)
{
    let valid = true;
    if(checkInjection)
    {
        valid = AntiInjectionStringField(username,'utility',false) && 
                AntiInjectionStringField(password,'utility',true);
    }

    if(valid)
    {
        let consulta = "SELECT email FROM players WHERE email = '"+username+"' AND password = '"+password+"'";
        try{
            let [rows,fields] = await db.baseP.query(consulta);
            return rows.length > 0;
        }
        catch(err)
        {
            debug.logError("Error de consulta en ValidLogin, "+err,'utility');
            return false;   
        }
    }
    return false;
}

/**
 * Devuelve verdadero si el campo id es un número
 * @param {*} id cualquier número a comprobar su validez
 * @param {String} name Nombre del módulo
 * @returns {Boolean}
 */
function AntiInjectionNumberField(id, name)
{
    let wrong = isNaN(id);
    if(wrong) debug.logSQLInjectionWarning(name,id);
    return !wrong;
}

/**
 * Devuelve verdadero si el campo data es una cadena limpia de inyecciones
 * @param {*} data Supuesta cadena a validar
 * @param {string} name Nombre del módulo
 * @param {boolean} pass Indica si el dato representa una contraseña 
 * @returns 
 */
function AntiInjectionStringField(data,name,pass)
{
    //Esto habrá que modificarlo según los carácteres válidos que permita el cifrado
    //de contraseña en unity.
    const invalidChars = ['"',"'"];
    let isString = typeof(data) == typeof("a");
    if(isString)
    {
        let n = invalidChars.length;

        let valid = true;
        for(let i = 0; (i < n) && valid; i++){
            //Si no los encuentra, sigue siendo válido
            valid = (data.indexOf(invalidChars[i]) == -1) && valid;
        }

        if(!valid) debug.logSQLInjectionWarning(name,data);
        return valid;
    }

    return false;
}

/**
 * Devuelve verdadero si la cadena pasada no contiene keywords de mysql
 * @param {string} data 
 * @param {string} name 
 */
function SearchForKeyWords(data, name)
{
    const invalidStrings = ["INSERT ","DELETE ","SELECT ","UPDATE ", "CREATE ", "USE ", 
    "TABLE ", "ALTER ", "DROP ", "VALUES ", "VIEW "];
    let isString = typeof(data) == typeof("a");
    
    if(isString)
    {
        upper = data.toUpperCase();
        let valid = true;
        for(let i = 0; (i < invalidStrings.length) && valid; i++){
            valid = (!data.includes(invalidStrings[i])) && valid;
        }
        if(!valid) debug.logSQLInjectionWarning(name,data);
        return valid;
    }
    return false;
}

/**
 * Devuelve un diccionario con el coste, las filas y el tiempo de una consulta EXPLAIN
* @param {Number} casoID 
* @param {*} consulta 
 */
async function parseExplain(casoID,consulta)
{
    //1º Obtener cadenas del EXPLAIN
    let expl = "EXPLAIN ANALYZE ";
    let resultado ="";
    let resultado2 = "";
    let consultaBuena ="";
    
    try{
        let[rows,fields] = await db.baseP.query("SELECT consulta FROM cases WHERE id = "+casoID);
        consultaBuena = rows[0]["consulta"];
    }catch(err){
        debug.logError("Error de consulta en parseExplain (No existe el caso): "+err,'utility');
        return {};
    }

    try{
        let[rows,fields] = await db.gameP.query(expl + consultaBuena);
        resultado2 = rows[0]["EXPLAIN"];
    }catch(err){
        debug.logError("Error de consulta en parseExplain, NO DEBERÍA DE EXISTIR: "+err,'utility');
        return {};
    }

    try{
        let [rows,fields] = await db.gameP.query(expl + consulta);
        resultado = rows[0]["EXPLAIN"];
    }
    catch(err){
        debug.logError("Error de consulta en parseExplain: "+err,'utility');
        return {};
    }

    //2º Encontrar valores en cadenas
    [costes, nFilas, time] = FindValuesInExplain(resultado);
    [c2,n2,t2] = FindValuesInExplain(resultado2);

    //3º Devolver valores en diccionario
    return {cost:costes-c2, rows:nFilas-n2, time:time-t2};
}

/**
 * Devuelve un número aleatorio entre min y max
 * @param {Number} min Valor mínimo inclusivo
 * @param {Number} max Valor máximo exclusivo
 * @returns {Number} numero "aleatorio"
 */
function randBetween(min,max)
{
    return Math.floor(Math.random()*(max-min) + min);
}


/**
 * Obtiene los valores de la cadena de una consulta Explain
 * @param {String} resultado 
 * @returns 
 */
function FindValuesInExplain(resultado)
{
    //Costes
    let costes = 0;
    for(let i = 0; i < resultado.length-5; i++)
    {
        if(resultado[i] == 'c')
        {
            if(resultado.substring(i,i+5) === "cost=")
            {
                let j = i+5;
                for(; j < resultado.length-1 && resultado[j] != ' '; j++){}
                
                costes += parseFloat(resultado.substring(i+5,j));
            }
        }
    }
    //rows
    let nFilas = 0;
    for(let i = 0; i < resultado.length-5; i++)
    {
        if(resultado[i] == 'r')
        {
            if(resultado.substring(i,i+5) === "rows=")
            {
                let j = i+5;
                for(; j < resultado.length-1 && (resultado[j] != ' ' && resultado[j] != ')'); j++){}
                
                nFilas += parseInt(resultado.substring(i+5,j));
            }
        }
    }
    nFilas *= 0.5;

    //time
    let time = 0;
    for(let i = 0; i < resultado.length-5; i++)
    {
        if(resultado[i] == 't')
        {
            if(resultado.substring(i,i+5) === "time=")
            {
                let j = i+5;
                for(; j < resultado.length-1 && resultado[j] != ' '; j++){}
                
                let intervalo = resultado.substring(i+5,j);
                let sumParcial = 0;
                for(let k = 0; k < intervalo.length-1; k++)
                {
                    if(intervalo[k] == '.' && intervalo[k+1] == '.')
                    {
                        sumParcial = parseFloat(intervalo.substring(0,k)) + 
                            parseFloat(intervalo.substring(k+2,intervalo.length));
                        
                        break;
                    }
                }

                time += parseFloat(sumParcial*0.5);
            }
        }
    }
    return [costes, nFilas, time];
}


module.exports.PlayerExist = PlayerExist;
module.exports.AntiInjectionNumberField = AntiInjectionNumberField;
module.exports.AntiInjectionStringField = AntiInjectionStringField;
module.exports.randBetween = randBetween;
module.exports.ValidLogin = ValidLogin;
module.exports.UsernameToID = UsernameToID;
module.exports.ChangeNickname = ChangeNickname;
module.exports.GetNickname = GetNickname;
module.exports.NicknameExist = NicknameExist;
module.exports.SearchForKeyWords = SearchForKeyWords;
module.exports.parseExplain = parseExplain;