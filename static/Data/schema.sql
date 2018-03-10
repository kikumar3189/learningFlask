drop table if exists users;
    create table users (
    id integer primary key autoincrement,
    firstname text,
    lastname text,
    email not null UNIQUE,
    password text not null

);