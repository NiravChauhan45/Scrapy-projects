/*
SQLyog Community v13.2.1 (64 bit)
MySQL - 8.1.0 : Database - nykaa_latest
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`nykaa_latest` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `nykaa_latest`;

/*Table structure for table `last_cat` */

DROP TABLE IF EXISTS `last_cat`;

CREATE TABLE `last_cat` (
  `id` int NOT NULL AUTO_INCREMENT,
  `main_cat_name` varchar(100) DEFAULT NULL,
  `cat_name` varchar(100) DEFAULT NULL,
  `sub_cat_name` varchar(100) DEFAULT NULL,
  `cat_id` varchar(10) DEFAULT NULL,
  `cat_url` text,
  `status` varchar(10) DEFAULT 'pending',
  `price_range` varchar(20) DEFAULT NULL,
  `segment_code` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `last_cat` */

insert  into `last_cat`(`id`,`main_cat_name`,`cat_name`,`sub_cat_name`,`cat_id`,`cat_url`,`status`,`price_range`,`segment_code`) values 
(1,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','1000-1999','126125'),
(2,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','1000-1999','219195'),
(3,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','1000-1999','152823'),
(4,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','1000-1999','126126'),
(5,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','1000-1999','126127'),
(6,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','1000-1999','153299'),
(7,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','1000-1999','214440'),
(8,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','500-999','126125'),
(9,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','500-999','219195'),
(10,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','500-999','152823'),
(11,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','500-999','126126'),
(12,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','500-999','126127'),
(13,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','500-999','153299'),
(14,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','500-999','214440'),
(15,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','0-499','126125'),
(16,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','0-499','219195'),
(17,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','0-499','152823'),
(18,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','0-499','126126'),
(19,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','0-499','126127'),
(20,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','0-499','153299'),
(21,'Lingerie & Accessories','Jewellery','Earrings','11364','https://www.nykaa.com/jewellery-accessories/earrings/c/11364','Done','0-499','214440');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
