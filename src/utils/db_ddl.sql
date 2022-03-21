drop table sessions;
drop table energy_history;
drop table parking_history;
drop table cars;
drop table users;
drop table places;
drop table levels;
drop table parkings;

create table parkings
(
    id          integer not null
        constraint parkings_pk
            primary key autoincrement,
    name        text    not null,
    description text,
    city        text,
    street      text,
    postal_code text,
    image_url   text
);


create table levels
(
    id           integer not null
        constraint levels_pk
            primary key autoincrement,
    name         text    not null,
    total_places int     not null,
    parking_id   integer not null
        references parkings
);

create unique index levels_id_uindex
    on levels (id);


create table places
(
    id       integer not null
        primary key autoincrement,
    status   int     not null,
    level_id integer not null
        references levels
);

create unique index places_id_uindex
    on places (id);


create table users
(
    id       integer not null
        primary key autoincrement,
    username text    not null,
    password text    not null,
    mail     text    not null,
    type     text default 'U' not null
);

create unique index users_id_uindex
    on users (id);


create table cars
(
    id                  integer not null
        constraint cars_pk
            primary key autoincrement,
    manufacturer        text    not null,
    model               text    not null,
    registration_number text    not null,
    owner_id            integer not null
        references users,
    battery_volume      integer,
    preferred_battery_percent real    not null
);

create unique index cars_id_uindex
    on cars (id);

create unique index cars_registration_number_uindex
    on cars (registration_number);


create table parking_history
(
    id               integer not null
        constraint parking_history_pk
            primary key autoincrement,
    place_id         integer not null
        references places,
    car_id           integer not null
        references cars,
    start_time       text    not null,
    end_time         text,
    battery_on_start real    not null,
    battery_on_end   real,
    charging_speed   integer not null
);

create unique index parking_history_id_uindex
    on parking_history (id);


create table sessions
(
    session_token text    not null
        primary key,
    valid_to      text    not null,
    user_id       integer not null
        references users
);

create table energy_history
(
    id        integer not null
        constraint energy_history_pk
            primary key autoincrement,
    post_date text    not null,
    value     real    not null
);

create unique index energy_history_id_uindex
    on energy_history (id);
