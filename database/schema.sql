create table channel
(
    id    integer not null
        primary key autoincrement,
    title text    not null,
    url   text    not null
);

create table item
(
    title            text    not null,
    guid             text    not null,
    link             text,
    description      text,
    publication_date datetime,
    channel_id       int     not null
        references channel
            on update cascade on delete cascade,
    id               integer not null
        constraint item_pk
            primary key autoincrement,
    constraint per_channel_key
        unique (guid, channel_id)
);

create index channel_id_index
    on item (channel_id);

create unique index item_id_uindex
    on item (id);
