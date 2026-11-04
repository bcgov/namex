INSERT INTO synonym (synonyms_text) VALUES ('10, onezero, ten, tenth, twentieth, twenty, twozero, twozeroth, x');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '10, onezero, ten, tenth, twentieth, twenty, twozero, twozeroth, x', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('11, 11th, eleven, eleventh, oneone, oneoneth, xi');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '11, 11th, eleven, eleventh, oneone, oneoneth, xi', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('12, 12th, onetwo, onetwoth, twelfth, twelve, twelveth, xii');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '12, 12th, onetwo, onetwoth, twelfth, twelve, twelveth, xii', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('13, 13th, onethree, onethreeth, thirteen, thirteenth, xiii');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '13, 13th, onethree, onethreeth, thirteen, thirteenth, xiii', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('14, 14th, fourteen, fourtenth, onefour, onefourth, xiv');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '14, 14th, fourteen, fourtenth, onefour, onefourth, xiv', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('15, 15th, fifteen, fiftenth, onefive, onefiveth, xv');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '15, 15th, fifteen, fiftenth, onefive, onefiveth, xv', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('16, 16th, onesix, onesixth, sixteen, sixtenth, xvi');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '16, 16th, onesix, onesixth, sixteen, sixtenth, xvi', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('17, 17th, oneseven, oneseventh, seventeen, sevententh, xvii');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '17, 17th, oneseven, oneseventh, seventeen, sevententh, xvii', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('18, 18th, eighteen, eightenth, oneight, oneighth, xviii');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '18, 18th, eighteen, eightenth, oneight, oneighth, xviii', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('19, 19th, nineteen, ninetenth, onenine, onenineth, xix');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '19, 19th, nineteen, ninetenth, onenine, onenineth, xix', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('1st, first');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '1st, first', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('1stnation, 1stpeople, aboriginal, firstnation, firstpeople, indian, indigenous, native');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '1stnation, 1stpeople, aboriginal, firstnation, firstpeople, indian, indigenous, native', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('21, 21st, twentyfirst, twentyone, twone, twonest, xxi');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '21, 21st, twentyfirst, twentyone, twone, twonest, xxi', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('22, 22nd, twentysecond, twentytwo, twotwo, twotwond, xxii');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '22, 22nd, twentysecond, twentytwo, twotwo, twotwond, xxii', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('23, 23rd, twentythird, twentythree, twothree, twothreerd, xxiii');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '23, 23rd, twentythird, twentythree, twothree, twothreerd, xxiii', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('24, 24th, twentyfour, twentyfourth, twofour, twofourth, xxiv');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '24, 24th, twentyfour, twentyfourth, twofour, twofourth, xxiv', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('25, 25th, twentyfifth, twentyfive, twofive, twofiveth, xxv');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '25, 25th, twentyfifth, twentyfive, twofive, twofiveth, xxv', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('26, 26th, twentysix, twentysixth, twosix, twosixth, xxvi');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '26, 26th, twentysix, twentysixth, twosix, twosixth, xxvi', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('27, 27th, twentyseven, twentyseventh, twoseven, twoseventh, xxvii');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '27, 27th, twentyseven, twentyseventh, twoseven, twoseventh, xxvii', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('28, 28th, twentyeight, twentyeighth, twoeight, twoeighth, xxviii');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '28, 28th, twentyeight, twentyeighth, twoeight, twoeighth, xxviii', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('29, 29th, twentynine, twentyninth, twonine, twonineth, xxix');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '29, 29th, twentynine, twentyninth, twonine, twonineth, xxix', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('2nd hand, 2ndhand, consign, consignment, second hand, secondhand, thrift, used');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '2nd hand, 2ndhand, consign, consignment, second hand, secondhand, thrift, used', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('2nd, second');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '2nd, second', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('3, 3rd, iii, third, three, threerd');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '3, 3rd, iii, third, three, threerd', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('30, 30th, thirtieth, thirty, threezero, threezeroth, xxx');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '30, 30th, thirtieth, thirty, threezero, threezeroth, xxx', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('31, 31st, thirtyfirst, thirtyone, threeone, threeonest, xxxi');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '31, 31st, thirtyfirst, thirtyone, threeone, threeonest, xxxi', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('32, 32nd, thirtysecond, thirtytwo, threetwo, threetwond, xxxii');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '32, 32nd, thirtysecond, thirtytwo, threetwo, threetwond, xxxii', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('33, 33rd, thirtythird, thirtythree, threethree, threethreerd, xxxiii');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '33, 33rd, thirtythird, thirtythree, threethree, threethreerd, xxxiii', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('33, 33rd, thirtythird, thirtythree, threethree, xxxiii');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '33, 33rd, thirtythird, thirtythree, threethree, xxxiii', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('34, 34th, thirtyfour, thirtyfourth, threefour, threefourth, xxxiv');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '34, 34th, thirtyfour, thirtyfourth, threefour, threefourth, xxxiv', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('35, 35th, thirtyfifth, thirtyfive, threefive, threefiveth, xxxv');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '35, 35th, thirtyfifth, thirtyfive, threefive, threefiveth, xxxv', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('36, 36th, thirtysix, thirtysixth, threesix, threesixth, xxxvi');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '36, 36th, thirtysix, thirtysixth, threesix, threesixth, xxxvi', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('37, 37th, thirtyseven, thirtyseventh, threeseven, threeseventh, xxxvii');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '37, 37th, thirtyseven, thirtyseventh, threeseven, threeseventh, xxxvii', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('38, 38th, thirtyeight, thirtyeighth, threeeight, threeeighth, xxxviii');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '38, 38th, thirtyeight, thirtyeighth, threeeight, threeeighth, xxxviii', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('39, 39th, thirtynine, thirtyninth, threenine, threenineth, xxxix');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '39, 39th, thirtynine, thirtyninth, threenine, threenineth, xxxix', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('3rd, third');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '3rd, third', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('40, 40th, fortieth, forty, fourzero, fourzeroth, xl');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '40, 40th, fortieth, forty, fourzero, fourzeroth, xl', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('41, 41st, fortyfirst, fortyone, fourone, fouronest, xli');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '41, 41st, fortyfirst, fortyone, fourone, fouronest, xli', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('42, 42nd, fortysecond, fortytwo, fourtwo, fourtwond, xlii');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '42, 42nd, fortysecond, fortytwo, fourtwo, fourtwond, xlii', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('420, bud, cannabis, cannibus, cbd, chronic, compasion, cron, dispensary, four twozero, ganja, marihuana, marijuana, maryjane, medicinal, pot, thc, weed');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '420, bud, cannabis, cannibus, cbd, chronic, compasion, cron, dispensary, four twozero, ganja, marihuana, marijuana, maryjane, medicinal, pot, thc, weed', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('43, 43rd, fortythird, fortythree, fourthree, fourthreerd, xliii');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '43, 43rd, fortythird, fortythree, fourthree, fourthreerd, xliii', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('43, 43th, fortythird, fortythree, fourthree, fourthreed, xliii');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '43, 43th, fortythird, fortythree, fourthree, fourthreed, xliii', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('44, 44th, fortyfour, fortyfourth, fourfour, fourfourth, xliv');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '44, 44th, fortyfour, fortyfourth, fourfour, fourfourth, xliv', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('45, 45th, fortyfifth, fortyfive, fourfive, fourfiveth, xlv');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '45, 45th, fortyfifth, fortyfive, fourfive, fourfiveth, xlv', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('46, 46th, fortysix, fortysixth, foursix, foursixth, xlvi');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '46, 46th, fortysix, fortysixth, foursix, foursixth, xlvi', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('47, 47th, fortyseven, fortyseventh, fourseven, fourseventh, xlvii');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '47, 47th, fortyseven, fortyseventh, fourseven, fourseventh, xlvii', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('48, 48th, fortyeight, fortyeighth, foureight, foureighth, xlviii');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '48, 48th, fortyeight, fortyeighth, foureight, foureighth, xlviii', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('49, 49th, fortynine, fortyninth, fournine, fournineth, xlix');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '49, 49th, fortynine, fortyninth, fournine, fournineth, xlix', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('4mula, 4mulas, formula, fourmula');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '4mula, 4mulas, formula, fourmula', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('4th, fourth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '4th, fourth', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('4x4, allterain, atv, fourxfour, offroad, quad');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '4x4, allterain, atv, fourxfour, offroad, quad', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('5, 5th, V, fifth, five, fiveth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '5, 5th, V, fifth, five, fiveth', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('50, 50th, fiftieth, fifty, fivezero, fivezeroth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '50, 50th, fiftieth, fifty, fivezero, fivezeroth', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('51, 51st, fiftyfirst, fiftyone, fiveone, fiveonest');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '51, 51st, fiftyfirst, fiftyone, fiveone, fiveonest', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('52, 52nd, fiftysecond, fiftytwo, fivetwo, fivetwond');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '52, 52nd, fiftysecond, fiftytwo, fivetwo, fivetwond', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('53, 53rd, fiftythird, fiftythree, fivethree, fivethreerd');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '53, 53rd, fiftythird, fiftythree, fivethree, fivethreerd', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('53, 53st, fiftythird, fiftythree, fivethree, fivethreed');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '53, 53st, fiftythird, fiftythree, fivethree, fivethreed', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('54, 54th, fiftyfour, fiftyfourth, fivefour, fivefourth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '54, 54th, fiftyfour, fiftyfourth, fivefour, fivefourth', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('55, 55th, fiftyfifth, fiftyfive, fivefive, fivefiveth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '55, 55th, fiftyfifth, fiftyfive, fivefive, fivefiveth', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('56, 56th, fiftysix, fiftysixth, fivesix, fivesixth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '56, 56th, fiftysix, fiftysixth, fivesix, fivesixth', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('57, 57th, fiftyseven, fiftyseventh, fiveseven, fiveseventh');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '57, 57th, fiftyseven, fiftyseventh, fiveseven, fiveseventh', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('58, 58th, fiftyeight, fiftyeighth, fiveight, fiveighth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '58, 58th, fiftyeight, fiftyeighth, fiveight, fiveighth', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('59, 59th, fiftynine, fiftyninth, fivenine, fivenineth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '59, 59th, fiftynine, fiftyninth, fivenine, fivenineth', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('5th, fifth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '5th, fifth', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('6, 6th, six, sixth, vi');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '6, 6th, six, sixth, vi', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('60, 60th, sixtieth, sixty, sixzero, sixzeroth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '60, 60th, sixtieth, sixty, sixzero, sixzeroth', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('61, 61st, sixone, sixonest, sixtyfirst, sixtyone');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '61, 61st, sixone, sixonest, sixtyfirst, sixtyone', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('62, 62nd, sixtwo, sixtwond, sixtysecond, sixtytwo');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '62, 62nd, sixtwo, sixtwond, sixtysecond, sixtytwo', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('63, 63rd, sixthree, sixthreed, sixtythree, sixtythrird');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '63, 63rd, sixthree, sixthreed, sixtythree, sixtythrird', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('63, 63rd, sixthree, sixthreerd, sixtythird, sixtythree');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '63, 63rd, sixthree, sixthreerd, sixtythird, sixtythree', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('64, 64th, sixfour, sixfourth, sixtyfour, sixtyfourth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '64, 64th, sixfour, sixfourth, sixtyfour, sixtyfourth', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('65, 65th, sixfive, sixfiveth, sixtyfifth, sixtyfive');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '65, 65th, sixfive, sixfiveth, sixtyfifth, sixtyfive', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('66, 66th, lxvi, sixsix, sixsixth, sixtysix, sixtysixth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '66, 66th, lxvi, sixsix, sixsixth, sixtysix, sixtysixth', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('67, 67th, sixseven, sixseventh, sixtyseven, sixtyseventh');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '67, 67th, sixseven, sixseventh, sixtyseven, sixtyseventh', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('68, 68th, sixeight, sixeighth, sixtyeight, sixtyeighth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '68, 68th, sixeight, sixeighth, sixtyeight, sixtyeighth', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('69, 69th, lxix, sixnine, sixnineth, sixtynine, sixtyninth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '69, 69th, lxix, sixnine, sixnineth, sixtynine, sixtyninth', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('6th, sixth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '6th, sixth', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('70, 70th, seventieth, seventy, sevenzero, sevenzeroth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '70, 70th, seventieth, seventy, sevenzero, sevenzeroth', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('71, 71st, sevenone, sevenonest, seventyfirst, seventyone');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '71, 71st, sevenone, sevenonest, seventyfirst, seventyone', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('72, 72nd, seventwo, seventwond, seventysecond, seventytwo');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '72, 72nd, seventwo, seventwond, seventysecond, seventytwo', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('73, 73rd, seventhree, seventhreed, seventythird, seventythree');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '73, 73rd, seventhree, seventhreed, seventythird, seventythree', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('73, 73rd, seventhree, seventhreerd, seventythird, seventythree');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '73, 73rd, seventhree, seventhreerd, seventythird, seventythree', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('74, 74th, sevenfour, sevenfourth, seventyfour, seventyfourth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '74, 74th, sevenfour, sevenfourth, seventyfour, seventyfourth', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('7th, seventh');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '7th, seventh', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('88, 88th, eighthree, eighthreerd, eightythird, eightythree');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '88, 88th, eighthree, eighthreerd, eightythird, eightythree', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('8th, eighth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '8th, eighth', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('93, 93rd, ninethree, ninethreerd, ninetythird, ninetythree');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '93, 93rd, ninethree, ninethreerd, ninetythird, ninetythree', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('98, 98th, nineight, nineighth, ninetyeight, ninetyeighth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '98, 98th, nineight, nineighth, ninetyeight, ninetyeighth', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('9th, nineth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', '9th, nineth', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('abbatoir, butcher, halal, meat, packer, packing, sausage, slaughter');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'abbatoir, butcher, halal, meat, packer, packing, sausage, slaughter', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('abe, abey, abie, aby');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'abe, abey, abie, aby', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('abel, able');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'abel, able', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('abode, acre, build, civil, construction, contract, develop, estate, handyman, home, land, listing, meadow, property, real, remodel, reno, renovation, restore, structure');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'abode, acre, build, civil, construction, contract, develop, estate, handyman, home, land, listing, meadow, property, real, remodel, reno, renovation, restore, structure', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('academic, college, institute, school');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'academic, college, institute, school', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('accelerate, xlr8, xlreight');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'accelerate, xlr8, xlreight', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('access, axis, axys');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'access, axis, axys', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('accommodate, reservation');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'accommodate, reservation', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('account, accountant, admin, biz, bookkeeping, business, compliance, corporate, cpa, dictate, document, hr, office, personnel, secretary, tax, title, transcript, transcription, type, wordprocessing');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'account, accountant, admin, biz, bookkeeping, business, compliance, corporate, cpa, dictate, document, hr, office, personnel, secretary, tax, title, transcript, transcription, type, wordprocessing', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('acept, asset, capital, capitol, credit, equity, finance, fund, invest, lend, loan, mortgage, mutualfund, payday, security, wealth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'acept, asset, capital, capitol, credit, equity, finance, fund, invest, lend, loan, mortgage, mutualfund, payday, security, wealth', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('acoustics, audio, broadcast, cd, dejay, dj, electronic, homeentertainment, music, radio, record, sound, stereo, tape');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'acoustics, audio, broadcast, cd, dejay, dj, electronic, homeentertainment, music, radio, record, sound, stereo, tape', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('acqua, acwa, aqua');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'acqua, acwa, aqua', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('acrylic, plastic, poli, poly, pvc, vinyl');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'acrylic, plastic, poli, poly, pvc, vinyl', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('adjudicate, adr, arbitrate, dispute, mediate, negotiate, resolution');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'adjudicate, adr, arbitrate, dispute, mediate, negotiate, resolution', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('adjust, appraisal, claim');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'adjust, appraisal, claim', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('adventure, cruise, expedition, getaway, holiday, safari, tour, travel, trip, vacation');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'adventure, cruise, expedition, getaway, holiday, safari, tour, travel, trip, vacation', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('advertising, marketing, media, radio, television');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'advertising, marketing, media, radio, television', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('advise, analyze, coach, consult, counsel');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'advise, analyze, coach, consult, counsel', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('aerial, arial, ariel');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'aerial, arial, ariel', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('aeries, aries');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'aeries, aries', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('aero, aeroplane, aerospace, air, airplane, arow, aviate, ayr, chopper, flight, flite, fly, flyte, heli, jet, plane, prop, space, ultralight');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'aero, aeroplane, aerospace, air, airplane, arow, aviate, ayr, chopper, flight, flite, fly, flyte, heli, jet, plane, prop, space, ultralight', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('aerobic, bootcamp, cardio, circuit, condition, exercise, fit, gym, hot tub, hottub, hotub, kundalini, movement, pilates, pool, slim, spa, strength, thin, train, weight, workout, yoga');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'aerobic, bootcamp, cardio, circuit, condition, exercise, fit, gym, hot tub, hottub, hotub, kundalini, movement, pilates, pool, slim, spa, strength, thin, train, weight, workout, yoga', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('aesthetic, barber, beard, beauty, brow, coif, coiffure, cosmetic, cosmetology, cut, day spa, dayspa, electrolysis, esthetic, extenstion, groom, hair, lash, makceup, manicure, nail, salon, skin, style');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'aesthetic, barber, beard, beauty, brow, coif, coiffure, cosmetic, cosmetology, cut, day spa, dayspa, electrolysis, esthetic, extenstion, groom, hair, lash, makceup, manicure, nail, salon, skin, style', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('agen, brocer, factor');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'agen, brocer, factor', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('aggregate, crush, fill, gravel, mater, sand, soil');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'aggregate, crush, fill, gravel, mater, sand, soil', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('agra, agri, catle, farm, livestoc, ranch, stable');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'agra, agri, catle, farm, livestoc, ranch, stable', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('aikido, aikikai, bj, capoeira, jiujitsu, judo, karate, kickbox, kungfu, martial, mma, selfdefence, taekwondo, wingchung');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'aikido, aikikai, bj, capoeira, jiujitsu, judo, karate, kickbox, kungfu, martial, mma, selfdefence, taekwondo, wingchung', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('aircondition, balance, climate, comfort, furnace, furnace, gasfit, heat, hvac, mechanical, pipefit, plumbing, sheetmetal, vent');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'aircondition, balance, climate, comfort, furnace, furnace, gasfit, heat, hvac, mechanical, pipefit, plumbing, sheetmetal, vent', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('airport, blablacar, black car, cab, chauffeur, limo, livery, taxi, towncar, uber');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'airport, blablacar, black car, cab, chauffeur, limo, livery, taxi, towncar, uber', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('al, awl');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'al, awl', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('alan, alen, allan, allen');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'alan, alen, allan, allen', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('alarm, forensic, gard, guard, investigate, locksmith, monitor, patrol, protect, response, security, surveillance, tactic, watch');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'alarm, forensic, gard, guard, investigate, locksmith, monitor, patrol, protect, response, security, surveillance, tactic, watch', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('alcohol, distillery, liquor, moonshine, spirit');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'alcohol, distillery, liquor, moonshine, spirit', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('ale, beer, brew, lager');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'ale, beer, brew, lager', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('aley, ali, biliard, bowl, lanes');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'aley, ali, biliard, bowl, lanes', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('alfa, alpha');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'alfa, alpha', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('alix, alx');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'alix, alx', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('aloy, casting, duct, fab, forge, foundry, iron, machine, metal, rail, reinforce, stainless, stamping, steel, tool, weld');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'aloy, casting, duct, fab, forge, foundry, iron, machine, metal, rail, reinforce, stainless, stamping, steel, tool, weld', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('alteration, crest, dresmac, embroider, sew, stitch, tailor');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'alteration, crest, dresmac, embroider, sew, stitch, tailor', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('ambiance, ambience');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'ambiance, ambience', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('ambulance, emergency, firstaid, firstresponse, paramedic, paramedical');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'ambulance, emergency, firstaid, firstresponse, paramedic, paramedical', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('ammo, ammunition, armament, armor, arms, artillery, firearm, gun, pistol, rifle, weapon');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'ammo, ammunition, armament, armor, arms, artillery, firearm, gun, pistol, rifle, weapon', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('angling, aquaculture, aquafarm, charter, excursion, fish, guid, mariculture, outfit, oyster, salmon, seafarm, seafod, shellfish, sightsee, sport fish');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'angling, aquaculture, aquafarm, charter, excursion, fish, guid, mariculture, outfit, oyster, salmon, seafarm, seafod, shellfish, sightsee, sport fish', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('animal, criter, pet, vet');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'animal, criter, pet, vet', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('animate, carton, cast, cinema, dud, dvd, entertain, film, media, motion, movie, picture, production, release, studios, talent, television, theater, theatre, tv, vcr, video');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'animate, carton, cast, cinema, dud, dvd, entertain, film, media, motion, movie, picture, production, release, studios, talent, television, theater, theatre, tv, vcr, video', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('answer, call, cell, cellular, com, longdistance, mobile, network, page, phone, reconect, tel, telephone, voice, voip, wifi, wireles, wireless');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'answer, call, cell, cellular, com, longdistance, mobile, network, page, phone, reconect, tel, telephone, voice, voip, wifi, wireles, wireless', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('antiq, bailif, colect, memorab, proces, trac');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'antiq, bailif, colect, memorab, proces, trac', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('aparel, atire, boutique, casual, clothes, clothier, clothing, couture, fashion, garb, garment, wardrobe, wear');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'aparel, atire, boutique, casual, clothes, clothier, clothing, couture, fashion, garb, garment, wardrobe, wear', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('apartment, apt, condo, court, loft, manor, residence, strata, stratum, suite, townhome, townhouse, vila');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'apartment, apt, condo, court, loft, manor, residence, strata, stratum, suite, townhome, townhouse, vila', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('apiary, apiculture, apitherapy, bee, beekeeping, honey, nectar, pollen');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'apiary, apiculture, apitherapy, bee, beekeeping, honey, nectar, pollen', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('apnea, cpap, oxygen, respiration');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'apnea, cpap, oxygen, respiration', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('apostle, apotres');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'apostle, apotres', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('apothecary, chemist, dispensary, drug, med, medicine, pharmacy, prescription, rx');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'apothecary, chemist, dispensary, drug, med, medicine, pharmacy, prescription, rx', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('appliance, coldstorage, foodlocker, freeze, fridge, ice, refrige');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'appliance, coldstorage, foodlocker, freeze, fridge, ice, refrige', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('application, apps, cloud, computer, data, interactive, laptop, pc, peripheral, program, software, solution, system, ware');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'application, apps, cloud, computer, data, interactive, laptop, pc, peripheral, program, software, solution, system, ware', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('ar, are');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'ar, are', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('arb, brush, fal, loging, prun, stump, trecare, treprun, treservice, tresurgeon, tretop');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'arb, brush, fal, loging, prun, stump, trecare, treprun, treservice, tresurgeon, tretop', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('archive, museum, records');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'archive, museum, records', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('arctic, artec, artic');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'arctic, artec, artic', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('argentum, bitcoin, blockchain, cloudchain, crypto, ether, ethereum, fulfill, hash, pay, remit, setl');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'argentum, bitcoin, blockchain, cloudchain, crypto, ether, ethereum, fulfill, hash, pay, remit, setl', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('armor, armour');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'armor, armour', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('aron, erin, eron');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'aron, erin, eron', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('arora, aurora');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'arora, aurora', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('art, gallery, sculpture, studio');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'art, gallery, sculpture, studio', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('asbestos, disaster, flood, hazard, hazmat, mold, mould, remediate');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'asbestos, disaster, flood, hazard, hazmat, mold, mould, remediate', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('asphalt, blacktop, interlock, pave, rhode, road, rode, tar');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'asphalt, blacktop, interlock, pave, rhode, road, rode, tar', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('asur, benefit, casualty, indemnity, insure, life, underwrite');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'asur, benefit, casualty, indemnity, insure, life, underwrite', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('ateli, bed, furniture, futon, mattress, sleep');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'ateli, bed, furniture, futon, mattress, sleep', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('atelier, coating, decor, design, interior, living, paint, stage, wallcover, wallpaper');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'atelier, coating, decor, design, interior, living, paint, stage, wallcover, wallpaper', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('athletic, outdoor, run, sport');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'athletic, outdoor, run, sport', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('atlin, atlyn');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'atlin, atlyn', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('atrium, conservator, greenhouse, hothouse, skylight, skylite, solar, sunroom');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'atrium, conservator, greenhouse, hothouse, skylight, skylite, solar, sunroom', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('attraction, carnival, celebratr, conferencr, convention, event, exhibit, expo, fair, fare, fayre, festival, happening, meeting, occasion, occurence, present, show');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'attraction, carnival, celebratr, conferencr, convention, event, exhibit, expo, fair, fare, fayre, festival, happening, meeting, occasion, occurence, present, show', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('auction, bid, liquidate');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'auction, bid, liquidate', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('audiolog, hear, here');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'audiolog, hear, here', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('audit, inventor, stock');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'audit, inventor, stock', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('auld, old, olde, ole');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'auld, old, olde, ole', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('auto, body, car, collision, fix, garage, mechanic, motor, repair, service, tune, vehicle');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'auto, body, car, collision, fix, garage, mechanic, motor, repair, service, tune, vehicle', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('autoclave, sterilize');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'autoclave, sterilize', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('autocourt, bedbreakfast, guest, hostel, hotel, inn, lodge, motel, motorcourt, motorhotel, motorinn, resort, suites');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'autocourt, bedbreakfast, guest, hostel, hotel, inn, lodge, motel, motorcourt, motorhotel, motorinn, resort, suites', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('automate, cable, control, electric, instrument, led, light, lite, lyte, measure, robot, wire');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'automate, cable, control, electric, instrument, led, light, lite, lyte, measure, robot, wire', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('automatic, clutch, diferential, driveline, gear, transmision');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'automatic, clutch, diferential, driveline, gear, transmision', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('autospa, carwash, detail');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'autospa, carwash, detail', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('autosport, motorsport, performance, race, speed');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'autosport, motorsport, performance, race, speed', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('avatar, avitar, avtar');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'avatar, avitar, avtar', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('aviary, bird');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'aviary, bird', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('award, engrave, trophy');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'award, engrave, trophy', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('awning, canopy, canvas, tarp, tent');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'awning, canopy, canvas, tarp, tent', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('axi, axy');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'axi, axy', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('aye, eye');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'aye, eye', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('bachoe, bobcat, buldoz, dig, ditch, doz, earth, grad, gradal, trench, xcavat');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'bachoe, bobcat, buldoz, dig, ditch, doz, earth, grad, gradal, trench, xcavat', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('bagel, bake, baking, bread, cake, cookie, muffin, pastry, patisiery, patisserie, pie');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'bagel, bake, baking, bread, cake, cookie, muffin, pastry, patisiery, patisserie, pie', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('baggage, luggage, suitcase');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'baggage, luggage, suitcase', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('baha, baja');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'baha, baja', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('bait, lure, rea, rel, rod, tacle');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'bait, lure, rea, rel, rod, tacle', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('banquet, canteen, cater, concsesion, foodserve, foodtruck, mealprep');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'banquet, canteen, cater, concsesion, foodserve, foodtruck, mealprep', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('barbecue, barbq, bq');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'barbecue, barbq, bq', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('barclay, barkley');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'barclay, barkley', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('bare, bear');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'bare, bear', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('barge, carrier, cartage, courier, delivery, diesel, dispatch, dray, errand, express, express, forward, freight, haul, hawl, hotshot, intermodal, line, lobed, logistic, lowbed, mail, messenger, move, navigate, parcel, recovery, refer, shipper, shipping, transfer, transport, truck, tug, wrecker');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'barge, carrier, cartage, courier, delivery, diesel, dispatch, dray, errand, express, express, forward, freight, haul, hawl, hotshot, intermodal, line, lobed, logistic, lowbed, mail, messenger, move, navigate, parcel, recovery, refer, shipper, shipping, transfer, transport, truck, tug, wrecker', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('barrister, law, legal, litigate, solicitor');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'barrister, law, legal, litigate, solicitor', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('bartend, beverage, mixology');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'bartend, beverage, mixology', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('bath, cabinet, casew, counter, cupboard, kitchen, solidsurface');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'bath, cabinet, casew, counter, cupboard, kitchen, solidsurface', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('beach, beech');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'beach, beech', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('beau, bough, bow');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'beau, bough, bow', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('bereave, cemetery, cremate, funeral, memorial, mortuary');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'bereave, cemetery, cremate, funeral, memorial, mortuary', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('bi, buy, by');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'bi, buy, by', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('bijou, diamon, diamond, explore, gem, gold, goldsmith, jem, jewel, joial, jual, mine, mineral, mining, placer, prospect, resourc, silver, silversmith');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'bijou, diamon, diamond, explore, gem, gold, goldsmith, jem, jewel, joial, jual, mine, mineral, mining, placer, prospect, resourc, silver, silversmith', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('bike, chopper, cycle, moto, mtb, mx, sbk, scooter, vtwin');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'bike, chopper, cycle, moto, mtb, mx, sbk, scooter, vtwin', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('billboard, neon, sign, sine');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'billboard, neon, sign, sine', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('bin, compost, conserve, convers, convert, disposal, ecol, effluent, environment, garbage, recycle, refuse, rubbish, sanitation, scrap, trash, waste');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'bin, compost, conserve, convers, convert, disposal, ecol, effluent, environment, garbage, recycle, refuse, rubbish, sanitation, scrap, trash, waste', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('birth, doula, midwife, obstetrician');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'birth, doula, midwife, obstetrician', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('bistro, buffet, cafe, cantina, cappuccino, chai, coffee, convenience, cuisine, deli, dine, diner, dining, eat, eater, eats, edible, espresso, expresso, food, galley, grill, grocer, java, kitchen, latte, market, mart, restaurant, roast, sandwich, shop, snack, snax, steak, store, takeout, taverna, tea, tiffin, tratoria, variety');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'bistro, buffet, cafe, cantina, cappuccino, chai, coffee, convenience, cuisine, deli, dine, diner, dining, eat, eater, eats, edible, espresso, expresso, food, galley, grill, grocer, java, kitchen, latte, market, mart, restaurant, roast, sandwich, shop, snack, snax, steak, store, takeout, taverna, tea, tiffin, tratoria, variety', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('bite, byte');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'bite, byte', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('blacksmith, farrier, horseshoe');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'blacksmith, farrier, horseshoe', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('blast, dynamite, explosive, nitro, powder, tnt');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'blast, dynamite, explosive, nitro, powder, tnt', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('bleu, blew, blu, blue');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'bleu, blew, blu, blue', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('blind, cover, curtain, drape, shade, shutter, window');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'blind, cover, curtain, drape, shade, shutter, window', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('blossom, floral, florist, flower');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'blossom, floral, florist, flower', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('blueprint, cad, draft, draught, draw, plan');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'blueprint, cad, draft, draught, draw, plan', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('blvd, boulevard');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'blvd, boulevard', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('board, canoe, kayak, paddle, sup, surf, whitewater');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'board, canoe, kayak, paddle, sup, surf, whitewater', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('boat, marina, nautical, outboard, sail, ship, vessel, watercraft, yacht');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'boat, marina, nautical, outboard, sail, ship, vessel, watercraft, yacht', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('bodywork, massage, physio, physiotherapy, reflx, rehab, therapy');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'bodywork, massage, physio, physiotherapy, reflx, rehab, therapy', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('bolt, fasten, nut, screw, spiral');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'bolt, fasten, nut, screw, spiral', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('book, copied, copy, desktop, director, duplicate, edit, gazete, graff, graph, guide, litho, magazine, news, press, print, publication, publish, report, reproduction, screen, wecl, write');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'book, copied, copy, desktop, director, duplicate, edit, gazete, graff, graph, guide, litho, magazine, news, press, print, publication, publish, report, reproduction, screen, wecl, write', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('boot, cobbler, footwear, shoe');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'boot, cobbler, footwear, shoe', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('box, container, package');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'box, container, package', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('braemar, braymar');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'braemar, braymar', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('brian, bryan');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'brian, bryan', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('brick, brix, bryc, granite, mason, monument, quartz, rock, slate, stone');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'brick, brix, bryc, granite, mason, monument, quartz, rock, slate, stone', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('bridal, wedding');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'bridal, wedding', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('bride, formal, groom, marriage, matrimony, wedding');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'bride, formal, groom, marriage, matrimony, wedding', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('bright, brite');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'bright, brite', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('brons, bronze');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'brons, bronze', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('bus, carriage, coach, shuttle, stage, trail, transit');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'bus, carriage, coach, shuttle, stage, trail, transit', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('caesar, ceasar, cesar, cesare');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'caesar, ceasar, cesar, cesare', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('cain, cane');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cain, cane', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('caisson, tunnel, underground');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'caisson, tunnel, underground', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('caladonia, caledonia');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'caladonia, caledonia', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('caliber, calibre');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'caliber, calibre', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('calona, celowna, clo');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'calona, celowna, clo', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('cambel, cambell, campbel, campbell');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cambel, cambell, campbel, campbell', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('camera, foto, image, photo');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'camera, foto, image, photo', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('camper, motorhome, recreationalvehicle, recreationvehicle, rv, trailer');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'camper, motorhome, recreationalvehicle, recreationvehicle, rv, trailer', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('can, cdn');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'can, cdn', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('candle, parafin, wax');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'candle, parafin, wax', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('cando, candu');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cando, candu', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('candy, chocolate, confection, sweet');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'candy, chocolate, confection, sweet', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('canine, cnine, dawg, dog, hound, kennel, pooch, pup');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'canine, cnine, dawg, dog, hound, kennel, pooch, pup', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('canning, jam, jelly, pickle, preserve');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'canning, jam, jelly, pickle, preserve', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('capt, captain');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'capt, captain', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('carbonfiber, carbonfibre, composite');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'carbonfiber, carbonfibre, composite', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('card, greeting, station');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'card, greeting, station', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('career, carer, employ, hour, hr, humanresource, job, labor, labour, overload, personel, placement, recruit, staff, support, temp, workforce');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'career, carer, employ, hour, hr, humanresource, job, labor, labour, overload, personel, placement, recruit, staff, support, temp, workforce', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('caren, caron');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'caren, caron', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('carpentry, finish, frame, join, millwork, woodcraft, woodwork');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'carpentry, finish, frame, join, millwork, woodcraft, woodwork', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('carpet, ceramic, floor, hardwood, laminate, lino, marble, pottery, rug, terrazzo, til, tile');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'carpet, ceramic, floor, hardwood, laminate, lino, marble, pottery, rug, terrazzo, til, tile', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('carpool, carshare, rideshare');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'carpool, carshare, rideshare', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('cartograph, chart, geomatic, gis, map');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cartograph, chart, geomatic, gis, map', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('cartridge, ink, inking, inkjet, laser, lazer, printer, refill, toner');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cartridge, ink, inking, inkjet, laser, lazer, printer, refill, toner', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('cash, currency, exchange, forx, fourx, intercambio, money');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cash, currency, exchange, forx, fourx, intercambio, money', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('casino, gambling, gaming');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'casino, gambling, gaming', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('cat, feline');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cat, feline', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('cataract, cite, contact, eyewear, lens, lenz, opt, retina, sight, site, vision');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cataract, cite, contact, eyewear, lens, lenz, opt, retina, sight, site, vision', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('ce, se, sea');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'ce, se, sea', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('ceiling, drywall, gypsum, panel, taper, taping, texture');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'ceiling, drywall, gypsum, panel, taper, taping, texture', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('cellar, oenophile, vino, vintner, viticulture, wine');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cellar, oenophile, vino, vintner, viticulture, wine', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('celtic, seltic');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'celtic, seltic', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('cemco, chemco');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cemco, chemco', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('cement, concrete, crete, form, icf, placing, precast, readymix, rebar, redimix, redmix, reinforce, shotcrete');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cement, concrete, crete, form, icf, placing, precast, readymix, rebar, redimix, redmix, reinforce, shotcrete', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('cent, fragrance, fragrant, parfum, perfume, scent, sent');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cent, fragrance, fragrant, parfum, perfume, scent, sent', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('center, centre, mall, plaza, shoppingcenter, shoppingcentre, square');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'center, centre, mall, plaza, shoppingcenter, shoppingcentre, square', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('cey, loc, quay');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cey, loc, quay', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('charade, shirade');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'charade, shirade', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('charity, fundraiser, philanthropy');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'charity, fundraiser, philanthropy', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('check, cheque');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'check, cheque', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('checker, chequer');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'checker, chequer', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('cheese, cream, dairy, gelato, icecream, kefir, milk, yogourt, yogurt');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cheese, cream, dairy, gelato, icecream, kefir, milk, yogourt, yogurt', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('cher, shair, shar');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cher, shair, shar', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('chic, sheic');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'chic, sheic', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('chicken, fowl, poultry, turckey');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'chicken, fowl, poultry, turckey', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('chilcotin, tsilhqot''in');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'chilcotin, tsilhqot''in', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('childcare, cinder, daycare, earlylearn, montesori, nursery, playschol, preschol');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'childcare, cinder, daycare, earlylearn, montesori, nursery, playschol, preschol', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('chris, cris');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'chris, cris', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('christmas, xmas');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'christmas, xmas', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('chrystal, cristal, crystal');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'chrystal, cristal, crystal', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('cib, cyb, sib, syb');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cib, cyb, sib, syb', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('ciel, seal, sel');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'ciel, seal, sel', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('ciera, seara, siera');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'ciera, seara, siera', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('cigar, cigarette, ecig, ejuice, esmoke, hookah, juice, pipe, smoke, tobacco, vape');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cigar, cigarette, ecig, ejuice, esmoke, hookah, juice, pipe, smoke, tobacco, vape', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('cinabar, cinibar');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cinabar, cinibar', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('cirus, cyrus, sirus, syrus');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cirus, cyrus, sirus, syrus', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('citi, city');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'citi, city', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('clad, hardy, siding, xterior');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'clad, hardy, siding, xterior', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('clair, clare');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'clair, clare', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('clean, clen, custodian, domestic, handyman, housekeeper, janitor, maid, maintenance');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'clean, clen, custodian, domestic, handyman, housekeeper, janitor, maid, maintenance', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('clear, cler');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'clear, cler', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('cloth, drygood, fabric, material, rag, textile, tx');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cloth, drygood, fabric, material, rag, textile, tx', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('clubmaker, clubs, golf, gulf');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'clubmaker, clubs, golf, gulf', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('cmor, seamore, semore, seymour');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cmor, seamore, semore, seymour', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('cned, ned, neid');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cned, ned, neid', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('cnel, neal, neil');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cnel, neal, neil', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('cng, coal, drill, energy, fuel, gas, lng, lubricate, nrg, oil, petro, pipeline, propane, resource');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cng, coal, drill, energy, fuel, gas, lng, lubricate, nrg, oil, petro, pipeline, propane, resource', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('cnight, night, nite');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cnight, night, nite', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('cnowledge, educat, instruct, learn, seminar, teach, train, tutor');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cnowledge, educat, instruct, learn, seminar, teach, train, tutor', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('co-gen, cogen, energy, generate, hydro, power, utility');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'co-gen, cogen, energy, generate, hydro, power, utility', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('coat, cote');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'coat, cote', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('cohlman, coleman, colman');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cohlman, coleman, colman', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('coin, coyne, numismat, vend');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'coin, coyne, numismat, vend', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('coling, radiator');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'coling, radiator', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('collateral, pawn');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'collateral, pawn', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('colombia, columbia');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'colombia, columbia', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('color, colour');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'color, colour', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('compute, computer, technology');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'compute, computer, technology', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('concept, dream, idea');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'concept, dream, idea', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('container, depot, reload, store, terminal, transload, warehouse');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'container, depot, reload, store, terminal, transload, warehouse', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('convey, handle');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'convey, handle', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('cosy, cozy');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cosy, cozy', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('cotenai, cotenay, cutenai, kootenay');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cotenai, cotenay, cutenai, kootenay', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('courtenay, courtney');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'courtenay, courtney', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('craft, hobby, radiocontrol');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'craft, hobby, radiocontrol', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('crane, erect, rig, scaffold');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'crane, erect, rig, scaffold', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('crochet, knit, loom, spin, weave, wool, woven, yarn');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'crochet, knit, loom, spin, weave, wool, woven, yarn', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('cwahlicum, qualicum');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cwahlicum, qualicum', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('cwest, quest, qwest');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cwest, quest, qwest', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('cwestar, qestar, questar, sequester');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cwestar, qestar, questar, sequester', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('cwic, quic');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cwic, quic', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('cygnet, signet');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cygnet, signet', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('cymbal, drum, percusion, percussion');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cymbal, drum, percusion, percussion', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('cypress, cyprus');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'cypress, cyprus', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('dahl, dol');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'dahl, dol', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('daily, daley, daly');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'daily, daley, daly', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('davey, davie, davy');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'davey, davie, davy', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('day, dey');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'day, dey', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('deal, del');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'deal, del', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('delight, delite');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'delight, delite', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('delux, dlux');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'delux, dlux', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('demo, dismantle, salvage');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'demo, dismantle, salvage', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('dentist, implant, orthodontist, periodontist');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'dentist, implant, orthodontist, periodontist', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('dew, do, du');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'dew, do, du', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('diagnostic, mri, sonograph, ultrasound, xray');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'diagnostic, mri, sonograph, ultrasound, xray', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('dickson, dixon, dixson');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'dickson, dixon, dixson', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('diet, nourish, nutri, supplement, vita, vitamin');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'diet, nourish, nutri, supplement, vita, vitamin', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('dinamo, dynamo');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'dinamo, dynamo', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('div, scuba, submarin, subsea, underwater');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'div, scuba, submarin, subsea, underwater', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('doc, doctor, dr');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'doc, doctor, dr', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('dolfin, dolphin');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'dolfin, dolphin', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('done, dun');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'done, dun', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('drain, outfall, septic, sewage, sewer, wastewater');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'drain, outfall, septic, sewage, sewer, wastewater', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('dri, dry');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'dri, dry', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('driving, motoring');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'driving, motoring', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('drone, uav, unmaned');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'drone, uav, unmaned', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('duane, dwayne');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'duane, dwayne', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('dundarave, dunderave');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'dundarave, dunderave', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('e-mail, ecomm, ecommerce, email, homepage, host, isp, net, on-line, online, searchengine, seo, server, socialmedia, web');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'e-mail, ecomm, ecommerce, email, homepage, host, isp, net, on-line, online, searchengine, seo, server, socialmedia, web', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('early, irly');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'early, irly', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('easi, easy, eazy, ez, eze');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'easi, easy, eazy, ez, eze', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('eave, eavestrough, gutter');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'eave, eavestrough, gutter', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('ecel, ecsel, exel, xcel, xcl, xell, xl, xsel');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'ecel, ecsel, exel, xcel, xcl, xell, xl, xsel', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('eddie, eddy');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'eddie, eddy', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('efect, fx, stunt');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'efect, fx, stunt', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('eight, eighth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'eight, eighth', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('eighteight, eighteighth, eightyeight, eightyeighth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'eighteight, eighteighth, eightyeight, eightyeighth', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('eightfive, eightfiveth, eightyfifth, eightyfive');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'eightfive, eightfiveth, eightyfifth, eightyfive', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('eightfour, eightfourth, eightyfour, eightyfourth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'eightfour, eightfourth, eightyfour, eightyfourth', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('eightieth, eighty, eightzero, eightzeroth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'eightieth, eighty, eightzero, eightzeroth', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('eightnine, eightnineth, eightynine, eightyninth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'eightnine, eightnineth, eightynine, eightyninth', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('eightone, eightonest, eightyfirst, eightyone');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'eightone, eightonest, eightyfirst, eightyone', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('eightseven, eightseventh, eightyseven, eightyseventh');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'eightseven, eightseventh, eightyseven, eightyseventh', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('eightsix, eightsixth, eightysix, eightysixth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'eightsix, eightsixth, eightysix, eightysixth', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('eightwo, eightwond, eightysecond, eightytwo');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'eightwo, eightwond, eightysecond, eightytwo', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('elder, geriatric, retire, senior');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'elder, geriatric, retire, senior', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('elevate, lift');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'elevate, lift', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('elic, elis');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'elic, elis', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('emigrate, immigrate, visa');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'emigrate, immigrate, visa', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('encore, oncor');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'encore, oncor', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('english, esl, interpret, language, translate');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'english, esl, interpret, language, translate', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('equestrian, equine, hors, rid');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'equestrian, equine, hors, rid', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('equip, implement, tractor');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'equip, implement, tractor', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('erwin, irwin');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'erwin, irwin', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('esix, esx, sx');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'esix, esx, sx', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('euro, uro');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'euro, uro', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('ewe, yew, you');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'ewe, yew, you', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('exhaust, muffler');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'exhaust, muffler', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('export, import, impx, imx, trade, trading, xim');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'export, import, impx, imx, trade, trading, xim', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('exterminate, fumigate, pest');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'exterminate, fumigate, pest', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('extreme, xstream, xtreme');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'extreme, xstream, xtreme', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('fantasy, phantasy');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'fantasy, phantasy', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('fastfood, takeout');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'fastfood, takeout', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('father, fr');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'father, fr', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('feed, grain, hay, petfood');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'feed, grain, hay, petfood', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('fenix, feonix, pheonix, phoenix');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'fenix, feonix, pheonix, phoenix', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('fiber, fibre');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'fiber, fibre', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('filipino, philipino');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'filipino, philipino', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('fire, fyr');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'fire, fyr', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('first, one, onest');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'first, one, onest', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('fitter, install, layer, laying');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'fitter, install, layer, laying', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('flag, traffic');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'flag, traffic', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('flair, flare');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'flair, flare', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('foam, insulate, spray');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'foam, insulate, spray', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('footbal, soccer');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'footbal, soccer', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('for, four, fourth, iv');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'for, four, fourth, iv', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('forest, forestry, log, lumber, mill, paper, ply, precut, pulp, reman, salvage, saw, timber, wood');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'forest, forestry, log, lumber, mill, paper, ply, precut, pulp, reman, salvage, saw, timber, wood', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('forester, forestmanager, forestry, reforest, silviculture, timbermanager, treeplant');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'forester, forestmanager, forestry, reforest, silviculture, timbermanager, treeplant', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('fort, ft');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'fort, ft', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('fraeme, frame');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'fraeme, frame', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('fraiser, fraser, frazer');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'fraiser, fraser, frazer', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('fruit, orchard, produce, sabzi, vegetable, vegi');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'fruit, orchard, produce, sabzi, vegetable, vegi', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('fungi, fungus, mushroom, mycology');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'fungi, fungus, mushroom, mycology', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('fushion, fusion');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'fushion, fusion', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('gaea, gaia');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'gaea, gaia', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('gail, gale, gayle');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'gail, gale, gayle', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('galley, kitchen');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'galley, kitchen', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('game, play, puzle, toy');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'game, play, puzle, toy', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('garden, gardener, grass, greenhouse, ground, horticulture, hydroponic, landscape, lawn, mow, nursery, plant, sod, succulent, turf, xeriscape, yard');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'garden, gardener, grass, greenhouse, ground, horticulture, hydroponic, landscape, lawn, mow, nursery, plant, sod, succulent, turf, xeriscape, yard', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('genesis, genesys, genisis');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'genesis, genesys, genisis', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('geoff, jeff');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'geoff, jeff', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('gerry, gery, jerry, jery');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'gerry, gery, jerry, jery', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('glass, glaze, mirror, shower, window, windshield');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'glass, glaze, mirror, shower, window, windshield', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('glide, soar');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'glide, soar', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('glider, sailplane');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'glider, sailplane', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('goar, gore');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'goar, gore', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('gofer, gopher');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'gofer, gopher', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('goru, guru');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'goru, guru', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('governor, guvnor');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'governor, guvnor', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('grace, grayce');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'grace, grayce', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('graeme, graham');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'graeme, graham', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('gray, grey');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'gray, grey', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('griffin, griffon, grifin, gryphon');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'griffin, griffon, grifin, gryphon', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('h20, htwo, spring, water');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'h20, htwo, spring, water', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('hai, hi, high, hy');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'hai, hi, high, hy', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('haidaway, hideaway');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'haidaway, hideaway', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('harbor, harbour');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'harbor, harbour', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('hart, heart');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'hart, heart', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('haus, house');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'haus, house', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('hawg, hog');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'hawg, hog', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('health, medic, practice, surgery, wellness');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'health, medic, practice, surgery, wellness', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('height, hite');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'height, hite', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('hics, hix');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'hics, hix', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('highland, hiland, hyland');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'highland, hiland, hyland', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('hightech, hitec, hytec');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'hightech, hitec, hytec', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('hightek, hitec, hytek');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'hightek, hitec, hytek', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('highway, hiway, hwy, hyway');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'highway, hiway, hwy, hyway', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('hire, lease, rent');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'hire, lease, rent', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('hldg, hold, holdco, holding');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'hldg, hold, holdco, holding', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('hundredth, onehundred, onehundredth, onezerozeroth, onezerzero');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'hundredth, onehundred, onehundredth, onezerozeroth, onezerzero', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('institute, school, training');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'institute, school, training', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('international, intl');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'international, intl', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('irrigate, sprinkler, watering, watersystem');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'irrigate, sprinkler, watering, watersystem', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('isis, isys');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'isis, isys', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('island, isle');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'island, isle', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('ix, nine, nineth, ninth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'ix, nine, nineth, ninth', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('jaemar, jaymar');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'jaemar, jaymar', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('jantsen, jantzen, janzen');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'jantsen, jantzen, janzen', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('jetwash, powerclean, powerwash, pressure, steam, wash');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'jetwash, powerclean, powerwash, pressure, steam, wash', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('johal, johel');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'johal, johel', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('john, jon');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'john, jon', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('johnny, jonny');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'johnny, jonny', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('johnson, johnston, jonson');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'johnson, johnston, jonson', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('karma, kharma');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'karma, kharma', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('keyboard, organ, piano, synthesizer');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'keyboard, organ, piano, synthesizer', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('kwality, quality');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'kwality, quality', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('kwantem, quantum');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'kwantem, quantum', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('lam, lamb');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'lam, lamb', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('landsdowne, lansdowne');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'landsdowne, lansdowne', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('lathe, plaster, stucco');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'lathe, plaster, stucco', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('laura, lora');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'laura, lora', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('laurel, lorel');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'laurel, lorel', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('lay, le, lea, lei, leigh, ly');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'lay, le, lea, lei, leigh, ly', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('leach, lech');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'leach, lech', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('lear, leer');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'lear, leer', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('lewis, louis');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'lewis, louis', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('lidle, lil, litle, lytle');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'lidle, lil, litle, lytle', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('linda, lynda');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'linda, lynda', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('link, links, linx, lynx');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'link, links, linx, lynx', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('lion, lyon');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'lion, lyon', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('load, lode');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'load, lode', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('lottery, lotto, sweepstake');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'lottery, lotto, sweepstake', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('love, luv');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'love, luv', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('magic, majic, majix');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'magic, majic, majix', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('magnem, magnum');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'magnem, magnum', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('main, maine, mayne');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'main, maine, mayne', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('mama, moma');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'mama, moma', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('manage, management, mgmt, mgr, mgt');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'manage, management, mgmt, mgr, mgt', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('manufactur, mfg');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'manufactur, mfg', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('manufacturedhome, mobilehome, modularhome, prefab');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'manufacturedhome, mobilehome, modularhome, prefab', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('marcs, marx');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'marcs, marx', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('marketer, marketing, mct');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'marketer, marketing, mct', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('meridian, meridien');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'meridian, meridien', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('midas, midys');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'midas, midys', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('mile, myle');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'mile, myle', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('minit, minut');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'minit, minut', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('miser, mizer');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'miser, mizer', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('mister, mr');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'mister, mr', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('misus, mrs');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'misus, mrs', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('miter, mitre, myter');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'miter, mitre, myter', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('mohr, more');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'mohr, more', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('monro, munro');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'monro, munro', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('mount, mt, mtn');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'mount, mt, mtn', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('natural, organic');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'natural, organic', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('neu, new, nieu, nu');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'neu, new, nieu, nu', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('newest, nuwest, nw');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'newest, nuwest, nw', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('ninefive, ninefiveth, ninetyfifth, ninetyfive');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'ninefive, ninefiveth, ninetyfifth, ninetyfive', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('ninefour, ninefourth, ninetyfour, ninetyfourth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'ninefour, ninefourth, ninetyfour, ninetyfourth', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('ninenine, ninenineth, ninetynine, ninetyninth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'ninenine, ninenineth, ninetynine, ninetyninth', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('nineone, nineonest, ninetyfirst, ninetyone');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'nineone, nineonest, ninetyfirst, ninetyone', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('nineseven, nineseventh, ninetyseven, ninetyseventh');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'nineseven, nineseventh, ninetyseven, ninetyseventh', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('ninesix, ninesixth, ninetysix, ninetysixth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'ninesix, ninesixth, ninetysix, ninetysixth', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('ninetieth, ninety, ninezero, ninezeroth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'ninetieth, ninety, ninezero, ninezeroth', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('ninetwo, ninetwond, ninetysecond, ninetytwo');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'ninetwo, ninetwond, ninetysecond, ninetytwo', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('no, number');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'no, number', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('nouveau, nuvo');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'nouveau, nuvo', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('odysea, odysey');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'odysea, odysey', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('olsen, olson');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'olsen, olson', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('pace, paice, payce');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'pace, paice, payce', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('pairadice, paradise');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'pairadice, paradise', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('part, wrec');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'part, wrec', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('peac, pec, pece, pique');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'peac, pec, pece, pique', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('pearce, pierce');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'pearce, pierce', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('pege, pg, princegeorge');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'pege, pg, princegeorge', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('persepolis, persopolis');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'persepolis, persopolis', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('phase, phaze');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'phase, phaze', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('philatelic, philately, stamp');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'philatelic, philately, stamp', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('pic, pyc');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'pic, pyc', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('planet, planit');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'planet, planit', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('poco, port coquitlam');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'poco, port coquitlam', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('point, pt');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'point, pt', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('pointofsale, pos, register');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'pointofsale, pos, register', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('portocal, portofcal');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'portocal, portofcal', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('post trauma, ptsd');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'post trauma, ptsd', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('price, pryce');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'price, pryce', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('prime, pryme');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'prime, pryme', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('principal, principle');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'principal, principle', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('profit, prophet');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'profit, prophet', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('pumpkin, punkin');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'pumpkin, punkin', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('qc, quencharlote');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'qc, quencharlote', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('quail, quayle');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'quail, quayle', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('quesnel, quinel');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'quesnel, quinel', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('rae, rai, ray');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'rae, rai, ray', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('rain, raine, rayne, reign, rein');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'rain, raine, rayne, reign, rein', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('rainbow, raynbow');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'rainbow, raynbow', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('read, red, reid');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'read, red, reid', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('recover, rescue, tow');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'recover, rescue, tow', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('reimer, rhymer, rimer, rymer');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'reimer, rhymer, rimer, rymer', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('right, rite, wright, write');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'right, rite, wright, write', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('rise, rize');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'rise, rize', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('robin, robyn');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'robin, robyn', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('roe, row');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'roe, row', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('rof, shace, shingle');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'rof, shace, shingle', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('rough, ruff');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'rough, ruff', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('rubber, tire, tyre');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'rubber, tire, tyre', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('saber, sabre');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'saber, sabre', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('saddle, tack');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'saddle, tack', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('saint, st, street');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'saint, st, street', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('sampson, samson');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'sampson, samson', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('sandalwood, sandlewood');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'sandalwood, sandlewood', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('savor, savour');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'savor, savour', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('scale, weigh');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'scale, weigh', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('scene, sen, son, sun');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'scene, sen, son, sun', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('schaefer, shaefer, shafer');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'schaefer, shaefer, shafer', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('seagul, segal, siegal, siegel');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'seagul, segal, siegal, siegel', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('sean, shaun, shawn, shon');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'sean, shaun, shawn, shon', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('second, two, twond');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'second, two, twond', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('serious, sirius');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'serious, sirius', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('seumas, sumas');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'seumas, sumas', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('seven, seventh');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'seven, seventh', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('seveneight, seveneighth, seventyeight, seventyeighth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'seveneight, seveneighth, seventyeight, seventyeighth', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('sevenfive, sevenfiveth, seventyfifth, seventyfive');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'sevenfive, sevenfiveth, seventyfifth, seventyfive', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('sevenine, sevenineth, seventynine, seventyninth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'sevenine, sevenineth, seventynine, seventyninth', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('sevenseven, sevenseventh, seventyseven, seventyseventh');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'sevenseven, sevenseventh, seventyseven, seventyseventh', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('sevensix, sevensixth, seventysix, seventysixth');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'sevensix, sevensixth, seventysix, seventysixth', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('sfu, simonfraseruniversity');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'sfu, simonfraseruniversity', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('sharen, sharon');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'sharen, sharon', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('shay, shea');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'shay, shea', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('shear, sher, shur, sur, sure');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'shear, sher, shur, sur, sure', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('sincoloid, syncoloid');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'sincoloid, syncoloid', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('soce, tsouce');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'soce, tsouce', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('sol, sole, soul');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'sol, sole, soul', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('somer, sumer');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'somer, sumer', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('sonshine, sunshine');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'sonshine, sunshine', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('spartan, sparton');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'spartan, sparton', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('stephen, steven');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'stephen, steven', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('sterling, stirling');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'sterling, stirling', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('stewart, stuart');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'stewart, stuart', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('straight, strait, strate');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'straight, strait, strate', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('strice, stryce');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'strice, stryce', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('sulfur, sulphur');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'sulfur, sulphur', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('team, teem');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'team, teem', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('telerad, telrad');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'telerad, telrad', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('teresa, theresa');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'teresa, theresa', TRUE);
SELECT PG_SLEEP(0.001);

INSERT INTO synonym (synonyms_text) VALUES ('thom, tom');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'thom, tom', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('thompson, thomson, tomson');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'thompson, thomson, tomson', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('through, thru');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'through, thru', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('thyme, time, tyme');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'thyme, time, tyme', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('tough, tuff');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'tough, tuff', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('treat, treit, tret');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'treat, treit, tret', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('tri, try');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'tri, try', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('triad, tryad');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'triad, tryad', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('ubc, ubysey, universitybritishcolumbia');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'ubc, ubysey, universitybritishcolumbia', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('unec, unique');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'unec, unique', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('universityvictoria, uvic');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'universityvictoria, uvic', TRUE);
SELECT PG_SLEEP(0.003);

INSERT INTO synonym (synonyms_text) VALUES ('userexerience, ux');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'userexerience, ux', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('vale, valey, valy');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'vale, valey, valy', TRUE);
SELECT PG_SLEEP(0.009);

INSERT INTO synonym (synonyms_text) VALUES ('vancouverisland, vanisle, vi');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'vancouverisland, vanisle, vi', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('view, vu');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'view, vu', TRUE);
SELECT PG_SLEEP(0.002);

INSERT INTO synonym (synonyms_text) VALUES ('virtual, vr');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'virtual, vr', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('walace, walis, wallace, wallis');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'walace, walis, wallace, wallis', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('weatherb, weatherby');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'weatherb, weatherby', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('werc, werk, werx, worc, work, worx');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'werc, werk, werx, worc, work, worx', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('wesix, wesx');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'wesix, wesx', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('white, whyte');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'white, whyte', TRUE);
SELECT PG_SLEEP(0.008);

INSERT INTO synonym (synonyms_text) VALUES ('why, wi');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'why, wi', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('whyld, whylde, wild, wilde, wyld, wylde');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'whyld, whylde, wild, wilde, wyld, wylde', TRUE);
SELECT PG_SLEEP(0.007);

INSERT INTO synonym (synonyms_text) VALUES ('win, wyn');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'win, wyn', TRUE);
SELECT PG_SLEEP(0.005);

INSERT INTO synonym (synonyms_text) VALUES ('wind, wynd');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'wind, wynd', TRUE);
SELECT PG_SLEEP(0.006);

INSERT INTO synonym (synonyms_text) VALUES ('wise, wyse');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'wise, wyse', TRUE);
SELECT PG_SLEEP(0.004);

INSERT INTO synonym (synonyms_text) VALUES ('zed, zee');
INSERT INTO synonym_audit (synonym_id, username, action, synonyms_text, enabled) VALUES ((SELECT last_value FROM synonym_id_seq), 'INITIALIZATION', 'CREATE', 'zed, zee', TRUE);
SELECT PG_SLEEP(0.006);
