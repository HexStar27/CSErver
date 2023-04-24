//Funciones relacionadas con la puntuación de los jugadores.
var db = require("./mysql").baseP;
var util = require("./utility");
var puzzle = require("./case");
const { logError } = require("./debug");

/**
 * Devuelve los 10 jugadores con más puntuación hasta la fecha
 */
async function Top10(idCaso)
{
    let consulta = "";
    if(idCaso < 0)
        consulta = "SELECT p.nickname, sum(ps.score) as score FROM scores as ps INNER JOIN players as p ON ps.player_id = p.id GROUP BY player_id ORDER BY sum(score) DESC limit 10";
    else 
        consulta ="SELECT p.nickname, ps.score as score FROM scores as ps INNER JOIN players as p ON ps.player_id = p.id WHERE ps.case_id = "+idCaso+" ORDER BY score DESC limit 10";
    try{
        let [rows,fields] = await db.query(consulta);
        return {info:"Correcto", res:rows};
    }
    catch(err){
        logError("Error de consulta en Top10: "+err, 'score');
        return {info:"Error..."};
    }
}

/**
 * Devuelve un array (de hasta 1024 valores) con las puntuaciones de los jugadores en esa dificultad
 * @param {Number} dif dificulty or case_id depending on the value of 'tipo'
 * @param {Number} tipo
 */
async function Score(dif, tipo)
{
    if(util.AntiInjectionNumberField(dif,"score") &&
        util.AntiInjectionNumberField(tipo,"score"))
    {
        dif = parseInt(dif);
        tipo = parseInt(tipo);
        var consulta = "";
        switch(tipo)
        {
            case 0: //Puntuación (dificultad especifica)
                consulta = "SELECT score FROM scores WHERE difficulty = "+dif+" ORDER BY score ASC limit 1024";
                break;
            case 1: //Consultas Usadas (dificultad especifica)
                consulta = "SELECT used_queries FROM scores WHERE difficulty = "+dif+" ORDER BY used_queries ASC limit 1024";
                break;
            case 2: //Tiempo empleado (dificultad especifica)
                consulta = "SELECT time_spent FROM scores WHERE difficulty = "+dif+" ORDER BY time_spent ASC limit 1024";
                break;
            case 3: //Todo (dificultad especifica)
                consulta = "SELECT player_id, score, used_queries, time_spent FROM scores WHERE difficulty = "+dif+" ORDER BY score ASC limit 1024";
                break;
            case 4: //Todo (caso específico)
                consulta = "SELECT player_id score, used_queries, time_spent FROM scores WHERE case_id = "+dif+" ORDER BY score ASC limit 1024";
                break;
        }

        try{
            let [rows,fields] = await db.query(consulta);
            return {info:"Correcto", res:rows};
        }
        catch(err){
            logError("Error de consulta en Score: "+err,'score');
            return {info:"Error..."};
        }
    }
    else return {info:"Incorrecto", res:"K COÑO ESTÁS INTENTANTO JOPUTA"};
}

/**
 * Guarda en la BD los datos de la puntuación indicada
 * @param {Number} id ID del jugador
 * @param {Number} caso
 * @param {Number} punt 
 * @param {Number} dif 
 * @param {Number} used
 * @param {Number} time
 */
 async function SaveScore(id,caso,punt,dif,used,time)
 {
    if(util.AntiInjectionNumberField(dif,'score') && 
        util.AntiInjectionNumberField(id,'score') &&
        util.AntiInjectionNumberField(punt,'score') &&
        util.AntiInjectionNumberField(used,'score') && 
        util.AntiInjectionNumberField(time,'score') &&
        util.AntiInjectionNumberField(caso,'score'))
    {
        let c = parseInt(caso);
        let d = parseInt(dif);
        let p = parseInt(punt);
        let u = parseInt(used);
        let t = parseFloat(time);

        //TODO: Comprobar si ya hay una score del jugador en ese caso, si lo es, 
        //      simplemente actualizar en vez de insertar
        let qComprobar = "SELECT score FROM scores WHERE player_id = "+id+" AND case_id = "+c;
        try{
            let [rows,fields] = await db.query(qComprobar);
            
            var consulta;
            if(rows.length <= 0) //Hay que insertar
                consulta = "INSERT INTO scores (player_id, case_id, difficulty, score, used_queries, time_spent) VALUES ("+id+","+c+","+d+","+p+","+u+","+t+")";
            else{ //Sólo actualizar
                var oldP = parseInt(rows[0]["score"]); //Recemos
                console.log(rows);
                console.log(rows[0]);
                console.log(rows[0]["score"]);
                if( p > oldP){
                    consulta = "UPDATE scores SET score = "+p+" WHERE player_id = "+id+" AND case_id = "+c;
                }
                else{
                    return {info:"Correcto", res:"No ha hehco falta guardarlo :v"};
                }
            }
            
            try{
                let [rows,fields] = await db.query(consulta);
                return {info:"Correcto", res:"Puntuación guardada correctamente."};
            }
            catch(err){
                logError("Error de consulta en SaveScore: "+err, 'score');
                return {info:"Error..."};
            }

        }catch(err){
            logError("Error de consulta en SaveScore al comprobar puntuacion: "+err, 'score');
            return {info:"Error..."};
        }
    }
    else return {info:"Incorrecto", res:"Faltan datos o son incorrectos."};
 }

/**
 * Devuelve la puntuación correspondiente de los datos de la consulta dada.
 * @param {Number} casoID
 * @param {String} consultaEvaluada 
 * @param {Number} consultasUsadas 
 * @param {Number} tiempoEmpleado 
 * @param {Boolean} casoExamen 
 * @param {Boolean} retoOpcional 
 * @param {Number} dificultad 
 * @returns 
 */
async function CalcularScore(casoID, consultaEvaluada, consultasUsadas, tiempoEmpleado, casoExamen, retoOpcional, dificultad)
{
    //1º Comprobar éxito
    let exito = await puzzle.ResolverCaso(casoID, consultaEvaluada);
    if(exito["info"] != "Correcto") return exito;
    let continuar = exito["res"];
    if(!continuar) return {info:"Incorrecto",res:"La consulta no soluciona el caso."};
    
    //2º Obtener datos de EXPLAIN ANALYZE
    let datos = await util.parseExplain(casoID,consultaEvaluada);
    //datos-> "cost", "rows", "time"
    
    //3º Calcular fórmula (Temporal)
    let a=1.85, b=10;
    let puntConsulta = b/(b+a*(consultasUsadas-1)*(consultasUsadas-1));
    a=0.24;
    let puntTiempo = b/(b+a*(tiempoEmpleado-1));
    let puntEfic;
    if(datos["cost"] >= 0)
        puntEfic = 2*dificultad/(2*dificultad+datos["cost"]*datos["cost"]);
    else
        puntEfic = 1;
    //Puntuación máxima = 200*dificultad
    let puntuacion = (100*puntConsulta + 100*puntTiempo)*dificultad + 20*puntEfic;
    //Puntuación máxima verdadera = 200*dificultad + 200
    if(casoExamen) puntuacion+=100;
    if(retoOpcional) puntuacion+=100;
    //Reducción por eficiencia

    puntuacion = parseInt(puntuacion);
    return {info:"Correcto", res:puntuacion, otros:datos};
}

/**
 * Devuelve la puntuación completa del jugador indicado, es decir,
 * la suma de las puntuaciones de cada caso completado
 * @param {*} id ID del jugador
 * @returns 
 */
async function CompleteScore(id)
{
    if(util.AntiInjectionNumberField(id,'score'))
    {
        id = parseInt(id);
        var consulta = "SELECT SUM(score) FROM scores WHERE player_id = "+id+" GROUP BY player_id";
        
        try{
            let [rows,fields] = await db.query(consulta);
            if (rows.length == 0) return {info:"Incorrecto", res:"Este jugador no tiene puntuación."};
            return {info:"Correcto", res:rows[0]["SUM(score)"]};
        }
        catch(err){
            logError("Error de consulta en CompleteScore: "+err,'score');
            return {info:"Error..."};
        }
    }
    else return {info:"Incorrecto", res:"Casi cuela."};
}

module.exports.Top10 = Top10;
module.exports.Score = Score;
module.exports.SaveScore = SaveScore;
module.exports.CalcularScore = CalcularScore;
module.exports.CompleteScore = CompleteScore;