CREATE DATABASE bokseri;
USE bokseri;

CREATE TABLE boksač (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ime VARCHAR(255) NOT NULL,
    prezime VARCHAR(255) NOT NULL,
    kategorija VARCHAR(255),
    drzava VARCHAR(255),
    broj_pobjeda INT DEFAULT 0,
    broj_poraza INT DEFAULT 0,
    broj_nerjesenih INT DEFAULT 0,
    stil VARCHAR(255)
);

CREATE TABLE borbe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    datum DATE,
    runde INT,
    zavrseno_na_bodove BOOLEAN,
    nokaut BOOLEAN,
    prekid BOOLEAN,
    pobjednik_id INT,
    gubitnik_id INT,
    FOREIGN KEY (pobjednik_id) REFERENCES boksač(id),
    FOREIGN KEY (gubitnik_id) REFERENCES boksač(id)
);
