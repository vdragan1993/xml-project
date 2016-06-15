from lxml import etree, objectify
from lxml.etree import XMLSyntaxError
import os
from xhtml2pdf import pisa


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
xsl_act_html = 'transformations/'
xsl_act_pdf = 'transformations/'


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
        css = css_act

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
