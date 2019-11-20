-- MySQL dump 10.13  Distrib 5.7.27, for Linux (x86_64)
--
-- Host: localhost    Database: cnnpc
-- ------------------------------------------------------
-- Server version	5.7.27-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `resnet_search`
--

DROP TABLE IF EXISTS `resnet_search`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `resnet_search` (
  `com_1` tinyint(4) DEFAULT NULL,
  `rate_1` double DEFAULT NULL,
  `com_2` tinyint(4) DEFAULT NULL,
  `rate_2` double DEFAULT NULL,
  `accuracy` double DEFAULT NULL,
  `res_dir` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resnet_search`
--

LOCK TABLES `resnet_search` WRITE;
/*!40000 ALTER TABLE `resnet_search` DISABLE KEYS */;
INSERT INTO `resnet_search` VALUES (0,0,0,0,89.418,NULL);
/*!40000 ALTER TABLE `resnet_search` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mobilenet_search`
--

DROP TABLE IF EXISTS `mobilenet_search`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mobilenet_search` (
  `com_1` tinyint(4) DEFAULT NULL,
  `rate_1` double DEFAULT NULL,
  `com_2` tinyint(4) DEFAULT NULL,
  `rate_2` double DEFAULT NULL,
  `accuracy` double DEFAULT NULL,
  `res_dir` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mobilenet_search`
--

LOCK TABLES `mobilenet_search` WRITE;
/*!40000 ALTER TABLE `mobilenet_search` DISABLE KEYS */;
INSERT INTO `mobilenet_search` VALUES (0,0,0,0,0.906,NULL);
/*!40000 ALTER TABLE `mobilenet_search` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-20 22:18:50
