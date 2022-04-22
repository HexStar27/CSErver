//Zona principal donde se asignan rutas con funciones del servidor.

var express = require("express");

var pScore  = require('./score');
var auth    = require('./authentication');
var util    = require('./utility');
var event   = require('./event');
var game    = require('./game');
var debug   = require('./debug');
var casos   = require('./case');

const app = express();
app.use(express.urlencoded( {extended:false} ));
app.use(express.json());


//Log in
//body: [username]
//      [password]
app.post('/login', async (req,res)=>{
    const{username,password} = req.body;
    let accessToken = await auth.Login(username, password);
    if(accessToken.length > 0)
    res.header('authorization',accessToken).json({
        message: 'Usuario correcto',
        token: accessToken
    });
    else 
    res.json({
        message: 'Usuario incorrecto',
        token: ''
    });
});


//---------------SCORE---------------//
//Get Top10 score globally OR the scores of a specific difficulty.
//body: [dif]  int
//      [tipo] int
app.post("/score", async (req,res)=>{
    let dif = req.body["dif"];
    let tipo = req.body["tipo"];
    if(tipo == null) tipo = 0;
    if(isNaN(dif)) res.json(await pScore.Top10());
    else res.json(await pScore.Score(dif,tipo));
});

//Save a score to the DB
//body: [authorization]
//      [dif]  number
//      [punt] number
//      [user] string
//      [used] number
//      [time] number (float)
app.post("/score", auth.validateToken, async (req,res)=>{
    let dif = req.body["dif"];
    let punt = req.body["punt"];
    let used = req.body["used"];
    let time = req.body["time"];
    let id = await util.UsernameToID(req.body["user"],true);
    res.json(await pScore.SaveScore(id,punt,dif,used,time));
});

//Return sum of scores of the given user
//body: [authorization]
//      [user] string
app.post("/score/total", auth.validateToken, async (req,res)=>{
    let id = await util.UsernameToID(req.body["user"],true);
    res.json(await pScore.CompleteScore(id));
});

//Calculates the score of a given data
//body: [authorization]
//      [caso_id]   number
//      [consultas] number
//      [tiempo]    number
//      [examen]    boolean
//      [reto]      boolean
//      [dificultad] number
//      [consulta]  string
app.post("/score/calculate", auth.validateToken, async (req,res)=>{
    let casoID = req.body["caso_id"];
    let consultasUsadas = req.body["consultas"];
    let tiempoEmpleado = req.body["tiempo"];
    let casoExamen = req.body["examen"];
    let retoOpcional = req.body["reto"];
    let dificultad = req.body["dificultad"];
    let consultaEvaluada = req.body["consulta"];

    let p = await pScore.CalcularScore(casoID,consultaEvaluada, consultasUsadas,
                                tiempoEmpleado,casoExamen, retoOpcional, dificultad);
    res.json(p);
});


//---------------EVENT---------------//
//Returns an especific event
//body: [id] number
app.post("/event", async (req,res)=>{   
    let id = req.body["id"];
    res.json(await event.getEvent(id));
});

//Returns a random event
app.get("/event/random", async (req,res)=>{
    res.json(await event.getRandomEvent());
});


//---------------GAME----------------//
//Save the savefile of a user in the DB
//body: [authorization]
//      [user] string
//      [save] json
app.post("/save", auth.validateToken, async (req,res)=>{
    let id = await util.UsernameToID(req.body["user"],true);
    let saveFile = req.body["save"];
    res.json(await game.Save(id,saveFile));
});

//Load the savefile to a user of the DB
//body: [authorization]
//      [user] string
app.post('/load', auth.validateToken, async (req,res)=>{
    let id = await util.UsernameToID(req.body["user"],true);
    res.json(await game.Load(id));
});


//---------------CASOS---------------//
//Return N cases of a given difficulty
//body: [authorization]
//      [dif]   number
//      [casos] number
app.post('/case', auth.validateToken, async (req,res)=>{
    let dif = req.body["dif"];
    let nCasos = req.body["casos"];
    res.json(await casos.GetCasosAlmacenados(dif,nCasos));
});

//Return one exam case of a given difficulty
//body: [authorization]
//      [dif]   number
app.post('/case/exam', auth.validateToken, async (req,res)=>{
    let dif = req.body["dif"];
    res.json(await casos.GetCasoExamen(dif));
});

//Return the FINAL case of a given difficulty
//body: [authorization]
app.post('/case/final', auth.validateToken, async (req,res)=>{
    res.json(await casos.GetCasoFinal());
});

//Returns whether a proposed solution is valid or not
//body: [authorization]
//      [caseid] number
//      [caso]   number
app.post('/case/solve', auth.validateToken, async (req,res)=>{
    let caseID = req.body["caseid"];
    let consulta = req.body["caso"];
    if(util.AntiInjectionStringField(consulta,'app',true))
        res.json(await casos.ResolverCaso(caseID, consulta));
    else res.json({info:"Incorrecto", res:"La consulta es sospechosa"});
});


//Oda a la alegría
app.get('/', (req,res)=>{
    res.json({respuesta:"POR FIN"});
});

app.listen(5000,()=>{
    console.log("Servicio operativo! " + debug.logFullDate());
});
