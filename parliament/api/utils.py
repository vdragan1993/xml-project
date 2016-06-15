from lxml import etree, objectify
from lxml.etree import XMLSyntaxError
import os


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