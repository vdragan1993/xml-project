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
        utils.clean_xml_file(file_location)
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


def text_search(text):
    """
    Performs text search on MarkLogic database.
    :param text: query
    :return: list of document uri
    """
    url = db.DATABASE_URL + "search?q=" + text + "&database=Tim20"
    headers = {'Accept': 'text/xml'}
    response = requests.get(url, headers=headers, auth=HTTPDigestAuth(db.DATABASE_USER, db.DATABASE_PASS))
    result = response.content.decode('utf8')
    return utils.parse_search_results(result)


def advanced_search(attribute, value):
    """
    Performs advanced search for one attribute and value.
    :param attribute: attribute
    :param value: value
    :return: list of act uri
    """
    uris = utils.get_uries_from_content()
    ret_val = []
    for uri in uris:
        file_path = get_document_from_uri(uri)
        if utils.contains_metadata(file_path, attribute, value):
            ret_val.append(uri)
        utils.remove_existing_file(file_path)
    return ret_val


def advanced_search_list(attributes, values, operator):
    """
    Performs advanced search on list of attribute-value pairs.
    :param attributes: list of attributes
    :param values: list of values
    :param operator: AND - OR
    :return: list of act uri
    """
    uris = utils.get_uries_from_content()
    ret_val = {}
    for uri in uris:
        ret_val[uri] = 0

    for i in range(0, len(attributes)):
        this_results = advanced_search(attributes[i], values[i])
        for result in this_results:
            ret_val[result] += 1

    total_results = []
    if operator == 'AND':
        for k, v in ret_val.items():
            if v == len(attributes):
                total_results.append(k)
    elif operator == 'OR':
        for k, v in ret_val.items():
            if v > 0:
                total_results.append(k)

    return total_results