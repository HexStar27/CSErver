CREATE DATABASE IF NOT EXISTS `db_game` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `db_game`;

--
-- Estructura para la tabla `alojadoEn`
--

CREATE TABLE `alojadoEn` (
  `vivienda` int NOT NULL,
  `ciudadano` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura para la tabla `asistenteVoz`
--

CREATE TABLE `asistenteVoz` (
  `id` int NOT NULL,
  `dniPropietario` int NOT NULL,
  `fecha` datetime NOT NULL,
  `log` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura para la tabla `ciudadanos`
--

CREATE TABLE `ciudadanos` (
  `dni` int NOT NULL,
  `nombre` varchar(70) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `edad` int DEFAULT NULL,
  `colorPelo` varchar(30) DEFAULT NULL,
  `altura` float DEFAULT NULL,
  `especie` varchar(40) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura para la tabla `corgomatic`
--

CREATE TABLE `corgomatic` (
  `matricula` varchar(7) NOT NULL,
  `fecha` date NOT NULL,
  `cambios` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura para la tabla `correos`
--

CREATE TABLE `correos` (
  `id` int NOT NULL,
  `fecha` datetime NOT NULL,
  `emisor` varchar(50) NOT NULL,
  `destinatario` varchar(50) NOT NULL,
  `asunto` varchar(256) NOT NULL,
  `contenido` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura para la tabla `grabacionRestaurante`
--

CREATE TABLE `grabacionRestaurante` (
  `transcripcion` varchar(200) NOT NULL,
  `hora` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura para la tabla `megaMilky_productos`
--

CREATE TABLE `megaMilky_productos` (
  `id` int NOT NULL,
  `nombre` varchar(80) NOT NULL,
  `precio` float NOT NULL,
  `tipo` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'otros',
  `stock` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura para la tabla `megaMilky_ventas`
--

CREATE TABLE `megaMilky_ventas` (
  `id` int NOT NULL,
  `dniCliente` int NOT NULL,
  `fecha` datetime NOT NULL,
  `idProducto` int NOT NULL,
  `cantidad` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura para la tabla `muricaGuns_armasRegistradas`
--

CREATE TABLE `muricaGuns_armasRegistradas` (
  `numSerie` int UNSIGNED NOT NULL,
  `dni` int NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `marca` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura para la tabla `paulsPizzeria_inventario`
--

CREATE TABLE `paulsPizzeria_inventario` (
  `id` int NOT NULL,
  `objeto` varchar(80) NOT NULL,
  `tipo` varchar(32) NOT NULL DEFAULT 'varios',
  `proveedor` varchar(32) DEFAULT NULL,
  `existencias` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura para la tabla `pingBusquedas`
--

CREATE TABLE `pingBusquedas` (
  `correo` varchar(40) NOT NULL,
  `busqueda` varchar(200) NOT NULL,
  `fecha` datetime NOT NULL,
  `ip` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura para la tabla `rinconDelTurro_mesas`
--

CREATE TABLE `rinconDelTurro_mesas` (
  `idReserva` int NOT NULL,
  `dniCliente` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura para la tabla `rinconDelTurro_reservas`
--

CREATE TABLE `rinconDelTurro_reservas` (
  `id` int NOT NULL,
  `comensales` int NOT NULL,
  `fecha` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura para la tabla `rutas`
--

CREATE TABLE `rutas` (
  `matricula` varchar(7) NOT NULL,
  `zonaOrigen` varchar(80) NOT NULL,
  `zonaDestino` varchar(80) NOT NULL,
  `distanciaViaje` float NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura para la tabla `transbordos`
--

CREATE TABLE `transbordos` (
  `id` int NOT NULL,
  `numPuerto` int NOT NULL,
  `fechaLlegada` date NOT NULL,
  `entidadSolicitante` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura para la tabla `transbordos_empleados`
--

CREATE TABLE `transbordos_empleados` (
  `idTransbordo` int NOT NULL,
  `dniEmpleado` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura para la tabla `vehiculos`
--

CREATE TABLE `vehiculos` (
  `matricula` varchar(7) NOT NULL,
  `idTitular` int DEFAULT NULL,
  `marca` varchar(70) NOT NULL,
  `color` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura para la tabla `viviendas`
--

CREATE TABLE `viviendas` (
  `id` int NOT NULL,
  `direccion` varchar(200) NOT NULL,
  `titular` int DEFAULT NULL,
  `esPiso` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
