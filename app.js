//Zona principal donde se asignan rutas con funciones del servidor.

var express = require("express");

var pScore  = require('./score');
var auth    = require('./authentication');
var util    = require('./utility');
var event   = require('./event');
var game    = require('./game');
var debug   = require('./debug');
var casos   = require('./case');
var tService= require('./tableService')

const app = express();
app.use(express.urlencoded( {extended:false} ));
app.use(express.json());

const root = '/game'

//---------------USERS---------------//
// Log in
//body: [username]
//      [password]
app.post(root+'/login', async (req,res)=>{
    username = req.body["username"];
    password = req.body["password"];
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

// Create account
//body: [nickname]
//      [email]
//      [password]
app.post(root+'/signin', async (req,res)=>{
    nick = req.body["nickname"];
    email = req.body["email"];
    password = req.body["password"];

    let result = await game.CreateAccount(nick,email,password);
    if(result["info"] != "Correcto") res.json(result);
    else{
        let accessToken = await auth.Login(email, password);
        if(accessToken.length > 0) 
            res.header('authorization',accessToken).json({message: 'Usuario correcto', token: accessToken});
        else
            res.json({ message: 'Usuario incorrecto', token: '' });
    }
});

//Change Nickname
//body: [authorization]
//      [email]
//      [nickname]
app.post(root+'/nickname', auth.validateToken, async (req,res)=>{
    usuario = req.body["email"];
    nick = req.body["nickname"];
    if(nick == null)
        res.json(await util.GetNickname(usuario));
    else
        res.json(await util.ChangeNickname(usuario,nick));
});


//---------------SCORE---------------//
// Get Top10 score globally OR the scores of a specific difficulty OR of a specific case.
//body: [dif]  int (optional)
//      [tipo] int (optional)
//      [caso] int (optional)
app.post(root+"/score", async (req,res)=>{
    let dif = req.body["dif"];
    let tipo = req.body["tipo"];
    let idCaso = req.body["caso"];
    if(tipo < 0) res.json(await pScore.Top10(idCaso));
    else res.json(await pScore.Score(idCaso,dif,tipo));
});

// Save a score to the DB
//body: [authorization]
//      [user] string
//      [caso] number
//      [punt] number
//      [dif]  number
//      [used] number
//      [time] number (float)
app.post(root+"/score/save", auth.validateToken, async (req,res)=>{
    let id = await util.UsernameToID(req.body["user"],true);
    let caso = req.body["caso"];
    let punt = req.body["punt"];
    let dif = req.body["dif"];
    let used = req.body["used"];
    let time = req.body["time"];
    res.json(await pScore.SaveScore(id,caso,punt,dif,used,time));
});

// Return sum of scores of the given user
//body: [authorization]
//      [user] string
app.post(root+"/score/total", auth.validateToken, async (req,res)=>{
    let id = await util.UsernameToID(req.body["user"],true);
    res.json(await pScore.CompleteScore(id));
});

// Calculates the score of a given data
//body: [authorization]
//      [caso]   number
//      [consultas] number
//      [tiempo]    number
//      [examen]    boolean
//      [reto]      boolean
//      [dificultad] number
//      [consulta]  string
app.post(root+"/score/calculate", auth.validateToken, async (req,res)=>{
    let casoID = req.body["caso"];
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
// Returns an especific event
//body: [id] number
app.post(root+"/event", async (req,res)=>{   
    let id = req.body["id"];
    res.json(await event.getEvent(id));
});

// Returns a random event
app.get(root+"/event/random", async (req,res)=>{
    res.json(await event.getRandomEvent());
});


//---------------GAME----------------//
// Save the savefile of a user in the DB
//body: [authorization]
//      [user] string
//      [save] json
app.post(root+"/save", auth.validateToken, async (req,res)=>{
    let id = await util.UsernameToID(req.body["user"],true);
    let saveFile = req.body["save"];
    res.json(await game.Save(id,saveFile));
});

// Load the savefile to a user of the DB
//body: [authorization]
//      [user] string
app.post(root+'/load', auth.validateToken, async (req,res)=>{
    let id = await util.UsernameToID(req.body["user"],true);
    res.json(await game.Load(id));
});


//---------------CASOS---------------//
// Return the data of a case with a specific id
//body: [authorization]
//      [caso] number
//returns: A case object serialized in the form of a json
app.post(root+'/case/get', auth.validateToken, async(req,res)=>{
    let idCaso = req.body["caso"];
    res.json(await casos.GetCasoEspecifico(idCaso));
});

// Return The id from all available cases that come next to the one sent
//body: [authorization]
//      [id]   number
//      [win]  boolean
//returns: A json array whose elements are case IDs
app.post(root+'/case/next', auth.validateToken, async (req,res)=>{
    let id = req.body["id"];
    let win = req.body["win"];
    res.json(await casos.GetSiguienteCaso(id,win));
});

// User is trying to solve a case
//body: [authorization]
//      [caseid] number
//      [caso]   number
//returns: A bool stating if the proposed query is correct for the case.
app.post(root+'/case/solve', auth.validateToken, async (req,res)=>{
    let caseID = req.body["caseid"];
    let consulta = req.body["caso"];
    res.json(await casos.ResolverCaso(caseID, consulta));
});

// User is trying to query the GAME database
//body: [authorization]
//      [consulta] string
//returns: A json array whose elements are tuples from the GAME database.
app.post(root+'/case/check', auth.validateToken, async(req,res)=>{
    let consulta = req.body["consulta"];
    res.json(await casos.RealizarConsulta(consulta));
});


//----------OTROS SERVICIOS----------//
// Return tables availables from the codes given.
//body: [authorization]
//      [codigos] array
//returns: A json array whose elements are tuples from the "tablesUnlockCode" table.
app.post(root+'/meta', auth.validateToken, async (req,res)=>{
    let codigos = req.body["codigos"];
    res.json(await tService.GetTablesAvailables(codigos));
});

// Return columns from a given table.
//body: [authorization]
//      [table] array
//returns: A json array whose elements are lists of column names per table.
app.post(root+'/meta/col', auth.validateToken, async (req,res)=>{
    let table = req.body["table"];
    res.json(await tService.GetTableColumns(table));
});

app.listen(5000,()=>{
    console.log("Servicio operativo! " + debug.logFullDate());
});
