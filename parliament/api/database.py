import parliament.settings as db
import api.utils as utils
import requests
from requests.auth import HTTPDigestAuth


"""
CRUD operations
"""


def insert_document_from_file(filepath, collection):
    """
    Inserts file from given file path into given collection
    :param filepath: path to xml file
    :param collection: usvojeniakti, procesakti, usvojeniamandmani, procesamandmani
    """
    file_name = utils.get_file_name(filepath) + ".xml"
    doc_uri = collection + "/" + file_name
    if utils.exists_in_content(doc_uri):
        print("File {0} already exists into database!".format(doc_uri))
        return

    f = open(filepath, "rb")
    data = f.read()
    f.close()
    insert_document(data, doc_uri, collection)


def insert_document_from_string(file_name, collection, string):
    """
    Inserts given strings under given file name into given collection
    :param file_name: file name
    :param collection: usvojeniakti, procesakti, usvojeniamandmani, procesamandmani
    :param string: xml string
    :return: True or False
    """
    doc_uri = collection + "/" + file_name
    if utils.exists_in_content(doc_uri):
        print("File {0} already exists into database".format(doc_uri))
        return

    insert_document(string, doc_uri, collection)


def insert_document(data, doc_uri, collection):
    """
    MarkLogic REST insert xml document
    :param data: xml data
    :param doc_uri: document uri
    :param collection: collection name
    """
    url = db.DATABASE_URL + "documents?uri=/" + doc_uri + "&database=Tim20&collection="+collection
    headers = {'Content-Type': 'text/xml', 'charset': 'utf-8'}
    response = requests.put(url, data=data, headers=headers, auth=HTTPDigestAuth(db.DATABASE_USER, db.DATABASE_PASS))
    if 200 <= response.status_code < 300:
        print("File {0} successfully inserted into database!".format(doc_uri))
        utils.write_to_content(doc_uri)
        return
    else:
        print("Error during inserting {0} into database!".format(doc_uri))
        return


def get_document(file_name, collection):
    """
    Gets xml document and save it in download/file_name
    :param file_name: xml file name
    :param collection:
    :return: downloaded file location
    """
    doc_uri = collection + "/" + file_name
    return get_document_from_uri(doc_uri)


def get_document_from_uri(doc_uri):
    """
    MarkLogic REST get xml document from given document uri and save it in download/file_name
    :param doc_uri: document uri
    :return: downloaded file location
    """
    url = db.DATABASE_URL + "documents?uri=/" + doc_uri + "&database=Tim20"
    headers = {'Accept': 'text/html', 'charset': 'utf-8'}
    response = requests.get(url, headers=headers, auth=HTTPDigestAuth(db.DATABASE_USER, db.DATABASE_PASS))
    if 200 <= response.status_code < 300:
        print("File {0} successfully get from database!".format(doc_uri))
        file_location = "download/" + utils.get_file_name(doc_uri) + ".xml"
        f = open(file_location, "wb")
        f.write(response.content)
        f.close()
        return file_location
    else:
        print("Error during getting {0} from database!".format(doc_uri))
        return None


def delete_document(file_name, collection):
    """
    Deletes xml document with given file name from given collection
    :param file_name: file name
    :param collection: database collection
    """
    doc_uri = collection + "/" + file_name
    delete_document_from_uri(doc_uri)


def delete_document_from_uri(doc_uri):
    """
    MarkLogic REST delete xml document from given document uri
    :param doc_uri: document uri
    """
    url = db.DATABASE_URL + "documents?uri=/" + doc_uri + "&database=Tim20"
    response = requests.delete(url, auth=HTTPDigestAuth(db.DATABASE_USER, db.DATABASE_PASS))
    if 200 <= response.status_code < 300:
        print("File {0} successfully deleted!".format(doc_uri))
        utils.delete_from_content(doc_uri)
        return
    else:
        print("Error during deleting {0} from database!".format(doc_uri))
        return


def update_document_from_file_uri(file_path, doc_uri):
    """
    Updates file on give uri with file from given path
    :param file_path: path to xml file
    :param doc_uri: document uri
    """
    f = open(file_path, "rb")
    data = f.read()
    f.close()
    update_document(data, doc_uri)


def update_document_from_string_uri(string, doc_uri):
    """
    Updates file on give uri with given string
    :param string: xml file string
    :param doc_uri: document uri
    """
    update_document(string, doc_uri)


def update_document_from_file(file_path, update_name, collection):
    """
    Updates file with given update name in given collection with file from given path
    :param file_path: path to xml file
    :param update_name: update file name
    :param collection: collection name
    """
    doc_uri = collection + "/" + update_name
    update_document_from_file_uri(file_path, doc_uri)


def update_document_from_string(string, update_name, collection):
    """
    Updates file with given update name in given collection with given string
    :param string:
    :param update_name:
    :param collection:
    :return:
    """
    doc_uri = collection + "/" + update_name
    update_document_from_string_uri(string, doc_uri)


def update_document(data, doc_uri):
    """
    MarkLogic REST update xml document
    :param data: xml data
    :param doc_uri: document uri
    """
    url = db.DATABASE_URL + "documents?uri=/" + doc_uri + "&database=Tim20"
    headers = {'Content-Type': 'text/xml', 'charset': 'utf-8'}
    response = requests.put(url, data=data, headers=headers, auth=HTTPDigestAuth(db.DATABASE_USER, db.DATABASE_PASS))
    if 200 <= response.status_code < 300:
        print("File {0} successfully updated!".format(doc_uri))
        return
    else:
        print("Error during updating {0}!".format(doc_uri))
