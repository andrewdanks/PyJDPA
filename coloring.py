#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
""" Display a text with coloured sentiment phrase

"""
import os
import logging
from lxml import etree
from termcolor import colored

log = logging.getLogger(__name__)

class InvalidJDPADocIdError(Exception):
    pass

class Annotation(object):

    def __init__(self, id, annotator, start, end, text):
        """ Annotation object

        """
        self.id, self.annotator, self.start, self.end, self.text\
            = id, annotator, start, end, text


class JDPAParser(object):
    """ This class contains a variety of functions used to interpret an 
    annotated JDPA doc.

    """
    def __init__(self, path, doc_id):
        self.doc_id = doc_id
        try:
            self.type, self.batch_id, self.doc_short_id = doc_id.split("-")
        except ValueError, err:
            raise InvalidJDPADocIdError("doc_id must follow the format of "
                      "{type}-{batch_id}-{id}, e.g.: "
                      "camera-002-001")

        batch_path = os.path.join(path, self.type, "batch%s" % self.batch_id)  

        text_file = os.path.join(batch_path, "txt", "%s.txt" % doc_id)
        ftext = open(text_file, "r")
        self.text = ftext.read()
        ftext.close()

        ann_file = os.path.join(batch_path, "annotation",
                                "%s.txt.knowtator.xml" % doc_id)
        self.dom = etree.parse(ann_file)                                 

    def parse(self):
        self.annotations = []
        for item in self.dom.xpath("//annotation"):
            self.annotations.append(
                    Annotation(item.xpath("mention")[0].get("id"),
                               item.xpath("annotator")[0].get("id"),
                               item.xpath("span")[0].get("start"),
                               item.xpath("span")[0].get("end"),
                               self.text)
                )


def main(options, args):
    parser = JDPAParser(options.path, args[0])
    parser.parse()
    for ann in parser.annotations:
        print ann.id, ann.annotator, ann.start, ann.end

if __name__ == "__main__":
    # Parse command options
    from optparse import OptionParser
    parser = OptionParser(usage="Usage: %prog [options] doc_file_name."
                                "E.g: %prog camera-002-002")    
    parser.add_option("-d", "--data-path", dest="path",
                       default="../data", action="store",
                       help="Path to JDPA data dir")
    # Add more options here
    options, args = parser.parse_args()
    main(options, args)
