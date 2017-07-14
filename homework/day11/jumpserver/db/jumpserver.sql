/*
Navicat MySQL Data Transfer

Source Server         : myhost
Source Server Version : 50173
Source Host           : 119.29.237.119:5008
Source Database       : jumpserver

Target Server Type    : MYSQL
Target Server Version : 50173
File Encoding         : 65001

Date: 2017-07-14 15:52:13
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `department`
-- ----------------------------
DROP TABLE IF EXISTS `department`;
CREATE TABLE `department` (
  `pid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'department-ID',
  `title` varchar(32) NOT NULL COMMENT '部门名称',
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of department
-- ----------------------------
INSERT INTO `department` VALUES ('1', 'IT管理');
INSERT INTO `department` VALUES ('2', '销售');
INSERT INTO `department` VALUES ('3', '市场');
INSERT INTO `department` VALUES ('4', '行政');
INSERT INTO `department` VALUES ('5', '财务');
INSERT INTO `department` VALUES ('6', '研发部');
INSERT INTO `department` VALUES ('7', '系统部');

-- ----------------------------
-- Table structure for `host`
-- ----------------------------
DROP TABLE IF EXISTS `host`;
CREATE TABLE `host` (
  `hid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'HOST-ID',
  `hostname` varchar(32) NOT NULL DEFAULT 'localhost' COMMENT '主机名',
  `private_ip` char(15) NOT NULL DEFAULT '' COMMENT '内网IP',
  `public_ip` char(15) NOT NULL COMMENT '公网IP',
  `ssh_port` varchar(5) NOT NULL DEFAULT '22' COMMENT 'ssh端口',
  `username` varchar(32) NOT NULL COMMENT '用户名',
  `password` varchar(32) NOT NULL COMMENT '密码',
  `key_path` varchar(32) DEFAULT '' COMMENT 'key路径',
  `idc_id` int(10) unsigned NOT NULL COMMENT 'IDC-id',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`hid`),
  KEY `fk_idc_id` (`idc_id`),
  CONSTRAINT `fk_idc_id` FOREIGN KEY (`idc_id`) REFERENCES `idc` (`did`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of host
-- ----------------------------
INSERT INTO `host` VALUES ('1', 'h1', '192.168.1.1', '119.29.237.119', '63008', 'shuke', 'Shuke163@163.com', '/home/shuke/.ssh/authorized_keys', '2', '2017-07-10 15:28:23', '2017-07-11 15:31:40');
INSERT INTO `host` VALUES ('4', 'h4', '192.168.1.2', '119.29.237.119', '63008', 'shuke', 'Shuke163@163.com', '/home/shuke/.ssh/authorized_keys', '2', '2017-07-10 15:31:28', '2017-07-10 15:31:32');
INSERT INTO `host` VALUES ('5', 'h5', '192.168.1.3', '119.29.237.119', '63008', 'shuke', 'Shuke163@163.com', '/home/shuke/.ssh/authorized_keys', '2', '2017-07-10 16:08:10', '2017-07-10 16:08:12');
INSERT INTO `host` VALUES ('6', 'h6', '192.168.1.4', '119.29.237.119', '63008', 'shuke', 'Shuke163@163.com', '/home/shuke/.ssh/authorized_keys', '4', '2017-07-10 16:08:15', '2017-07-10 16:08:17');
INSERT INTO `host` VALUES ('7', 'web07', '192.168.1.5', '119.29.237.119', '63008', 'shuke', 'Shuke163@163.com', '/home/shuke/.ssh/authorized_keys', '4', '2017-07-10 16:08:20', '2017-07-10 16:08:23');
INSERT INTO `host` VALUES ('9', 'web09', '192.168.1.6', '119.29.237.119', '63008', 'shuke', 'Shuke163@163.com', '/home/shuke/.ssh/authorized_keys', '5', '2017-07-10 16:08:26', '2017-07-10 16:08:29');
INSERT INTO `host` VALUES ('12', 'db12', '192.168.1.7', '119.29.237.119', '63008', 'shuke', 'Shuke163@163.com', '/home/shuke/.ssh/authorized_keys', '4', '2017-07-10 16:08:33', '2017-07-10 16:08:35');
INSERT INTO `host` VALUES ('14', 'db14', '192.168.1.8', '119.29.237.119', '63008', 'shuke', 'Shuke163@163.com', '/home/shuke/.ssh/authorized_keys', '4', '2017-07-11 17:18:26', '2017-07-11 17:18:29');

-- ----------------------------
-- Table structure for `host_group`
-- ----------------------------
DROP TABLE IF EXISTS `host_group`;
CREATE TABLE `host_group` (
  `gid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'hostgroup-ID',
  `group_name` varchar(32) NOT NULL COMMENT '主机组名称',
  PRIMARY KEY (`gid`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of host_group
-- ----------------------------
INSERT INTO `host_group` VALUES ('8', 'web');
INSERT INTO `host_group` VALUES ('9', 'nginx');
INSERT INTO `host_group` VALUES ('10', 'db');
INSERT INTO `host_group` VALUES ('11', 'cache');
INSERT INTO `host_group` VALUES ('12', 'cache');

-- ----------------------------
-- Table structure for `idc`
-- ----------------------------
DROP TABLE IF EXISTS `idc`;
CREATE TABLE `idc` (
  `did` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'idc-ID',
  `name` varchar(32) NOT NULL COMMENT '机房名称',
  PRIMARY KEY (`did`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of idc
-- ----------------------------
INSERT INTO `idc` VALUES ('1', '洋桥机房');
INSERT INTO `idc` VALUES ('2', '鲁谷机房');
INSERT INTO `idc` VALUES ('3', '兆维机房');
INSERT INTO `idc` VALUES ('4', '唐山机房');
INSERT INTO `idc` VALUES ('5', 'HP机房');

-- ----------------------------
-- Table structure for `service`
-- ----------------------------
DROP TABLE IF EXISTS `service`;
CREATE TABLE `service` (
  `sid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'serivice-ID',
  `service` varchar(32) NOT NULL COMMENT '业务线',
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of service
-- ----------------------------
INSERT INTO `service` VALUES ('1', '广告');
INSERT INTO `service` VALUES ('2', '王者荣耀项目');
INSERT INTO `service` VALUES ('3', '滴滴专车项目');
INSERT INTO `service` VALUES ('4', '穿越火线项目');
INSERT INTO `service` VALUES ('5', '大数据');
INSERT INTO `service` VALUES ('6', '机器学习');
INSERT INTO `service` VALUES ('7', '全民枪战项目');
INSERT INTO `service` VALUES ('8', '阴阳师项目');

-- ----------------------------
-- Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `uid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'USER-ID',
  `username` varchar(32) NOT NULL COMMENT '用户名',
  `password` varchar(32) NOT NULL COMMENT '密码',
  `mail` varchar(32) NOT NULL COMMENT '邮箱',
  `department_id` int(10) unsigned NOT NULL COMMENT '部门ID',
  PRIMARY KEY (`uid`),
  KEY `fk_dpt_id` (`department_id`),
  CONSTRAINT `fk_dpt_id` FOREIGN KEY (`department_id`) REFERENCES `department` (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'jack', '123456', 'jack@mail.com', '7');
INSERT INTO `user` VALUES ('3', 'rain', '123456', 'rain@mail.com', '7');
INSERT INTO `user` VALUES ('6', 'shuke', '123456', 'shuke@mail.com', '1');
INSERT INTO `user` VALUES ('7', 'alex', '123456', 'alex@mail.com', '7');
INSERT INTO `user` VALUES ('8', 'eric', '123456', 'eric@mail.com', '7');
INSERT INTO `user` VALUES ('9', 'byby', '123456', 'byby@mail.com', '1');
INSERT INTO `user` VALUES ('10', '张三', '123456', 'zhangsan@mail.com', '2');
INSERT INTO `user` VALUES ('11', '李四', '123456', 'lisi@mail.com', '3');
INSERT INTO `user` VALUES ('12', 'admin', '123456', 'admin@mail.com', '7');

-- ----------------------------
-- Table structure for `user_host`
-- ----------------------------
DROP TABLE IF EXISTS `user_host`;
CREATE TABLE `user_host` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `user_id` int(10) unsigned NOT NULL COMMENT '用户ID',
  `host_id` int(10) unsigned NOT NULL COMMENT '主机ID',
  `service_id` int(10) unsigned NOT NULL COMMENT '业务线ID',
  `group_id` int(10) unsigned NOT NULL COMMENT '主机组ID',
  PRIMARY KEY (`id`),
  KEY `fk_uid` (`user_id`),
  KEY `fk_hid` (`host_id`),
  KEY `fk_sid` (`service_id`),
  KEY `fk_gid` (`group_id`),
  CONSTRAINT `fk_uid` FOREIGN KEY (`user_id`) REFERENCES `user` (`uid`),
  CONSTRAINT `fk_hid` FOREIGN KEY (`host_id`) REFERENCES `host` (`hid`),
  CONSTRAINT `fk_sid` FOREIGN KEY (`service_id`) REFERENCES `service` (`sid`),
  CONSTRAINT `fk_gid` FOREIGN KEY (`group_id`) REFERENCES `host_group` (`gid`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user_host
-- ----------------------------
INSERT INTO `user_host` VALUES ('1', '6', '9', '2', '8');
INSERT INTO `user_host` VALUES ('2', '6', '9', '2', '8');
INSERT INTO `user_host` VALUES ('3', '6', '9', '2', '8');
INSERT INTO `user_host` VALUES ('4', '6', '9', '2', '10');
INSERT INTO `user_host` VALUES ('6', '6', '7', '2', '8');
INSERT INTO `user_host` VALUES ('12', '7', '4', '2', '10');
