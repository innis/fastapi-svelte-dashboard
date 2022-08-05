
CREATE DATABASE `fastapi_svelte_local`;

CREATE TABLE `fastapi_svelte_local`.`gifts` (
  `code` varchar(15) NOT NULL,
  `event_id` bigint unsigned NOT NULL,
  `used` tinyint(1) NOT NULL DEFAULT '0',
  `issued_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `start_at` datetime DEFAULT NULL,
  `finish_at` datetime DEFAULT NULL,
  `use_info` text,
  `user_pid` varchar(100) DEFAULT NULL,
  `user_platform` varchar(100) DEFAULT NULL,
  `used_at` datetime DEFAULT NULL,
  UNIQUE KEY `pk` (`code`) USING BTREE,
  KEY `idx_eventid` (`event_id`) USING BTREE,
  KEY `idx_userpid` (`user_pid`) USING BTREE,
  KEY `idx_userplatform` (`user_platform`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `fastapi_svelte_local`.`events` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `desc` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `start_at` datetime DEFAULT NULL,
  `finish_at` datetime DEFAULT NULL,
  `gift_num` int(10) unsigned DEFAULT NULL,
  `gift_used_num` int(10) unsigned NOT NULL DEFAULT '0',
  `gift_issued_num` int(10) unsigned DEFAULT '0',
  `event_info` varchar(255) DEFAULT NULL,
  `category` varchar(10) DEFAULT 'event',
  PRIMARY KEY (`id`),
  KEY `idx_category` (`category`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `fastapi_svelte_local`.`users` (
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
