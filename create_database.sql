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


create table `bookmarks`(
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `bookmarked_by` INT NOT NULL,
    `bookmarked_post` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

create table `feed_entry`(
	`id` int auto_increment primary key,
    `user_id` int not null,
    `post_id` int not null,
    `score` double,
    `position` int
);

create table `feedback`(
	`id` int auto_increment primary key,
    `user_id` int not null,
    `text` varchar(500) not null,
    `type` varchar(100) not null
    
);


create table `follow`(
	`id` int auto_increment primary key,
    `followed_id` int not null,
    `follower_id` int not null
);

create table `like`(
	`id` int auto_increment primary key,
    `liker_id` int not null,
    `post_id` int not null,
    `created_at` timestamp default current_timestamp not null
);

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

create table `posts`(
	`id` int auto_increment primary key,
    `user_id` int not null,
    `parent_id` int not null,
    `text` varchar(500) not null,
    `created_at` timestamp default current_timestamp not null
);

create table `post_media`(
	`id` int auto_increment primary key,
    `post_id` int not null,
    `file_name` varchar(255) not null,
    `mime_type` varchar(100) not null,
    `url` varchar(512) not null,
    `created_at` timestamp default current_timestamp not null
);

create table `retweets`(
	`id` int auto_increment primary key,
    `reference_id` int not null,
    `retweeter_id` int not null,
    `type` varchar(100) not null,
    `created_at` timestamp default current_timestamp not null
);

create table `polls`(
	`id` int auto_increment primary key,
    `post_id` int,
    `created_at` timestamp default current_timestamp,
    `expires_at` timestamp null
);

create table `poll_choices`(
	`id` int auto_increment primary key,
    `choice` varchar(100),
    `vote_count` int,
    `poll_id` int
);

create table `poll_votes`(
	`id` int auto_increment primary key,
    `poll_id` int,
    `poll_choice_id` int,
    `user_id` int,
    `created_at` timestamp default current_timestamp not null
);

create table `trends`(
	`id` int auto_increment primary key,
    `name` varchar(100),
    `url` varchar(512),
    `tweet_volume` int,
    `recorded_at` timestamp default current_timestamp
    );