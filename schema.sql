drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  tinyurl text not null,
  pic text not null,
  qrcode text not null,
);