-- DROP DATABASE IF EXISTS finance; 
-- CREATE DATABASE finance;

USE finance;

CREATE TABLE users(
	id VARCHAR(50) NOT NULL PRIMARY KEY,
	first_name VARCHAR(50) DEFAULT NULL,
    last_name VARCHAR(50) DEFAULT NULL,
    username VARCHAR(50) DEFAULT NULL,
    UNIQUE KEY (username)
);

CREATE TABLE budget (
	code_name varchar(50) DEFAULT 'general',
    daily_limit integer DEFAULT 0,
    month_limit integer DEFAULT 0,
    user_id varchar(50) NOT NULL,
    PRIMARY KEY (code_name, user_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE category(
	code_name varchar(100),
    category_name varchar(50),
    aliases_ text,
	user_id varchar(50) NOT NULL,
    PRIMARY KEY(code_name, user_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE expenses (
	expense_id integer NOT NULL AUTO_INCREMENT,
    amount integer,
    date_time datetime, 
    category varchar(100),
	user_id varchar(50) NOT NULL,
    PRIMARY KEY(expense_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category) REFERENCES category(code_name)
);

CREATE TABLE incomes (
	income_id integer NOT NULL AUTO_INCREMENT,
    amount integer,
    date_time datetime,
    category varchar(100),
	user_id varchar(50) NOT NULL,
    PRIMARY KEY(income_id), 
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category) REFERENCES category(code_name)
);


INSERT INTO budget (code_name, daily_limit, month_limit) VALUES ('general', 0, 0)
