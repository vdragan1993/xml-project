from lxml import etree, objectify
from lxml.etree import XMLSyntaxError
import os
from xhtml2pdf import pisa
import io
from api.database import get_document_from_uri, update_document_from_string_uri


# location of xsd
xsd_act = 'schema/XML_Proj_schema_act.xsd'
xsd_amendment = 'schema/XML_Proj_schema_amandman.xsd'


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


xsl_amendment_html = 'transformations/amendment.xsl'
xsl_amendment_pdf = 'transformations/amendment_pdf.xsl'
xsl_act_html = 'transformations/Akt.xsl'
xsl_act_pdf = 'transformations/Akt_pdf.xsl'


def transform_document_to_html(xml_file_path, doc_type='amendment'):
    """
    Transforms given xml file to html and places it in generate/html folder
    :param xml_file_path: path to xml file
    :param doc_type: act or amendment
    :return: path to generated file
    """
    xml_file_name = get_file_name(xml_file_path)
    destination_path = 'generate/html/' + xml_file_name + ".html"
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

    pisa_status = pisa.CreatePDF(xhtml_string, dest=result_file, default_css=css)
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
    destination_path = 'generate/pdf/' + xml_file_name + ".pdf"
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
    f = open("data/content.txt", "r")
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
    f = open("data/content.txt", "a")
    line = doc_uri + "\n"
    f.write(line)
    f.close()


def delete_from_content(doc_uri):
    """
    Remove document uri from list of existing documents in database
    :param doc_uri: document name and collection
    """
    f = open("data/content.txt", "r")
    lines = f.readlines()
    f.close()

    f = open("data/content.txt", "w")
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


def accept_amendment(amendment_path, act_path, doc_uri):
    """
    Performs amendment operation on given act, and updates file in MarkLogic database.
    :param amendment_path: amendment file path
    :param act_path: act file path
    :param doc_uri: act uri
    """
    # amendment operations
    amendment_file = open(amendment_path, 'rb')
    amendment_data = amendment_file.read().decode("utf8")
    amendment_content = io.StringIO(amendment_data)
    amendment_dom = etree.parse(amendment_content)
    operation = amendment_dom.xpath('/*/@operacija')[0]
    target_article = amendment_dom.xpath('/*/@clanId')[0]
    # act operations
    act_file = open(act_path, 'rb')
    act_data = act_file.read().decode("utf8")
    act_content = io.StringIO(act_data)
    act_dom = etree.parse(act_content)
    # get all articles
    articles = act_dom.xpath('//b:clan/@rbr', namespaces={'b': 'http://ftn.uns.ac.rs/xml'})
    # iterate through given articles
    for article in articles:
        if article == target_article:
            if operation == 'Dodatak':
                last_article = act_dom.xpath("//b:clan[@rbr='" + article + "']", namespaces={'b': 'http://ftn.uns.ac.rs/xml'})[0]
                new_article = amendment_dom.xpath('//b:clan', namespaces={'b': 'http://ftn.uns.ac.rs/xml'})[0]
                last_article.append(new_article)

            elif operation == 'Izmena':
                amendment_text = amendment_dom.xpath('//b:clan/b:stav/tekst/blok', namespaces={'b': 'http://ftn.uns.ac.rs/xml'})[0]
                target_text = act_dom.xpath("//b:clan[@rbr='" + article + "']/b:stav/tekst/blok", namespaces={'b': 'http://ftn.uns.ac.rs/xml'})[0]
                target_text.text = ""
                target_text.text = amendment_text.text

            elif operation == 'Brisanje':
                delete_article = act_dom.xpath("//b:clan[@rbr='" + article + "']", namespaces={'b': 'http://ftn.uns.ac.rs/xml'})[0]
                delete_article.getparent().remove(delete_article)

    # fix article numbers
    new_articles_num = act_dom.xpath('//b:clan', namespaces={'b': 'http://ftn.uns.ac.rs/xml'})
    start = 1
    for current_article in new_articles_num:
        current_article.set('rbr', str(start))
        start += 1
    # return text
    new_act = etree.tostring(act_dom, pretty_print=True)
    new_act_string = new_act.decode("utf8")
    update_document_from_string_uri(new_act_string, doc_uri)
    print("Amendment acceptance successful!")


def accept_amendment_uri(amendment_uri, act_uri):
    """
    Performs amentment operation on given act.
    :param amendment_uri: amednment document uri
    :param act_uri: act document uri
    """
    amendment = get_document_from_uri(amendment_uri)
    act = get_document_from_uri(act_uri)
    accept_amendment(amendment, act, act_uri)
    remove_existing_file(amendment)
    remove_existing_file(act)


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