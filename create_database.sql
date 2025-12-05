create database twitter_clone;
use twitter_clone;

CREATE TABLE `users` (
    `id` SERIAL PRIMARY KEY,                     -- Unique identifier for each user
    `username` VARCHAR(64) NOT NULL UNIQUE,          -- Username of the user
    `password` VARCHAR(400),                     -- Password (hashed)
    `google_id` VARCHAR(255) UNIQUE,             -- Google ID for users who sign in with Google
    `email` VARCHAR(45) NOT NULL UNIQUE,         -- Email of the user
    `display_name` VARCHAR(45) NOT NULL,         -- Display name of the user
    `profile_picture_url` VARCHAR(255),          -- URL for the profile picture
    `banner_image_url` VARCHAR(255),             -- URL for the banner image
    `verified` BOOLEAN DEFAULT FALSE,            -- Whether the user is verified
    `bio` VARCHAR(180),                          -- Short bio of the user
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when the user was created
    `pinned_post_id` INTEGER                     -- ID of the pinned post
);

INSERT INTO `users` (`username`, `password`, `google_id`, `email`, `display_name`, `profile_picture_url`, `banner_image_url`, `verified`, `bio`, `pinned_post_id`) 
VALUES
('john_doe', 'hashed_password_1', 'google_id_1', 'john@example.com', 'John Doe', 'https://example.com/profile1.jpg', 'https://example.com/banner1.jpg', FALSE, 'This is John\'s bio.', NULL),
('jane_doe', 'hashed_password_2', 'google_id_2', 'jane@example.com', 'Jane Doe', 'https://example.com/profile2.jpg', 'https://example.com/banner2.jpg', TRUE, 'This is Jane\'s bio.', NULL),
('mike_ross', 'hashed_password_3', 'google_id_3', 'mike@example.com', 'Mike Ross', 'https://example.com/profile3.jpg', 'https://example.com/banner3.jpg', FALSE, 'This is Mike\'s bio.', NULL);



create table `bookmarks`(
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `bookmarked_by` INT NOT NULL,
    `bookmarked_post` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

INSERT INTO `bookmarks` (`bookmarked_by`, `bookmarked_post`) 
VALUES
(1, 2),
(2, 3),
(3, 1);




create table `feed_entry`(
	`id` int auto_increment primary key,
    `user_id` int not null,
    `post_id` int not null,
    `score` double,
    `position` int
);
INSERT INTO `feed_entry` (`user_id`, `post_id`, `score`, `position`)
VALUES
(1, 1, 10.0, 1),
(2, 2, 8.5, 2),
(3, 3, 9.0, 3);



create table `feedback`(
	`id` int auto_increment primary key,
    `user_id` int not null,
    `text` varchar(500) not null,
    `type` varchar(100) not null
    
);

INSERT INTO `feedback` (`user_id`, `text`, `type`)
VALUES
(1, 'Great app! Keep it up.', 'positive'),
(2, 'Could use more features.', 'neutral'),
(3, 'I found a bug on the homepage.', 'negative');


create table `follow`(
	`id` int auto_increment primary key,
    `followed_id` int not null,
    `follower_id` int not null
);

INSERT INTO `follow` (`followed_id`, `follower_id`)
VALUES
(1, 2),
(1, 3),
(2, 3),
(3, 1);


create table `like`(
	`id` int auto_increment primary key,
    `liker_id` int not null,
    `post_id` int not null,
    `created_at` timestamp default current_timestamp not null
);

INSERT INTO `like` (`liker_id`, `post_id`, `created_at`)
VALUES
(1, 1, NOW()),
(2, 2, NOW()),
(3, 3, NOW());



create table `notifications`(
	`id` int auto_increment primary key,
    `receiver_id` int not null,
    `sender_id` int not null,
    `type` varchar(100) not null,
    `reference_id` int not null,
    `text` varchar(500) not null, 
    `seen` boolean default false,
    `created_at` timestamp default current_timestamp not null
);

INSERT INTO `notifications` (`receiver_id`, `sender_id`, `type`, `reference_id`, `text`, `seen`)
VALUES
(1, 2, 'like', 1, 'Jane liked your post.', FALSE),
(2, 1, 'follow', 1, 'John started following you.', TRUE),
(3, 2, 'retweet', 2, 'Mike retweeted your post.', FALSE);



create table `posts`(
	`id` int auto_increment primary key,
    `user_id` int not null,
    `parent_id` int not null,
    `text` varchar(500) not null,
    `created_at` timestamp default current_timestamp not null
);


INSERT INTO `posts` (`user_id`, `parent_id`, `text`)
VALUES
(1, 0, 'This is John\'s first post.'),
(2, 0, 'This is Jane\'s first post.'),
(3, 0, 'This is Mike\'s first post.');


create table `post_media`(
	`id` int auto_increment primary key,
    `post_id` int not null,
    `file_name` varchar(255) not null,
    `mime_type` varchar(100) not null,
    `url` varchar(512) not null,
    `created_at` timestamp default current_timestamp not null
);

INSERT INTO `post_media` (`post_id`, `file_name`, `mime_type`, `url`)
VALUES
(1, 'image1.jpg', 'image/jpeg', 'https://example.com/media/image1.jpg'),
(2, 'image2.jpg', 'image/jpeg', 'https://example.com/media/image2.jpg'),
(3, 'image3.jpg', 'image/jpeg', 'https://example.com/media/image3.jpg');


create table `retweets`(
	`id` int auto_increment primary key,
    `reference_id` int not null,
    `retweeter_id` int not null,
    `type` varchar(100) not null,
    `created_at` timestamp default current_timestamp not null
);

INSERT INTO `retweets` (`reference_id`, `retweeter_id`, `type`)
VALUES
(1, 2, 'retweet'),
(2, 3, 'quote'),
(3, 1, 'retweet');


create table `polls`(
	`id` int auto_increment primary key,
    `post_id` int,
    `created_at` timestamp default current_timestamp,
    `expires_at` timestamp null
);

INSERT INTO `polls` (`post_id`, `expires_at`)
VALUES
(1, '2025-12-10 00:00:00'),
(2, '2025-12-11 00:00:00'),
(3, '2025-12-12 00:00:00');


create table `poll_choices`(
	`id` int auto_increment primary key,
    `choice` varchar(100),
    `vote_count` int,
    `poll_id` int
);

INSERT INTO `poll_choices` (`choice`, `vote_count`, `poll_id`)
VALUES
('Choice A', 10, 1),
('Choice B', 5, 1),
('Choice A', 3, 2),
('Choice B', 8, 2),
('Choice A', 7, 3),
('Choice B', 4, 3);


create table `poll_votes`(
	`id` int auto_increment primary key,
    `poll_id` int,
    `poll_choice_id` int,
    `user_id` int,
    `created_at` timestamp default current_timestamp not null
);

INSERT INTO `poll_votes` (`poll_id`, `poll_choice_id`, `user_id`)
VALUES
(1, 1, 1),
(1, 2, 2),
(2, 1, 3),
(2, 2, 1),
(3, 1, 2),
(3, 2, 3);


create table `trends`(
	`id` int auto_increment primary key,
    `name` varchar(100),
    `url` varchar(512),
    `tweet_volume` int,
    `recorded_at` timestamp default current_timestamp
    );
    
    
    INSERT INTO `trends` (`name`, `url`, `tweet_volume`)
VALUES
('Trend1', 'https://example.com/trend1', 1500),
('Trend2', 'https://example.com/trend2', 1200),
('Trend3', 'https://example.com/trend3', 800);
