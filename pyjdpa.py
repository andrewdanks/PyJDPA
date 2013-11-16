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

SEPARATOR = "\t"

class InvalidJDPADocIdError(Exception):
    pass

class Annotation(object):

    def __init__(self, id, annotator, start, end, text, mention_class,
                       slot_mention_ids):
        """ Annotation object

        """
        self.id, self.annotator, self.start, self.end, self.text,\
        self.mention_class, self.slot_mention_ids\
            = id, annotator, start, end, text, mention_class, slot_mention_ids

    @classmethod
    def from_dom(cls, item, text=None):
        id = item.find("mention").get("id")
        class_mention = item.xpath("//classMention[@id='%s']" % id)[0]
        return cls(
            item.find("mention").get("id"),
            item.find("annotator").get("id"),
            int(item.find("span").get("start")),
            int(item.find("span").get("end")),
            text,
            class_mention.find("mentionClass").get("id"),
            [el.get("id") for el in class_mention.findall("hasSlotMention")]
        )       

class SlotMention(object):

    def __init__(self, id, mention_slot, values, type):
        """ type must be "string" or "complex" """
        self.id, self.mention_slot, self.values, self.type\
            = id, mention_slot, values, type

    @classmethod
    def from_dom(cls, item):
        return cls(
                item.get("id"),
                item.find("mentionSlot").get("id"),
                [el.get("value") for el in\
                    (item.findall("stringSlotMentionValue") +
                     item.findall("complexSlotMentionValue"))],
                {"stringSlotMentionValue": "string",
                 "complexSlotMentionValue": "complex"}.get(item.tag)
            )


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
        self._parse_annotations()
        self._parse_slot_mentions()

    def _parse_annotations(self):
        self.annotations = {}
        for item in self.dom.xpath("//annotation"):
            id = item.xpath("mention")[0].get("id")
            ann = Annotation.from_dom(item, self.text)
            self.annotations[id] = ann

    def _parse_slot_mentions(self):
        self.slot_mentions = {}
        for item in (self.dom.xpath("//stringSlotMention")\
                     + self.dom.xpath("//complexSlotMention")):
            id = item.get("id")
            self.slot_mentions[id] = SlotMention.from_dom(item)


def main(options, args):
    if len(args) != 2:
        print("Please run with --help for usage information.")
        return 1

    doc_id, rel_type = args
    doc = JDPAParser(options.path, doc_id)
    doc.parse()
    if options.slot_mention == "complex":
        titles = ["arg0", "rel", "arg1", "arg0_start", "arg0_end", "arg1_start", "arg1_end"]
    elif options.slot_mention == "string":
        titles = ["arg0", "rel", "value", "arg0_start", "arg0_end"]

    sents = None
    if options.context:
        import nltk
        sent_tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")
        sents = sent_tokenizer.span_tokenize(doc.text)

    if not options.no_header:
        print(SEPARATOR.join(titles))
    for arg0 in doc.annotations.values():
        for rel_id in arg0.slot_mention_ids:
            rel = doc.slot_mentions[rel_id]
            if rel.mention_slot.lower() == rel_type.lower():
                for value in rel.values:
                    if options.slot_mention=="complex":
                        arg1 = doc.annotations[value]
                        result = [doc.text[arg0.start:arg0.end],
                                  rel_type,
                                  doc.text[arg1.start:arg1.end], 
                                  str(arg0.start),
                                  str(arg0.end),
                                  str(arg1.start),
                                  str(arg1.end)]
                    else:
                        result =[doc.text[arg0.start:arg0.end],
                                 rel_type,
                                 value,
                                 str(arg0.start),
                                 str(arg0.end)]
                    if options.context:
                        result.append(
                            doc.text[slice(
                                *[s for s in sents if arg0.start >= s[0] and\
                                                     arg0.end <= s[1]][0])
                            ]
                        )
                    print(SEPARATOR.join(result))))
                                

    return 0


if __name__ == "__main__":
    # Parse command options
    import sys
    from optparse import OptionParser
    parser = OptionParser(usage="Usage: %prog [options] doc_file_name rel_type. "
                                "E.g: %prog camera-002-002 target")    
    parser.add_option("-d", "--data-path", dest="path",
                       default="../data", action="store",
                       help="Path to JDPA data dir. Default is ../data")
    parser.add_option("-H", "--no-header", dest="no_header",
                default=False, action="store_true",
                help="Don't display header line")
    parser.add_option("-s", "--slot-mention", dest="slot_mention",
                default="complex", action="store",
                help="Slot mention type: 'string' (stringSlotMention) or"
                     "'complex' (complexSlotMention). Default is 'complex'. ")
    parser.add_option("-c", "--context", dest="context",
                default=False, action="store_true",
                help="Display sentence containing arg0. Require ntlk and "
                     "tokenizers/punkt/english.pickle installed.")
    options, args = parser.parse_args()
    sys.exit(main(options, args))
