//Funciones relacionadas con la entrega y corrección de casos.
var db = require("./mysql");
var util = require("./utility");
const { logError } = require("./debug");



/**
 * Devuelve un número de casos especificado guardados en la base de datos
 * @param {Number} dif 
 * @param {Number} nCasos 
 */
async function GetCasosAlmacenados(dif,nCasos)
{
    if (util.AntiInjectionNumberField(dif,"case") &&
        util.AntiInjectionNumberField(nCasos,"case"))
    {
        let consulta = "SELECT id, data, dif from cases where dif = "+dif+" AND isExam = FALSE"
        
        try {
            let [rows,fields] = await db.baseP.query(consulta);
            let n = rows.length;
            let total = nCasos;
            let lista = [];

            if(n < total) total = n;

            for (let i=0; i < n; i++) lista.push(rows[i]);
            lista.sort((a,b)=>{return 0.5 - Math.random()});
            let conjunto = lista.slice(0,total);
            conjunto.forEach(elem => {
                elem.concat("#");
            });
            return {info:"Correcto", res:conjunto};
        } 
        catch(err) {
            logError("Error de consulta en GetCasosAlmacenados: "+err,'case');
            return {info:"Error..."};
        }
    }
    else return {info:"Incorrecto", res:"K COÑO ESTÁS INTENTANTO JOPUTA"};
}


/**
 * Devuelve los datos de un caso examen preparado para esa dificultad
 * @param {Number} dif 
 */
async function GetCasoExamen(dif)
{
    if (util.AntiInjectionNumberField(dif,"case"))
    {
        let consulta = "SELECT id, data, dif from cases where dif = "+dif+" AND isExam = TRUE AND isFinal = FALSE";
        
        try{
            let [rows,fields] = await db.baseP.query(consulta);
            let aleatorio = util.randBetween(0,rows.length);
            if(rows.length == 0) return {info:"Correcto", res:[]};
            return {info:"Correcto", res:rows[aleatorio]};
        }
        catch(err){
            logError("Error de consulta en GetCasoExamen: "+err,'case');
            return {info:"Error..."};
        }        
    }
    else return {info:"Incorrecto", res:"K COÑO ESTÁS INTENTANTO JOPUTA"};
}


/**
 * Devuelve un caso en res con la dificultad máxima.
 */
async function GetCasoFinal()
{
    let consulta = "SELECT id, data, dif from cases where isFinal = TRUE";

    try {
        let [rows,fields] = await db.baseP.query(consulta);
        let aleatorio = util.randBetween(0,rows.length);
        if(rows.length == 0) return {info:"Correcto", res:[]};
        return {info:"Correcto", res:rows[aleatorio]};
    } 
    catch(err) {
        logError("Error de consulta en GetCasiFinal: "+err,'case');
        return{info:"Error..."};
    }
}


/**
 * Devuelve si la consulta es correcta
 * @param {String} qPropuesta 
 * @param {Number} casoID
 */
async function ResolverCaso(casoID, qPropuesta)
{
    casoID = parseInt(casoID);
    if(util.AntiInjectionNumberField(casoID,'case'))
    {
        let resultado;
        let solucion;
        let consulta = "SELECT consulta from cases where id = "+casoID;

        let qSol = "";
        try{
            let [rows,fields] = await db.baseP.query(consulta);
            qSol = rows[0]["consulta"];
        }catch(err){
            logError("Error de consulta en ResolverCaso: "+err,'case');
            return {info:"Error...", res:"El caso que se está intentando resolver no existe (?)"};
        }

        try{ //Se obtiene la solución almacenada del caso
            let [r1,f1] = await db.gameP.query(qSol);
            solucion = r1;
        }catch(err){
            logError("Error de consulta al obtener la solución en ResolverCaso: "+err,'case');
            return {info:"Error..."};
        }

        try{ //Se obtiene la solución propuesta por el jugador
            let [r2,f2] = await db.gameP.query(qPropuesta);
            resultado = r2;
        }catch(err){
            logError("Error de consulta al obtener la propuesta en ResolverCaso: "+err,'case');
            return {info:"Error..."};
        }

        let esIgual = jsonArrayEquals(resultado,solucion);
        
        //Si por algún fallo ambas cadenas están vacías, no se contará como correcta la solución.
        let noVacio = solucion.length != 0;
        
        if(noVacio) return {info:"Correcto", res:esIgual};
        else{
            logError("Error, un caso nunca debería dar como solución una consulta vacía",'case');
            return {info:"Error... Algo ha pasado con el caso(?)"};
        }
    }
    else return {info:"Incorrecto", res:false};
}

function isEqualJson(a,b){
    k1 = Object.keys(a);
    k2 = Object.keys(b);
    return k1.length === k2.length && Object.keys(a).every(key=>a[key] == b[key]);
}

function jsonArrayEquals(a,b){
    if (Array.isArray(a) && Array.isArray(b)){
        let contenido = true;
        let i = 0;
        for (; i < a.length && contenido; i++) {
            contenido = false;
            for (let j = 0; j < b.length; j++) {
                contenido = isEqualJson(a[i],b[i]);
            }
        }
        return i == a.length;
    }
    else return false;
}


module.exports.GetCasosAlmacenados = GetCasosAlmacenados;
module.exports.GetCasoExamen = GetCasoExamen;
module.exports.GetCasoFinal = GetCasoFinal;
module.exports.ResolverCaso = ResolverCaso;