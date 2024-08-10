CREATE TABLE IF NOT EXISTS `warns` (
  `id` int(11) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `moderator_id` varchar(20) NOT NULL,
  `reason` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `maple_mob` (
  `id` int(11) NOT NULL PRIMARY KEY,
  `name` varchar(20) NOT NULL,
  `mobType` varchar(2),
  `level` int(11),
  `isBoss` boolean,
  `isBodyAttack` boolean,
  `maxHP` int(11),
  `speed` int(11),
  `physicalDamage` int(11),
  `magicDamage` int(11),
  `accuracy` int(11),
  `evasion` int(11),
  `exp` int(11),
  `isAutoAggro` boolean
);

CREATE TABLE IF NOT EXISTS `maple_mob_map` (
  `mob_id` int(11) NOT NULL,
  `map_id` varchar(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS `maple_map` (
  `id` int(11) NOT NULL PRIMARY KEY,
  `name` varchar(20) NOT NULL,
  `streetName` varchar(20)
);