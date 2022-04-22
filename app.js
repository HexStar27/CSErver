//Zona principal donde se asignan rutas con funciones del servidor.

var express = require("express");
//const http  = require("http");
//const https = require("https");
//const fs    = require("fs");
//const path  = require("path");

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


//Obtencion del certificado SSL para habilitar el uso de HTTPS
//const privateKey = fs.readFileSync( path.join(process.env.PATHCRT, process.env.KEY), 'utf-8');
//const certificate = fs.readFileSync( path.join(process.env.PATHCRT,process.env.CRT), 'utf-8');
//const credentials = {
//    key: privateKey,
//    cert: certificate
//}; //Código zombi :(

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
//body: [tipo] int
app.get("/score", async (req,res)=>{
    let dif = req.body["dif"];
    let tipo = req.body["tipo"];
    if(tipo == null) tipo = 0;
    if(isNaN(dif)) res.json(await pScore.Top10());
    else res.json(await pScore.Score(dif,tipo));
});

//Save a score to the DB
//head: [authorization]
//body: [dif]  number
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
//head: [authorization]
//body: [user] string
app.get("/score/total", auth.validateToken, async (req,res)=>{
    let id = await util.UsernameToID(req.body["user"],true);
    res.json(await pScore.CompleteScore(id));
});

//Calculates the score of a given data
//head: [authorization]
//body: [caso_id]   number
//      [consultas] number
//      [tiempo]    number
//      [examen]    boolean
//      [reto]      boolean
//      [dificultad] number
//      [consulta]  string
app.get("/score/calculate", auth.validateToken, async (req,res)=>{
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
//Returns a random event or an especific one
//body: [id] number
app.get("/event", async (req,res)=>{
    let id = req.body["id"];
    if(isNaN(id)) res.json(await event.getRandomEvent());
    else res.json(await event.getEvent(id));
});


//---------------GAME----------------//
//Save the savefile of a user in the DB
//head: [authorization]
//body: [user] string
//      [save] json
app.post("/save", auth.validateToken, async (req,res)=>{
    let id = await util.UsernameToID(req.body["user"],true);
    let saveFile = req.body["save"];
    res.json(await game.Save(id,saveFile));
});

//Load the savefile to a user of the DB
//head: [authorization]
//body: [user] string
app.get('/load', auth.validateToken, async (req,res)=>{
    let id = await util.UsernameToID(req.body["user"],true);
    res.json(await game.Load(id));
});


//---------------CASOS---------------//
//Return N cases of a given difficulty
//head: [authorization]
//body: [dif]   number
//      [casos] number
app.get('/case', auth.validateToken, async (req,res)=>{
    let dif = req.body["dif"];
    let nCasos = req.body["casos"];
    res.json(await casos.GetCasosAlmacenados(dif,nCasos));
});

//Return one exam case of a given difficulty
//head: [authorization]
//body: [dif]   number
app.get('/case/exam', auth.validateToken, async (req,res)=>{
    let dif = req.body["dif"];
    res.json(await casos.GetCasoExamen(dif));
});

//Return the FINAL case of a given difficulty
//head: [authorization]
app.get('/case/final', auth.validateToken, async (req,res)=>{
    res.json(await casos.GetCasoFinal());
});

//Returns whether a proposed solution is valid or not
//head: [authorization]
//body: [caseid] number
//      [caso]   number
app.get('/case/solve', auth.validateToken, async (req,res)=>{
    let caseID = req.body["caseid"];
    let consulta = req.body["caso"];
    if(util.AntiInjectionStringField(consulta,'app',true))
        res.json(await casos.ResolverCaso(caseID, consulta));
    else res.json({info:"Incorrecto", res:"La consulta es sospechosa"});
});



//const httpServer = http.createServer(app);
//const httpsServer = https.createServer(credentials, app);

//httpServer.listen(process.env.PUERTO);
//httpsServer.listen(process.env.SPUERTO);

app.listen(5000,()=>{
    console.log("Servicio operativo! " + debug.logFullDate());
});
