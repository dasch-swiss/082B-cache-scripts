import csv
import numpy as np
import pandas as pd
import sys
import os
import datetime

from pprint import pprint

from lxml import etree
from lxml.builder import E


def make_root(shortcode, default_ontology):
    root = etree.Element("knora", nsmap={'xsi': "http://www.w3.org/2001/XMLSchema-instance"})
    root.set("shortcode", shortcode)
    root.set("default-ontology", default_ontology)
    return root

    # noinspection PyPep8Naming
def append_permissions(root_element: etree.Element):
    PERMISSIONS = E.permissions
    ALLOW = E.allow

    res_default = PERMISSIONS(id="res-default")
    res_default.append(ALLOW("RV", group='UnknownUser'))
    res_default.append(ALLOW("V", group='KnownUser'))
    res_default.append(ALLOW("CR", group='Creator'))
    res_default.append(ALLOW("CR", group='ProjectAdmin'))
    root_element.append(res_default)

    res_restricted = PERMISSIONS(id="res-restricted")
    res_restricted.append(ALLOW("V", group='KnownUser'))
    res_restricted.append(ALLOW("CR", group='Creator'))
    res_restricted.append(ALLOW("CR", group='ProjectAdmin'))
    root_element.append(res_restricted)

    prop_default = PERMISSIONS(id="prop-default")
    prop_default.append(ALLOW("V", group='UnknownUser'))
    prop_default.append(ALLOW("V", group='KnownUser'))
    prop_default.append(ALLOW("CR", group='Creator'))
    prop_default.append(ALLOW("CR", group='ProjectAdmin'))
    root_element.append(prop_default)

    prop_restricted = PERMISSIONS(id="prop-restricted")
    prop_restricted.append(ALLOW("V", group='KnownUser'))
    prop_restricted.append(ALLOW("CR", group='Creator'))
    prop_restricted.append(ALLOW("CR", group='ProjectAdmin'))
    root_element.append(prop_restricted)

    return root_element


# noinspection PyPep8Naming
def make_boolean_prop(name, value, permissions="prop-default") -> etree.Element:
    prop_ = etree.Element("boolean-prop", name=name)
    value_ = etree.Element("boolean", permissions=permissions)
    value_.text = value
    prop_.append(value_)
    return prop_


# noinspection PyPep8Naming
def make_color_prop(name, value, permissions="prop-default"):
    prop_ = etree.Element("color-prop", name=name)
    value_ = etree.Element("color", permissions=permissions)
    value_.text = value
    prop_.append(value_)
    return prop_


# noinspection PyPep8Naming
def make_date_prop(name, value, permissions="prop-default"):
    prop_ = etree.Element("date-prop", name=name)
    value_ = etree.Element("date", permissions=permissions)
    value_.text = value
    prop_.append(value_)
    return prop_


# noinspection PyPep8Naming
def make_geometry_prop(name, value, permissions="prop-default"):
    prop_ = etree.Element("geometry-prop", name=name)
    value_ = etree.Element("geometry", permissions=permissions)
    value_.text = value
    prop_.append(value_)
    return prop_


# noinspection PyPep8Naming
def make_geoname_prop(name, value, permissions="prop-default"):
    prop_ = etree.Element("geoname-prop", name=name)
    value_ = etree.Element("geoname", permissions=permissions)
    value_.text = value
    prop_.append(value_)
    return prop_


# noinspection PyPep8Naming
def make_resptr_prop(name, value, permissions="prop-default"):
    prop_ = etree.Element("resptr-prop", name=name)
    value_ = etree.Element("resptr", permissions=permissions)
    value_.text = value
    prop_.append(value_)
    return prop_


# noinspection PyPep8Naming
def make_interval_prop(name, value, permissions="prop-default"):
    prop_ = etree.Element("interval-prop", name=name)
    value_ = etree.Element("interval", permissions=permissions)
    value_.text = value
    prop_.append(value_)
    return prop_


# noinspection PyPep8Naming
def make_list_prop(list_name, prop_name, values, permissions="prop-default"):
    prop_ = etree.Element("list-prop", list=list_name, name=prop_name)

    for val in values:
        value_ = etree.Element("list", permissions=permissions)
        value_.text = val
        prop_.append(value_)

    return prop_


# noinspection PyPep8Naming
def make_text_prop(name, value, permissions="prop-default", encoding="utf8"):
    prop_ = etree.Element("text-prop", name=name)
    value_ = etree.Element("text", permissions=permissions, encoding=encoding)
    value_.text = value
    prop_.append(value_)
    return prop_


# noinspection PyPep8Naming
def make_uri_prop(name, value, permissions="prop-default"):
    prop_ = etree.Element("uri-prop", name=name)
    value_ = etree.Element("uri", permissions=permissions)
    value_.text = value
    prop_.append(value_)
    return prop_

# noinspection PyPep8Naming
def make_bitstream_prop(name, value, permissions="prop-default"):
    prop_ = etree.Element("bitstream")
    prop_.text = value
    return prop_


# noinspection PyPep8Naming
def make_resource(label, restype, id, permissions="res-default") -> etree.Element:
    resource_ = etree.Element("resource", label=label, restype=restype, id=id, permissions=permissions)
    return resource_


def main():
    cachechapter = pd.read_csv('./data/datenspeicherung_cache_15-02-2021_Chapter.csv', ';')
    cachereplica = pd.read_csv('./data/datenspeicherung_cache_15-02-2021_Replic.csv', ';')

    print(cachechapter.loc[0, :])
    print(cachechapter.at[0, 'kapitelname'])

    root = make_root("082B", "cache")
    root = append_permissions(root)

    # loop start
    # fill in loop

    for index, row in cachechapter.iterrows():
        kapitel = make_resource(row['kapitelname'], ":Kapitel", "kapitel_obj_"+str(index), "res-default")
        if pd.notna(row['pdf']):
            kapitel.append(make_bitstream_prop(":pdf", row['pdf'][21:]))

        if pd.notna(row['kapitelname']):
            kapitel.append(make_text_prop(":kapitelname", row['kapitelname']))

        if pd.notna(row['autor']):
            kapitel.append(make_text_prop(":autor", row['autor']))

        if pd.notna(row['titel_des_buchs']):
            kapitel.append(make_text_prop(":titel_des_buchs", row['titel_des_buchs']))

        if pd.notna(row['autoren_des_buchs']):
            kapitel.append(make_text_prop(":autoren_des_buchs", row['autoren_des_buchs']))

        if pd.notna(row['datum_der_veroeffentlichung']):
            kapitel.append(make_text_prop(":datum_der_veroeffentlichung", row['datum_der_veroeffentlichung']))

        if pd.notna(row['link']):
            kapitel.append(make_text_prop(":link", row['link']))

        if pd.notna(row['verlag']):
            kapitel.append(make_text_prop(":verlag", row['verlag']))

        root.append(kapitel)

    for index, row in cachereplica.iterrows():
        replik = make_resource(row['titel'], ":Replik", "titel"+str(index), "res-default")
        if pd.notna(row['pdf']):
            replik.append(make_bitstream_prop(":pdf", row['pdf'][21:]))

        if pd.notna(row['titel']):
            replik.append(make_text_prop(":titel", row['titel']))

        if pd.notna(row['autor']):
            replik.append(make_text_prop(":autor", row['autor']))

        if pd.notna(row['replik_auf']):
            replik.append(make_resptr_prop(":replik_auf", "kapitel_obj_" + str(index)))

        if pd.notna(row['datum_der_veroeffentlichung']):
            replik.append(make_text_prop(":datum_der_veroeffentlichung", row['datum_der_veroeffentlichung']))

        if pd.notna(row['link']):
            replik.append(make_text_prop(":link", row['link']))

        root.append(replik)

    

    # loop end

    document = root

    et = etree.ElementTree(document)
    with open('cache.xml', 'wb') as f:
        et.write(f, encoding="utf-8", xml_declaration=True, pretty_print=True)


if __name__ == "__main__":
    main()