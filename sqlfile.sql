/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.4.21-MariaDB : Database - bitcoin
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`bitcoin` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `bitcoin`;

/*Table structure for table `bitcoinreg` */

DROP TABLE IF EXISTS `bitcoinreg`;

CREATE TABLE `bitcoinreg` (
  `id` int(200) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `bitcoins` varchar(100) DEFAULT '0',
  `password` varchar(100) DEFAULT NULL,
  `ContactNumber` varchar(100) DEFAULT NULL,
  `PANCARD` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

/*Data for the table `bitcoinreg` */

insert  into `bitcoinreg`(`id`,`name`,`email`,`bitcoins`,`password`,`ContactNumber`,`PANCARD`) values (1,'mouli','mouli@gmail.com','290','1234','7894561231','FJNPM2887D');

/*Table structure for table `bitcointransaction` */

DROP TABLE IF EXISTS `bitcointransaction`;

CREATE TABLE `bitcointransaction` (
  `Slno` int(200) NOT NULL AUTO_INCREMENT,
  `Username` varchar(200) DEFAULT NULL,
  `Email` varchar(200) DEFAULT NULL,
  `Bitcoins` varchar(200) DEFAULT NULL,
  `Contact` varchar(200) DEFAULT NULL,
  `PANCARD` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`Slno`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

/*Data for the table `bitcointransaction` */

insert  into `bitcointransaction`(`Slno`,`Username`,`Email`,`Bitcoins`,`Contact`,`PANCARD`) values (1,'mouli@gmail.com','mouli@gmail.com','0','7894561231','FJNPM2887D'),(2,'mouli','mouli@gmail.com','-35','7894561231','FJNPM2887D'),(3,'mouli','mouli@gmail.com','-59','7894561231','FJNPM2887D'),(4,'mouli','mouli@gmail.com','-158','7894561231','FJNPM2887D'),(5,'mouli','mouli@gmail.com','-176','7894561231','FJNPM2887D'),(6,'mouli','mouli@gmail.com','431','7894561231','FJNPM2887D'),(7,'mouli','mouli@gmail.com','443','7894561231','FJNPM2887D'),(8,'mouli','mouli@gmail.com','304','7894561231','FJNPM2887D');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
