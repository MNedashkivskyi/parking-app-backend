insert into parkings (id, name, description, city, street, postal_code, image_url) values (0, 'Parking 0', 'Opis 0', 'Warszawa', 'Nowowiejska 15/19', '00-665', 'https://images.pexels.com/photos/1756957/pexels-photo-1756957.jpeg?cs=srgb&dl=pexels-brett-sayles-1756957.jpg&fm=jpg');
insert into parkings (id, name, description, city, street, postal_code, image_url) values (1, 'Parking 1', 'Opis 1', 'Karków', 'Podzamcze 5', '33-333', 'https://images.pexels.com/photos/1000633/pexels-photo-1000633.jpeg?cs=srgb&dl=pexels-jose-espinal-1000633.jpg&fm=jpg');

insert into levels (id, name, total_places, parking_id) values (0, 'Poziom 0', 4, 0);
insert into levels (id, name, total_places, parking_id) values (1, 'Poziom 1', 4, 0);
insert into levels (id, name, total_places, parking_id) values (2, 'Poziom 0', 4, 1);
insert into levels (id, name, total_places, parking_id) values (3, 'Poziom 1', 4, 1);

insert into places (id, status, level_id) values (0, 0, 0);
insert into places (id, status, level_id) values (1, 1, 0);
insert into places (id, status, level_id) values (2, 2, 0);
insert into places (id, status, level_id) values (3, 0, 0);
insert into places (id, status, level_id) values (4, 1, 1);
insert into places (id, status, level_id) values (5, 2, 1);
insert into places (id, status, level_id) values (6, 0, 1);
insert into places (id, status, level_id) values (7, 1, 1);
insert into places (id, status, level_id) values (8, 2, 2);
insert into places (id, status, level_id) values (9, 0, 2);
insert into places (id, status, level_id) values (10, 1, 2);
insert into places (id, status, level_id) values (11, 2, 2);
insert into places (id, status, level_id) values (12, 0, 3);
insert into places (id, status, level_id) values (13, 1, 3);
insert into places (id, status, level_id) values (14, 2, 3);
insert into places (id, status, level_id) values (15, 0, 3);

insert into cars (id, manufacturer, model, registration_number, owner_id, battery_volume, preferred_battery_percent) values (0, 'Peugeot', '308 I', 'W0 TEST0', 0, 1800000, 20);
insert into cars (id, manufacturer, model, registration_number, owner_id, battery_volume, preferred_battery_percent) values (1, 'Peugeot', '308 II', 'W0 TEST1', 0, 1800000, 20);
insert into cars (id, manufacturer, model, registration_number, owner_id, battery_volume, preferred_battery_percent) values (2, 'BMW', 'M3', 'W0 TEST2', 0, 1800000, 20);
insert into cars (id, manufacturer, model, registration_number, owner_id, battery_volume, preferred_battery_percent) values (3, 'Ferrari', 'LaFerrari', 'W0 TEST3', 1, 1800000, 20);

insert into parking_history values (0, 0, 0, '2021-12-19 15:16:33.634468', null, 20.05, null, 600000);

insert into energy_history values (0, '2021-01-15 12:00:00.000000', 1);
