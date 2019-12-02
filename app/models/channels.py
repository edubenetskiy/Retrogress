from datetime import datetime
from email.utils import parsedate_to_datetime

import requests
from bs4 import BeautifulSoup

from app import get_db


class Channel:
    id: int
    title: str
    url: str

    def update_items(self):
        items = fetch_items(self.url)
        connection = get_db()
        cursor = connection.cursor()
        for item in items:
            cursor.execute(
                "insert or ignore "
                "into item (title, guid, link, description, publication_date, channel_id) "
                "values (?, ?, ?, ?, ?, ?)",
                (item.title, item.guid, item.link, item.description, item.publication_date, self.id))
        cursor.close()
        connection.commit()

    def find_all_items(self):
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute(
            "select title, guid, link, description, publication_date "
            "from item "
            "where item.channel_id = ?",
            (self.id,))
        rows = cursor.fetchall()

        items = []
        for row in rows:
            item = Item()
            item.title = row[0]
            item.guid = row[1]
            item.link = row[2]
            item.description = row[3]
            item.publication_date = datetime.fromisoformat(row[4])
            item.channel_id = self.id
            items.append(item)
        return items


def find_all_channels():
    cur = get_db().cursor()
    cur.execute("select id, title, url from channel")
    rows = cur.fetchall()
    cur.close()

    channels = []
    for row in rows:
        channel = Channel()
        channel.id = row[0]
        channel.title = row[1]
        channel.url = row[2]
        channels.append(channel)

    return channels


def find_channel_by_id(channel_id) -> Channel:
    cur = get_db().cursor()
    cur.execute("select id, title, url from channel where channel.id = ?", (channel_id,))
    row = cur.fetchone()
    cur.close()

    channel = Channel()
    channel.id = row[0]
    channel.title = row[1]
    channel.url = row[2]

    return channel


def insert_new_channel(title, url) -> Channel:
    connection = get_db()
    cur = connection.cursor()
    cur.execute("insert into channel (title, url) values (?, ?)", (title, url))
    channel_id = cur.lastrowid
    cur.close()
    connection.commit()

    channel = Channel()
    channel.id = channel_id
    channel.title = title
    channel.url = url

    return channel


class Item:
    title: str
    guid: str
    link: str
    description: str
    publication_date: datetime
    channel_id: int


def convert_xml_to_item(xml_object) -> Item:
    item = Item()
    item.title = xml_object.title.text
    item.guid = xml_object.guid.text
    item.link = xml_object.link.text
    item.description = xml_object.description.text
    item.publication_date = parsedate_to_datetime(xml_object.pubDate.text)
    return item


def fetch_definition(url):
    channel_xml = fetch_xml_definition_object(url)

    channel = Channel()
    channel.id = None
    channel.url = channel_xml.link.text
    channel.title = channel_xml.title.text

    return channel


class SubscriptionError(Exception):
    pass


class ProvidedUrlIsNotRss(SubscriptionError):
    pass


class ProvidedUrlUnreachable(SubscriptionError):
    pass


def fetch_xml_definition_object(url):
    try:
        definition_text = requests.get(url).text
    except requests.exceptions.RequestException as exception:
        raise ProvidedUrlUnreachable(f"The URL ‘{url}’ is unreachable") from exception

    soup = BeautifulSoup(definition_text, features="xml")
    if soup.rss and soup.rss.channel:
        channel_xml = soup.rss.channel
        return channel_xml
    else:
        raise ProvidedUrlIsNotRss(f"There is no RSS definition at URL ‘{url}’")


def fetch_items(url):
    channel_xml = fetch_xml_definition_object(url)
    xml_items = channel_xml.find_all('item')
    return [convert_xml_to_item(item) for item in xml_items]


def subscribe(url) -> Channel:
    channel_definition = fetch_definition(url)
    channel = insert_new_channel(title=channel_definition.title, url=url)
    channel.update_items()
    return channel


def delete_channel_and_its_items(channel_id):
    connection = get_db()
    cur = connection.cursor()
    cur.execute("delete from item where channel_id=?", (channel_id,))
    cur.execute("delete from channel where id=?", (channel_id,))
    cur.close()
    connection.commit()
    return None
