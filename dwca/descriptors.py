# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


class _SectionDescriptor(object):
    """Class used to encapsulate the file section (for Core or an Extension) of the Descriptor"""
    def __init__(self, section_tag, is_core):
        #:
        self.raw_beautifulsoup = section_tag  # It's a Tag instance

        if is_core:
            self.represents_corefile = True
            self.represents_extensionfile = False
            self.id_index = int(self.raw_beautifulsoup.id['index'])
        else:
            self.represents_corefile = False
            self.represents_extensionfile = True
            self.coreid_index = int(self.raw_beautifulsoup.coreid['index'])

        #:
        self.type = self.raw_beautifulsoup['rowType']

        #:
        self.fields = []
        for f in self.raw_beautifulsoup.findAll('field'):
            default = (f['default'] if f.has_attr('default') else None)
            
            # Default fields don't have an index attribute
            index = (f['index'] if f.has_attr('index') else None)

            self.fields.append({'term': f['term'], 'index': index, 'default': default})

        # a Set containing all the Darwin Core terms appearing in Core file
        term_names = [f['term'] for f in self.fields]
        #:
        self.terms = set(term_names)

        #:
        self.file_location = self.raw_beautifulsoup.files.location.string  # TODO: Test !!!

        #:
        self.encoding = self.raw_beautifulsoup['encoding']  # TODO: test

        #:
        self.lines_terminated_by = self.raw_beautifulsoup['linesTerminatedBy'].decode("string-escape")  # TODO: test

        #:
        self.fields_terminated_by = self.raw_beautifulsoup['fieldsTerminatedBy'].decode("string-escape")  # TODO: test

    @property
    def lines_to_ignore(self):
        try:
            return int(self.raw_beautifulsoup['ignoreHeaderLines'])
        except KeyError:
            return 0


# TODO: Make _ArchiveDescriptor better structured (.core, .extension w/ child objects, ...)
class _ArchiveDescriptor(object):
    """Class used to encapsulate the Archive Descriptor"""
    def __init__(self, metaxml_content):
        #:
        self.raw_beautifulsoup = BeautifulSoup(metaxml_content, 'xml')
        
        #:
        self.metadata_filename = self.raw_beautifulsoup.archive['metadata']  # Relative to archive

        #:
        self.core = _SectionDescriptor(self.raw_beautifulsoup.core, is_core=True)

        self.extensions = [_SectionDescriptor(tag, False) for tag in self.raw_beautifulsoup.findAll('extension')]

        #:
        self.extensions_type = [e.type for e in self.extensions]

        
