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
//head: [username]
//      [password]
app.post('/login', async (req,res)=>{
    const{username,password} = req.head;
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
//head: [dif]  int
//      [tipo] int
app.get("/score", async (req,res)=>{
    let dif = req.head["dif"];
    let tipo = req.head["tipo"];
    if(tipo == null) tipo = 0;
    if(isNaN(dif)) res.json(await pScore.Top10());
    else res.json(await pScore.Score(dif,tipo));
});

//Save a score to the DB
//head: [authorization]
//      [dif]  number
//      [punt] number
//      [user] string
//      [used] number
//      [time] number (float)
app.post("/score", auth.validateToken, async (req,res)=>{
    let dif = req.head["dif"];
    let punt = req.head["punt"];
    let used = req.head["used"];
    let time = req.head["time"];
    let id = await util.UsernameToID(req.head["user"],true);
    res.json(await pScore.SaveScore(id,punt,dif,used,time));
});

//Return sum of scores of the given user
//head: [authorization]
//      [user] string
app.get("/score/total", auth.validateToken, async (req,res)=>{
    let id = await util.UsernameToID(req.head["user"],true);
    res.json(await pScore.CompleteScore(id));
});

//Calculates the score of a given data
//head: [authorization]
//      [caso_id]   number
//      [consultas] number
//      [tiempo]    number
//      [examen]    boolean
//      [reto]      boolean
//      [dificultad] number
//      [consulta]  string
app.get("/score/calculate", auth.validateToken, async (req,res)=>{
    let casoID = req.head["caso_id"];
    let consultasUsadas = req.head["consultas"];
    let tiempoEmpleado = req.head["tiempo"];
    let casoExamen = req.head["examen"];
    let retoOpcional = req.head["reto"];
    let dificultad = req.head["dificultad"];
    let consultaEvaluada = req.head["consulta"];

    let p = await pScore.CalcularScore(casoID,consultaEvaluada, consultasUsadas,
                                tiempoEmpleado,casoExamen, retoOpcional, dificultad);
    res.json(p);
});


//---------------EVENT---------------//
//Returns a random event or an especific one
//head: [id] number
app.get("/event", async (req,res)=>{
    //Calculate if id is in header
    if("id" in req.head)
    {
        let id = req.head["id"];
        if(isNaN(id)) res.json(await event.getRandomEvent());
        else res.json(await event.getEvent(id));
    }
    else res.json({Error: "No se ha especificado un id"});
});


//---------------GAME----------------//
//Save the savefile of a user in the DB
//head: [authorization]
//      [user] string
//      [save] json
app.post("/save", auth.validateToken, async (req,res)=>{
    let id = await util.UsernameToID(req.head["user"],true);
    let saveFile = req.head["save"];
    res.json(await game.Save(id,saveFile));
});

//Load the savefile to a user of the DB
//head: [authorization]
//      [user] string
app.get('/load', auth.validateToken, async (req,res)=>{
    let id = await util.UsernameToID(req.head["user"],true);
    res.json(await game.Load(id));
});


//---------------CASOS---------------//
//Return N cases of a given difficulty
//head: [authorization]
//      [dif]   number
//      [casos] number
app.get('/case', auth.validateToken, async (req,res)=>{
    let dif = req.head["dif"];
    let nCasos = req.head["casos"];
    res.json(await casos.GetCasosAlmacenados(dif,nCasos));
});

//Return one exam case of a given difficulty
//head: [authorization]
//      [dif]   number
app.get('/case/exam', auth.validateToken, async (req,res)=>{
    let dif = req.head["dif"];
    res.json(await casos.GetCasoExamen(dif));
});

//Return the FINAL case of a given difficulty
//head: [authorization]
app.get('/case/final', auth.validateToken, async (req,res)=>{
    res.json(await casos.GetCasoFinal());
});

//Returns whether a proposed solution is valid or not
//head: [authorization]
//      [caseid] number
//      [caso]   number
app.get('/case/solve', auth.validateToken, async (req,res)=>{
    let caseID = req.head["caseid"];
    let consulta = req.head["caso"];
    if(util.AntiInjectionStringField(consulta,'app',true))
        res.json(await casos.ResolverCaso(caseID, consulta));
    else res.json({info:"Incorrecto", res:"La consulta es sospechosa"});
});


app.get('/', (req,res)=>{
    res.json({respuesta:"POR FIN"});
});

app.listen(5000,()=>{
    console.log("Servicio operativo! " + debug.logFullDate());
});
