//Funciones para validar usuarios

require('dotenv').config();
const jwt = require('jsonwebtoken');
const util = require('./utility');

/**
 * Genera un token para que lo pase el usuario y se pueda autentificar
 * @param {*} info 
 * @returns 
 */
function generateAcessToken(info)
{
    //El tiempo de expiración es opcional
    return jwt.sign(info,process.env.SECRET);
}

/**
 * Comprueba la validez del token recibido, no es necesario saber el usuario
 * @param {*} req 
 * @param {*} res 
 * @param {*} next
 */
function validateToken(req,res,next)
{
    const accessToken = req.headers['authorization'];
    if(!accessToken) res.json({info:"Incorrecto", res:"No se ha encontrado ninguna clave de acceso en 'authorization'"});

    jwt.verify(accessToken, process.env.SECRET, (err, info)=>{
        if(err) res.json({info:"Incorrecto", res:'Token incorrecto o expirado'});
        else
        {
            req.info = info;
            next();
        }
    });

}

async function Login(username, password)
{
    //Consulta BD para ver si existe usuario
    let v = await util.ValidLogin(username,password,true);
    if(!v) return "";
    //Información a encriptar para generar el token
    const info = {username : username, password : password};
    
    return generateAcessToken(info);
}

module.exports.generateAcessToken = generateAcessToken;
module.exports.validateToken = validateToken;
module.exports.Login = Login;