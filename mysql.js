//Función para acceder a la base de datos :)

require('dotenv').config();
var mysql = require("mysql2");


/**
 * Pool de conexiones a la base de datos que gestiona TODO
 */
const baseConnection = mysql.createPool({
    connectionLimit: process.env.MAXCONEXIONES,
    host: process.env.DB_HOST,
    user: process.env.DB_BASE_USER,
    password: process.env.DB_BASE_PASS,
    database: process.env.DB_BASE_NAME,
    waitForConnections: true,
    queueLimit: 0
});
const promiseBase = baseConnection.promise();

/**
 * Pool de conexiones a la base de datos que contiene las tablas del juego 
 * accesibles para los jugadores
 */
 const gameConnection = mysql.createPool({
    connectionLimit: process.env.MAXCONEXIONES,
    host: process.env.DB_HOST,
    user: process.env.DB_GAME_USER,
    password: process.env.DB_GAME_PASS,
    database: process.env.DB_GAME_NAME,
    waitForConnections: true,
    queueLimit: 0
})
const promiseGame = gameConnection.promise();


//module.exports.base = baseConnection;
//module.exports.game = gameConnection;
module.exports.baseP = promiseBase;
module.exports.gameP = promiseGame;