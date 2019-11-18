-- MySQL dump 10.13  Distrib 5.7.27, for Linux (x86_64)
--
-- Host: localhost    Database: test
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
INSERT INTO `mobilenet_search` VALUES (0,0,0,0,0.906,'/home/'),(0,0.75,0,0.75,0.90404,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-0-0.25-0-0.25/models'),(1,0.9375,1,0.9375,0.84466,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-1-0.0625-1-0.0625/models'),(3,0.958333,3,0.958333,0.76288,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-3-0.041666668-3-0.041666668/models'),(6,0.8125,6,0.8125,0.85676,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-6-0.1875-6-0.1875/models'),(10,0.625,10,0.625,0.88794,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-10-0.375-10-0.375/models'),(13,0.760417,13,0.760417,0.87216,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-13-0.23958333-13-0.23958333/models'),(16,0.76875,16,0.76875,0.84878,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-16-0.23125-16-0.23125/models'),(1,0.5625,1,0.5625,0.90272,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-1-0.4375-1-0.4375/models'),(3,0.041667,3,0.041667,0.90542,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-3-0.9583333-3-0.9583333/models'),(0,0.84375,0,0.84375,0.8966,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-0-0.15625-0-0.15625/models'),(3,0.916667,3,0.916667,0.82464,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-3-0.083333336-3-0.083333336/models'),(6,0.78125,6,0.78125,0.86878,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-6-0.21875-6-0.21875/models'),(10,0.578125,10,0.578125,0.88978,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-10-0.421875-10-0.421875/models'),(13,0.71875,13,0.71875,0.87704,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-13-0.28125-13-0.28125/models'),(16,0.7,16,0.7,0.86022,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-16-0.3-16-0.3/models'),(1,0.75,1,0.75,0.89506,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-1-0.25-1-0.25/models'),(3,0.541667,3,0.541667,0.89802,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-3-0.45833334-3-0.45833334/models'),(6,0.6875,6,0.6875,0.88034,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-6-0.3125-6-0.3125/models'),(10,0.359375,10,0.359375,0.89812,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-10-0.640625-10-0.640625/models'),(3,0.5,10,0.359375,0.89128,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-3-0.5-10-0.640625/models'),(13,0.479167,13,0.479167,0.89398,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-13-0.5208333-13-0.5208333/models'),(16,0.35625,16,0.35625,0.89298,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-16-0.64375-16-0.64375/models'),(0,0.9375,0,0.9375,0.87264,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-0-0.0625-0-0.0625/models'),(10,0.53125,10,0.53125,0.89372,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-10-0.46875-10-0.46875/models'),(0,0.90625,10,0.53125,0.87342,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-0-0.09375-10-0.46875/models'),(10,0.546875,10,0.546875,0.89056,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-10-0.453125-10-0.453125/models'),(0,0.90625,10,0.546875,0.87402,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-0-0.09375-10-0.453125/models'),(13,0.666667,13,0.666667,0.88244,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-13-0.33333334-13-0.33333334/models'),(0,0.90625,13,0.666667,0.86474,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-0-0.09375-13-0.33333334/models'),(10,0.609375,10,0.609375,0.8882,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-10-0.390625-10-0.390625/models'),(1,0.875,10,0.609375,0.8616,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-1-0.125-10-0.390625/models'),(10,0.6875,10,0.6875,0.88042,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-10-0.3125-10-0.3125/models'),(3,0.875,10,0.6875,0.82084,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-3-0.125-10-0.3125/models'),(10,0.8125,10,0.8125,0.86084,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-10-0.1875-10-0.1875/models'),(6,0.90625,6,0.90625,0.73534,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-6-0.09375-6-0.09375/models'),(6,0.9375,6,0.9375,0.74012,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-6-0.0625-6-0.0625/models'),(3,0.5,3,0.5,0.89954,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-3-0.5-3-0.5/models'),(3,0.375,3,0.375,0.90052,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-3-0.625-3-0.625/models'),(6,0.15625,6,0.15625,0.90246,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-6-0.84375-6-0.84375/models'),(10,0.5,10,0.5,0.89406,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-10-0.5-10-0.5/models'),(3,0.875,3,0.875,0.85492,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-3-0.125-3-0.125/models'),(6,0.75,6,0.75,0.86626,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-6-0.25-6-0.25/models'),(10,0.515625,10,0.515625,0.8925,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-10-0.484375-10-0.484375/models'),(0,0.90625,10,0.515625,0.87584,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-0-0.09375-10-0.484375/models'),(13,0.635417,13,0.635417,0.88468,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-13-0.36458334-13-0.36458334/models'),(0,0.90625,13,0.635417,0.86768,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-0-0.09375-13-0.36458334/models'),(16,0.575,16,0.575,0.8791,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-16-0.425-16-0.425/models'),(0,0.90625,16,0.575,0.85824,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-0-0.09375-16-0.425/models'),(10,0.71875,10,0.71875,0.87786,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-10-0.28125-10-0.28125/models'),(10,0.703125,10,0.703125,0.87968,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-10-0.296875-10-0.296875/models'),(10,0.75,10,0.75,0.87634,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-10-0.25-10-0.25/models'),(6,0.125,6,0.125,0.90302,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-6-0.875-6-0.875/models'),(10,0.765625,10,0.765625,0.87364,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-10-0.234375-10-0.234375/models'),(0,0.65625,0,0.65625,0.90604,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-0-0.34375-0-0.34375/models'),(6,0.5,6,0.5,0.89278,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-6-0.5-6-0.5/models'),(6,0.375,6,0.375,0.89608,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-6-0.625-6-0.625/models'),(10,0.375,10,0.375,0.89854,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-10-0.625-10-0.625/models'),(6,0.34375,10,0.375,0.89224,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-6-0.65625-10-0.625/models'),(10,0.40625,10,0.40625,0.89784,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-10-0.59375-10-0.59375/models'),(6,0.3125,10,0.40625,0.88954,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-6-0.6875-10-0.59375/models'),(10,0.4375,10,0.4375,0.89602,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-10-0.5625-10-0.5625/models'),(6,0.28125,10,0.4375,0.88966,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-6-0.71875-10-0.5625/models'),(0,0.96875,0,0.96875,0.837,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-0-0.03125-0-0.03125/models'),(0,0.875,0,0.875,0.89536,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-0-0.125-0-0.125/models'),(0,0.9375,10,0.640625,0.86212,'/media/han/新加卷/mobilenet-OnEEC/mobilenet_2-0-0.0625-10-0.359375/models');
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

-- Dump completed on 2019-11-16 21:50:10
