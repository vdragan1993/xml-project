from lxml import etree, objectify
from lxml.etree import XMLSyntaxError


# location of xsd
xsd_act = 'schema/XML_Proj_schema_act.xsd'
xsd_amendment = 'schema/XML_Proj_schema_amandman.xsd'


def validate_act(act_xml_string):
    """
    Validates act with an XML schema
    :param act_xml_string: XML string of an act, UTF-8 encoded
    :return: True or False
    """
    try:
        schema = etree.XMLSchema(file=xsd_act)
        parser = objectify.makeparser(schema=schema)
        objectify.fromstring(act_xml_string, parser)
        return True
    except XMLSyntaxError:
        return False
        pass


def validate_amendment(amendment_xml_string):
    """
    Validates amendment with an XML schema
    :param amendment_xml_string: XML string of an amendment, UTF-8 encoded
    :return: True or False
    """
    try:
        schema = etree.XMLSchema(file=xsd_amendment)
        parser = objectify.makeparser(schema=schema)
        objectify.fromstring(amendment_xml_string, parser)
        return True
    except XMLSyntaxError:
        return False
        pass
