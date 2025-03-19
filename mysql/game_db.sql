CREATE DATABASE IF NOT EXISTS `db_game`;
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
  `transcripcion` int NOT NULL,
  `hora` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura para la tabla `megaMilky_productos`
--

CREATE TABLE `megaMilky_productos` (
  `id` int NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `precio` float NOT NULL,
  `tipo` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'otros',
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
  `numSerie` int NOT NULL,
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
  `objeto` varchar(50) NOT NULL,
  `tipo` varchar(50) NOT NULL DEFAULT 'varios',
  `proveedor` varchar(50) DEFAULT NULL,
  `existencias` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura para la tabla `pingBusquedas`
--

CREATE TABLE `pingBusquedas` (
  `correo` int NOT NULL,
  `busqueda` varchar(200) NOT NULL,
  `fecha` datetime NOT NULL,
  `ip` int NOT NULL
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
  `matricula` varchar(4) NOT NULL,
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

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alojadoEn`
--
ALTER TABLE `alojadoEn`
  ADD KEY `ciudadano` (`ciudadano`),
  ADD KEY `vivienda_2` (`vivienda`),
  ADD KEY `vivienda_3` (`vivienda`);

--
-- Indices de la tabla `asistenteVoz`
--
ALTER TABLE `asistenteVoz`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `ciudadanos`
--
ALTER TABLE `ciudadanos`
  ADD PRIMARY KEY (`dni`);

--
-- Indices de la tabla `correos`
--
ALTER TABLE `correos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `grabacionRestaurante`
--
ALTER TABLE `grabacionRestaurante`
  ADD UNIQUE KEY `hora` (`hora`);

--
-- Indices de la tabla `megaMilky_productos`
--
ALTER TABLE `megaMilky_productos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `megaMilky_ventas`
--
ALTER TABLE `megaMilky_ventas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `muricaGuns_armasRegistradas`
--
ALTER TABLE `muricaGuns_armasRegistradas`
  ADD PRIMARY KEY (`numSerie`);

--
-- Indices de la tabla `paulsPizzeria_inventario`
--
ALTER TABLE `paulsPizzeria_inventario`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `rinconDelTurro_mesas`
--
ALTER TABLE `rinconDelTurro_mesas`
  ADD UNIQUE KEY `idReserva` (`idReserva`);

--
-- Indices de la tabla `rinconDelTurro_reservas`
--
ALTER TABLE `rinconDelTurro_reservas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `transbordos`
--
ALTER TABLE `transbordos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `transbordos_empleados`
--
ALTER TABLE `transbordos_empleados`
  ADD PRIMARY KEY (`idTransbordo`);

--
-- Indices de la tabla `vehiculos`
--
ALTER TABLE `vehiculos`
  ADD PRIMARY KEY (`matricula`),
  ADD KEY `titular_id` (`idTitular`);

--
-- Indices de la tabla `viviendas`
--
ALTER TABLE `viviendas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `direccion` (`direccion`),
  ADD KEY `titular` (`titular`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `asistenteVoz`
--
ALTER TABLE `asistenteVoz`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `ciudadanos`
--
ALTER TABLE `ciudadanos`
  MODIFY `dni` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `correos`
--
ALTER TABLE `correos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `megaMilky_productos`
--
ALTER TABLE `megaMilky_productos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `megaMilky_ventas`
--
ALTER TABLE `megaMilky_ventas`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `paulsPizzeria_inventario`
--
ALTER TABLE `paulsPizzeria_inventario`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `rinconDelTurro_reservas`
--
ALTER TABLE `rinconDelTurro_reservas`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `transbordos`
--
ALTER TABLE `transbordos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `viviendas`
--
ALTER TABLE `viviendas`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `alojadoEn`
--
ALTER TABLE `alojadoEn`
  ADD CONSTRAINT `alojadoEn_ibfk_1` FOREIGN KEY (`vivienda`) REFERENCES `viviendas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `alojadoEn_ibfk_2` FOREIGN KEY (`ciudadano`) REFERENCES `ciudadanos` (`dni`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `vehiculos`
--
ALTER TABLE `vehiculos`
  ADD CONSTRAINT `vehiculos_ibfk_1` FOREIGN KEY (`idTitular`) REFERENCES `ciudadanos` (`dni`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Filtros para la tabla `viviendas`
--
ALTER TABLE `viviendas`
  ADD CONSTRAINT `viviendas_ibfk_1` FOREIGN KEY (`titular`) REFERENCES `ciudadanos` (`dni`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;