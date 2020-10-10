CREATE TABLE `video_13125005820` (
`id` bigint(32) NOT NULL AUTO_INCREMENT,
`title` varchar(128) NULL,
`des` varchar(255) NULL,
`local_path` varchar(255) NULL,
`play_count` int(255)  DEFAULT  0,
`recommend_count` int(255)  DEFAULT  0,
`publish_time` varchar(64) NULL,
`release_time` varchar(64) NULL,
`publish_status` int(255) DEFAULT  0,
PRIMARY KEY (`id`) 
);
