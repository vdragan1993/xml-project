from lxml import etree, objectify
from lxml.etree import XMLSyntaxError
import os
from xhtml2pdf import pisa
import io


# location of xsd
xsd_act = 'api/schema/XML_Proj_schema_act.xsd'
xsd_amendment = 'api/schema/XML_Proj_schema_amandman.xsd'


def validate_document(xml_doc_string, doc_type='amendment'):
    """
    Validates act or amendment with a XML schema
    :param xml_doc_string: XML string of an act or amendment, UTF-8 encoded
    :param doc_type: act or amendment
    :return: True or False
    """
    xsd_schema = xsd_amendment
    if doc_type == 'act':
        xsd_schema = xsd_act

    try:
        schema = etree.XMLSchema(file=xsd_schema)
        parser = objectify.makeparser(schema=schema)
        objectify.fromstring(xml_doc_string, parser)
        return True
    except XMLSyntaxError:
        return False
        pass


def get_file_name(path):
    """
    Extracts name of file from given path
    :param path: file path
    :return: file name with extension
    """
    if "/" in path:
        partials = path.split("/")
        return partials[len(partials) - 1].split(".")[0]
    else:
        return path.split(".")[0]


def remove_existing_file(path):
    """
    Removes file from given path, if exists
    :param path: file path
    """
    try:
        os.remove(path)
        print("Removed file: " + path)
    except:
        print(path + " does not exist")
        pass


xsl_amendment_html = 'api/transformations/amendment.xsl'
xsl_amendment_pdf = 'api/transformations/amendment_pdf.xsl'
xsl_act_html = 'api/transformations/Akt.xsl'
xsl_act_pdf = 'api/transformations/Akt_pdf.xsl'


def transform_document_to_html(xml_file_path, doc_type='amendment'):
    """
    Transforms given xml file to html and places it in generate/html folder
    :param xml_file_path: path to xml file
    :param doc_type: act or amendment
    :return: path to generated file
    """
    xml_file_name = get_file_name(xml_file_path)
    destination_path = 'api/generate/html/' + xml_file_name + ".html"
    remove_existing_file(destination_path)

    xsl_file = xsl_amendment_html
    if doc_type == 'act':
        xsl_file = xsl_act_html

    dom = etree.parse(xml_file_path)
    xslt = etree.parse(xsl_file)
    transform = etree.XSLT(xslt)
    new_dom = transform(dom)
    result = etree.tostring(new_dom, pretty_print=True)
    f = open(destination_path, "wb")
    f.write(result)
    f.close()
    print("File {0} generated successfully!".format(destination_path))
    return destination_path


css_amendment = "@page{size:a4 portrait; margin: 2cm;}"
css_act = "@page{size:a4 portrait; margin: 2cm;}"


def convert_xhtml_to_pdf(xhtml_string, destination_file, document_type='amendment'):
    """
    Converts given xhtml string to PDF.
    :param xhtml_string: xhtml string
    :param destination_file: pdf file location
    :return: convertion status (0 - no errors)
    """
    result_file = open(destination_file, "w+b")
    css = css_amendment
    if document_type == 'act':
        css = None

    pisa_status = pisa.CreatePDF(xhtml_string, dest=result_file, default_css=css, encoding='utf-8')
    result_file.close()
    print("File {0} generated successfully!".format(destination_file))
    return pisa_status.err


def transform_document_to_pdf(xml_file_path, doc_type='amendment'):
    """
    Transforms given xml file to html and places it in generate/pdf folder
    :param xml_file_path: path to xml file
    :param doc_type: act or amendment
    :return: path to generated file
    """
    xml_file_name = get_file_name(xml_file_path)
    destination_path = 'api/generate/pdf/' + xml_file_name + ".pdf"
    remove_existing_file(destination_path)

    xsl_file = xsl_amendment_pdf
    if doc_type == 'act':
        xsl_file = xsl_act_pdf

    dom = etree.parse(xml_file_path)
    xslt = etree.parse(xsl_file)
    transform = etree.XSLT(xslt)
    new_dom = transform(dom)
    result = etree.tostring(new_dom, pretty_print=True)
    convert_xhtml_to_pdf(result, destination_path, document_type=doc_type)
    return destination_path


def exists_in_content(doc_uri):
    """
    Check if document already exists in database
    :param doc_uri: document name and collection
    :return: True or False
    """
    f = open("api/data/content.txt", "r")
    lines = f.readlines()
    f.close()
    for line in lines:
        line = line[:-1]
        if line == doc_uri:
            return True
    return False


def write_to_content(doc_uri):
    """
    Add document uri in list of existing documents in database
    :param doc_uri: document name and collection
    """
    f = open("api/data/content.txt", "a")
    line = doc_uri + "\n"
    f.write(line)
    f.close()


def delete_from_content(doc_uri):
    """
    Remove document uri from list of existing documents in database
    :param doc_uri: document name and collection
    """
    f = open("api/data/content.txt", "r")
    lines = f.readlines()
    f.close()

    f = open("api/data/content.txt", "w")
    for line in lines:
        line = line[:-1]
        if line != doc_uri:
            write_to_content(line)
    f.close()


def clean_xml_file(file_path):
    """
    Cleans unnecessary encoding data from xml file header
    :param file_path: file path
    :return: clean file
    """
    f = open(file_path, "r", encoding='utf8')
    lines = f.readlines()
    f.close()
    lines[0] = '<?xml version="1.0"?>\n'
    f = open(file_path, "w", encoding='utf8')
    f.writelines(lines)
    f.close()


def parse_search_results(result):
    """
    Parses xml result of search and returns list of result uri.
    :param result: result xml
    :return: list of uri
    """
    result_content = io.StringIO(result)
    result_dom = etree.parse(result_content)
    uris = result_dom.xpath('//search:result/@uri', namespaces={'search': 'http://marklogic.com/appservices/search'})
    ret_val = []
    for uri in uris:
        ret_val.append(uri[1:])
    return ret_val


def uri_reader(uri_string):
    """
    Extracts name, collection, type and status of document based on its uri.
    :param uri_string: document uri
    :return: name, collection, doc_type, status
    """
    name = uri_string.split("/")[1]
    collection = uri_string.split("/")[0]
    doc_type = 'amandman'
    if 'akt' in uri_string:
        doc_type = 'akt'
    status = 'proces'
    if 'usvojen' in uri_string:
        status = 'usvojen'
    return name, collection, doc_type, status


def get_uries_from_content():
    """
    Returns all act uries from database.
    :return: list of act uries
    """
    f = open('api/data/content.txt', 'r')
    lines = f.readlines()
    f.close()
    ret_val = []
    for line in lines:
        line = line[:-1]
        name, collection, doc_type, status = uri_reader(line)
        if doc_type == 'akt':
            ret_val.append(line)
    return ret_val


def contains_metadata(file_path, metadata, value):
    """
    Checks if file at given path contains given metadata with given value
    :param file_path: file path
    :param metadata: metadata attribute
    :param value: metadata value
    :return: True or False
    """
    f = open(file_path, 'rb')
    f_data = f.read().decode('utf8')
    f_content = io.StringIO(f_data)
    f_dom = etree.parse(f_content)
    real_value = f_dom.xpath("/*/@" + metadata)
    if len(real_value) > 0:
        return real_value[0] == value
    else:
        return False


def read_metadata(string, metadata):
    """
    Reads attribute value from given string
    :param string: xml doc
    :param metadata: attribute
    :return: metadata value
    """
    content = io.StringIO(string)
    dom = etree.parse(content)
    return dom.xpath("/*/@" + metadata)[0]


def read_metadata_from_file(file_path, metadata):
    """
    Reads attribute value from given file
    :param file_path: xml doc path
    :param metadata: attribute
    :return: metadata value
    """
    file = open(file_path, 'rb')
    file_data = file.read().decode("utf8")
    return read_metadata(file_data, metadata)


def set_metadata_to_file(file_path, metadata, value):
    """
    Sets attribute value from given file
    :param file_path: xml doc path
    :param metada: attribute
    """
    file = open(file_path, 'rb')
    file_data = file.read().decode("utf8")
    return set_metadata(file_data, metadata, value)


def set_metadata(string, metadata, value):
    """
    Sets attribute value from given value
    :param string: xml doc
    :param metadata: attribute
    :param value: new attribute value
    :return: new xml doc
    """
    content = io.StringIO(string)
    dom = etree.parse(content)
    root_tag = dom.xpath('//b:amandman', namespaces={'b': 'https://ftn.uns.ac.rs/xml'})[0]
    root_tag.set(metadata, value)
    new_content = etree.tostring(dom, pretty_print=True)
    return new_content.decode("utf-8")


def get_proponent_for_user(username):
    """
    For every given username, returns proponent uri
    :param username: given username
    :return: list of uris
    """
    f = open("api/data/proponent.txt", "r")
    lines = f.readlines()
    f.close()
    ret_val = []
    for line in lines:
        line = line[:-1]
        if line.split(',')[1] == username:
            ret_val.append(line.split(',')[0])
    return ret_val


def get_all_proponents():
    """
    List all not accepted docs
    :return: list of uris
    """
    f = open("api/data/proponent.txt", "r")
    lines = f.readlines()
    f.close()
    ret_val = []
    for line in lines:
        this_uri = line.split(",")[0]
        ret_val.append(this_uri)
    return ret_val


def insert_proponent(uri, username):
    """
    For every inserted act or amendment, inserts into proponent statistics
    :param uri: doc uri
    :param username: given username
    """
    f = open("api/data/proponent.txt", "r")
    lines = f.readlines()
    f.close()
    new_line = uri + "," + username + "\n"
    lines.append(new_line)
    f = open("api/data/proponent.txt", "w")
    f.writelines(lines)
    f.close()


def delete_proponent(uri):
    """
    Deletes uri from proponent statistics
    :param uri: doc uri
    """
    f = open("api/data/proponent.txt", "r")
    lines = f.readlines()
    f.close()
    new_lines = []
    for line in lines:
        this_uri = line.split(",")[0]
        if this_uri != uri:
            new_lines.append(line)
    f = open("api/data/proponent.txt", "w")
    f.writelines(new_lines)
    f.close()


def extract_parent_act(uri):
    """
    Extracts parent act uri
    :param uri: given uri
    :return: uri
    """
    parts = uri.split("?uri=")[1]
    parts = parts[1:]
    return parts.split('&')[0]


def write_conference(string):
    """
    Writes conference data to file
    :param string: conference data
    """
    f = open('api/data/conference.txt', "a")
    f.write(string)
    f.close()