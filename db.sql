/*
Navicat MySQL Data Transfer

Source Server         : LOCALHOST
Source Server Version : 50562
Source Host           : 127.0.0.1:3306
Source Database       : eshop

Target Server Type    : MYSQL
Target Server Version : 50562
File Encoding         : 65001

Date: 2019-02-28 17:04:09
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES ('1', 'Can add log entry', '1', 'add_logentry');
INSERT INTO `auth_permission` VALUES ('2', 'Can change log entry', '1', 'change_logentry');
INSERT INTO `auth_permission` VALUES ('3', 'Can delete log entry', '1', 'delete_logentry');
INSERT INTO `auth_permission` VALUES ('4', 'Can add permission', '2', 'add_permission');
INSERT INTO `auth_permission` VALUES ('5', 'Can change permission', '2', 'change_permission');
INSERT INTO `auth_permission` VALUES ('6', 'Can delete permission', '2', 'delete_permission');
INSERT INTO `auth_permission` VALUES ('7', 'Can add group', '3', 'add_group');
INSERT INTO `auth_permission` VALUES ('8', 'Can change group', '3', 'change_group');
INSERT INTO `auth_permission` VALUES ('9', 'Can delete group', '3', 'delete_group');
INSERT INTO `auth_permission` VALUES ('10', 'Can add user', '4', 'add_user');
INSERT INTO `auth_permission` VALUES ('11', 'Can change user', '4', 'change_user');
INSERT INTO `auth_permission` VALUES ('12', 'Can delete user', '4', 'delete_user');
INSERT INTO `auth_permission` VALUES ('13', 'Can add content type', '5', 'add_contenttype');
INSERT INTO `auth_permission` VALUES ('14', 'Can change content type', '5', 'change_contenttype');
INSERT INTO `auth_permission` VALUES ('15', 'Can delete content type', '5', 'delete_contenttype');
INSERT INTO `auth_permission` VALUES ('16', 'Can add session', '6', 'add_session');
INSERT INTO `auth_permission` VALUES ('17', 'Can change session', '6', 'change_session');
INSERT INTO `auth_permission` VALUES ('18', 'Can delete session', '6', 'delete_session');
INSERT INTO `auth_permission` VALUES ('19', 'Can add category', '7', 'add_category');
INSERT INTO `auth_permission` VALUES ('20', 'Can change category', '7', 'change_category');
INSERT INTO `auth_permission` VALUES ('21', 'Can delete category', '7', 'delete_category');
INSERT INTO `auth_permission` VALUES ('22', 'Can add product', '8', 'add_product');
INSERT INTO `auth_permission` VALUES ('23', 'Can change product', '8', 'change_product');
INSERT INTO `auth_permission` VALUES ('24', 'Can delete product', '8', 'delete_product');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO `auth_user` VALUES ('1', 'pbkdf2_sha256$100000$H9m454KDVFxj$ANcsn9faSjZ6KI3tmb9tSXxFFNzN7dYapbkJ+gb3vlg=', '2019-02-28 13:41:09', '1', 'admin', '', '', 'admin@eshop.com', '1', '1', '2019-02-26 10:55:41');

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------
INSERT INTO `django_admin_log` VALUES ('1', '2019-02-26 10:56:01', '1', 'Honey products', '1', '[{\"added\": {}}]', '7', '1');
INSERT INTO `django_admin_log` VALUES ('2', '2019-02-26 10:56:36', '1', 'Honey', '1', '[{\"added\": {}}]', '8', '1');
INSERT INTO `django_admin_log` VALUES ('3', '2019-02-26 10:58:59', '1', 'Honey', '2', '[{\"changed\": {\"fields\": [\"image\"]}}]', '8', '1');
INSERT INTO `django_admin_log` VALUES ('4', '2019-02-26 11:07:49', '1', 'Honey', '2', '[{\"changed\": {\"fields\": [\"image\"]}}]', '8', '1');
INSERT INTO `django_admin_log` VALUES ('5', '2019-02-26 11:10:11', '1', 'Honey', '2', '[{\"changed\": {\"fields\": [\"image\"]}}]', '8', '1');
INSERT INTO `django_admin_log` VALUES ('6', '2019-02-26 21:18:35', '1', 'Honey', '2', '[{\"changed\": {\"fields\": [\"image\"]}}]', '8', '1');
INSERT INTO `django_admin_log` VALUES ('7', '2019-02-28 13:41:34', '1', 'Honey', '2', '[{\"changed\": {\"fields\": [\"image\"]}}]', '8', '1');
INSERT INTO `django_admin_log` VALUES ('8', '2019-02-28 13:45:44', '2', 'Fruits and vegetables', '1', '[{\"added\": {}}]', '7', '1');
INSERT INTO `django_admin_log` VALUES ('9', '2019-02-28 13:45:54', '3', 'Fruits', '1', '[{\"added\": {}}]', '7', '1');
INSERT INTO `django_admin_log` VALUES ('10', '2019-02-28 13:46:02', '4', 'Vegatables', '1', '[{\"added\": {}}]', '7', '1');
INSERT INTO `django_admin_log` VALUES ('11', '2019-02-28 13:49:42', '5', 'Berries', '1', '[{\"added\": {}}]', '7', '1');
INSERT INTO `django_admin_log` VALUES ('12', '2019-02-28 13:50:31', '6', 'Other fruits', '1', '[{\"added\": {}}]', '7', '1');
INSERT INTO `django_admin_log` VALUES ('13', '2019-02-28 13:54:04', '2', 'Cucumber', '1', '[{\"added\": {}}]', '8', '1');
INSERT INTO `django_admin_log` VALUES ('14', '2019-02-28 13:55:00', '3', 'Potatoes', '1', '[{\"added\": {}}]', '8', '1');
INSERT INTO `django_admin_log` VALUES ('15', '2019-02-28 13:56:10', '4', 'Blackberries', '1', '[{\"added\": {}}]', '8', '1');
INSERT INTO `django_admin_log` VALUES ('16', '2019-02-28 13:57:48', '5', 'Blueberries', '1', '[{\"added\": {}}]', '8', '1');
INSERT INTO `django_admin_log` VALUES ('17', '2019-02-28 13:59:35', '6', 'Banana', '1', '[{\"added\": {}}]', '8', '1');
INSERT INTO `django_admin_log` VALUES ('18', '2019-02-28 14:00:01', '7', 'Apples', '1', '[{\"added\": {}}]', '8', '1');

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES ('1', 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES ('3', 'auth', 'group');
INSERT INTO `django_content_type` VALUES ('2', 'auth', 'permission');
INSERT INTO `django_content_type` VALUES ('4', 'auth', 'user');
INSERT INTO `django_content_type` VALUES ('5', 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES ('7', 'ebag', 'category');
INSERT INTO `django_content_type` VALUES ('8', 'ebag', 'product');
INSERT INTO `django_content_type` VALUES ('6', 'sessions', 'session');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES ('1', 'contenttypes', '0001_initial', '2019-02-26 10:54:40');
INSERT INTO `django_migrations` VALUES ('2', 'auth', '0001_initial', '2019-02-26 10:54:40');
INSERT INTO `django_migrations` VALUES ('3', 'admin', '0001_initial', '2019-02-26 10:54:40');
INSERT INTO `django_migrations` VALUES ('4', 'admin', '0002_logentry_remove_auto_add', '2019-02-26 10:54:40');
INSERT INTO `django_migrations` VALUES ('5', 'contenttypes', '0002_remove_content_type_name', '2019-02-26 10:54:41');
INSERT INTO `django_migrations` VALUES ('6', 'auth', '0002_alter_permission_name_max_length', '2019-02-26 10:54:41');
INSERT INTO `django_migrations` VALUES ('7', 'auth', '0003_alter_user_email_max_length', '2019-02-26 10:54:41');
INSERT INTO `django_migrations` VALUES ('8', 'auth', '0004_alter_user_username_opts', '2019-02-26 10:54:41');
INSERT INTO `django_migrations` VALUES ('9', 'auth', '0005_alter_user_last_login_null', '2019-02-26 10:54:41');
INSERT INTO `django_migrations` VALUES ('10', 'auth', '0006_require_contenttypes_0002', '2019-02-26 10:54:41');
INSERT INTO `django_migrations` VALUES ('11', 'auth', '0007_alter_validators_add_error_messages', '2019-02-26 10:54:41');
INSERT INTO `django_migrations` VALUES ('12', 'auth', '0008_alter_user_username_max_length', '2019-02-26 10:54:41');
INSERT INTO `django_migrations` VALUES ('13', 'auth', '0009_alter_user_last_name_max_length', '2019-02-26 10:54:41');
INSERT INTO `django_migrations` VALUES ('14', 'ebag', '0001_initial', '2019-02-26 10:54:41');
INSERT INTO `django_migrations` VALUES ('15', 'sessions', '0001_initial', '2019-02-26 10:54:41');
INSERT INTO `django_migrations` VALUES ('16', 'ebag', '0002_auto_20190226_1106', '2019-02-26 11:07:04');
INSERT INTO `django_migrations` VALUES ('17', 'ebag', '0003_remove_product_slug', '2019-02-26 14:11:47');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('2inm8jx8ivr9wdpny1bwy4hsqykqv9lg', 'ZjljODY5MTVlZTgxOGUwZjA3YjFmMGJmMzBiZTk2NThlMjM2NDViYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkNGJmZTNjNGE5MjQ2YmM1ZjY4ZjU1NGYyNjE4MjM1MTUwY2JiNGM4In0=', '2019-03-14 14:43:49');

-- ----------------------------
-- Table structure for ebag_category
-- ----------------------------
DROP TABLE IF EXISTS `ebag_category`;
CREATE TABLE `ebag_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `last_update` datetime NOT NULL,
  `slug` varchar(50) NOT NULL,
  `lft` int(10) unsigned NOT NULL,
  `rght` int(10) unsigned NOT NULL,
  `tree_id` int(10) unsigned NOT NULL,
  `level` int(10) unsigned NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ebag_category_parent_id_slug_ee29faee_uniq` (`parent_id`,`slug`),
  KEY `ebag_category_slug_1850c00a` (`slug`),
  KEY `ebag_category_lft_838672bd` (`lft`),
  KEY `ebag_category_rght_85214687` (`rght`),
  KEY `ebag_category_tree_id_0f0ca738` (`tree_id`),
  KEY `ebag_category_level_e603fa8c` (`level`),
  KEY `ebag_category_parent_id_4912cbe5` (`parent_id`),
  CONSTRAINT `ebag_category_parent_id_4912cbe5_fk_ebag_category_id` FOREIGN KEY (`parent_id`) REFERENCES `ebag_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ebag_category
-- ----------------------------
INSERT INTO `ebag_category` VALUES ('1', 'Honey products', '2019-02-26 10:56:01', 'category/{%pk%}/honey-products', '1', '2', '1', '0', null);
INSERT INTO `ebag_category` VALUES ('2', 'Fruits and vegetables', '2019-02-28 13:45:44', 'category/{%pk%}/fruits-and-vegetables', '1', '10', '2', '0', null);
INSERT INTO `ebag_category` VALUES ('3', 'Fruits', '2019-02-28 13:45:54', 'category/{%pk%}/fruits', '4', '9', '2', '1', '2');
INSERT INTO `ebag_category` VALUES ('4', 'Vegatables', '2019-02-28 13:51:15', 'category/{%pk%}/vegatables', '2', '3', '2', '1', '2');
INSERT INTO `ebag_category` VALUES ('5', 'Berries', '2019-02-28 13:49:42', 'category/{%pk%}/berries', '5', '6', '2', '2', '3');
INSERT INTO `ebag_category` VALUES ('6', 'Other fruits', '2019-02-28 13:50:53', 'category/{%pk%}/other-fruits', '7', '8', '2', '2', '3');

-- ----------------------------
-- Table structure for ebag_product
-- ----------------------------
DROP TABLE IF EXISTS `ebag_product`;
CREATE TABLE `ebag_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `image` varchar(100) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ebag_product_category_id_ba3bab21` (`category_id`),
  CONSTRAINT `ebag_product_category_id_ba3bab21_fk_ebag_category_id` FOREIGN KEY (`category_id`) REFERENCES `ebag_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ebag_product
-- ----------------------------
INSERT INTO `ebag_product` VALUES ('1', 'Honey', 'Honey', '10.00', '58f2c584-de55-43d0-bbe8-06602539549b.jpg', '1');
INSERT INTO `ebag_product` VALUES ('2', 'Cucumber', 'Great green fresh cucumbers, ideal for a salad!', '2.55', 'd3669e60-07bf-4557-9eba-ed31d618df00.jpg', '4');
INSERT INTO `ebag_product` VALUES ('3', 'Potatoes', 'Potatoes are rich in Potassium. A great food for the winter period!', '6.99', 'c62ef86e-b687-4a53-828d-7d6842ed43f9.jpg', '4');
INSERT INTO `ebag_product` VALUES ('4', 'Blackberries', 'Super tasty blackberries!', '10.00', '09fd7d99-0ec4-4d7c-84ef-722f8889fdd4.jpg', '5');
INSERT INTO `ebag_product` VALUES ('5', 'Blueberries', 'Organic blueberries.', '12.49', 'bc3877e0-4cf4-4d18-b8af-16383dda3e47.jpg', '5');
INSERT INTO `ebag_product` VALUES ('6', 'Banana', 'Bananas. Origin: India.', '2.00', '0d9517a2-393a-4a00-ab26-1f17e2c89aca.jpg', '6');
INSERT INTO `ebag_product` VALUES ('7', 'Apples', 'Super tasty apples!', '5.00', '76baf4ba-91a5-481b-8da9-54ee5dd63201.jpg', '6');
SET FOREIGN_KEY_CHECKS=1;
