#!/usr/bin/env python

__author__ = "Jai Ram Rideout"
__copyright__ = "Copyright 2011-2013, The BIOM Format Development Team"
__credits__ = ["Jai Ram Rideout"]
__license__ = "BSD"
__url__ = "http://biom-format.org"
__version__ = "1.2.0-dev"
__maintainer__ = "Jai Ram Rideout"
__email__ = "jai.rideout@gmail.com"

import json
from biom.commands.table_validator import TableValidator
from biom.unit_test import TestCase, main

class TableValidatorTests(TestCase):
    def setUp(self):
        """Set up data for use in unit tests."""
        self.cmd = TableValidator()
        self.min_sparse_otu = json.loads(min_sparse_otu)
        self.rich_sparse_otu = json.loads(rich_sparse_otu)
        self.rich_dense_otu = json.loads(rich_dense_otu)
        self.min_dense_otu = json.loads(min_dense_otu)

    def test_valid(self):
        """Correctly validates a table that is indeed... valid."""
        exp = {'valid_table': True, 'report_lines': []}
        obs = self.cmd(table_json=self.min_sparse_otu)
        self.assertEqual(obs, exp)

        obs = self.cmd(table_json=self.rich_sparse_otu)
        self.assertEqual(obs, exp)

        # Soldier, report!!
        obs = self.cmd(table_json=self.min_sparse_otu, detailed_report=True)
        self.assertTrue(obs['valid_table'])
        self.assertTrue(len(obs['report_lines']) > 0)

    def test_invalid(self):
        """Correctly invalidates a table that is... invalid."""
        del self.min_sparse_otu['date']
        exp = {'valid_table': False, 'report_lines': ["Missing field: 'date'"]}
        obs = self.cmd(table_json=self.min_sparse_otu)
        self.assertEqual(obs, exp)

        self.rich_dense_otu['shape'][1] = 42
        exp = {'valid_table': False,
               'report_lines': ['Incorrect number of cols: [0, 0, 1, 0, 0, 0]',
                                "Number of columns in 'columns' is not equal "
                                "to 'shape'"]}
        obs = self.cmd(table_json=self.rich_dense_otu)
        self.assertEqual(obs, exp)

    def test_valid_format_url(self):
        """validates format url"""
        table = self.min_sparse_otu

        obs = self.cmd._valid_format_url(table)
        self.assertTrue(len(obs) == 0)

        table['format_url'] = 'foo'
        obs = self.cmd._valid_format_url(table)
        self.assertTrue(len(obs) > 0)

    def test_valid_format(self):
        """Should match format string"""
        table = self.min_sparse_otu

        self.cmd._format_version = 'Biological Observation Matrix 1.0.0'
        obs = self.cmd._valid_format(table)
        self.assertTrue(len(obs) == 0)

        table['format'] = 'foo'
        obs = self.cmd._valid_format(table)
        self.assertTrue(len(obs) > 0)

    def test_valid_type(self):
        """Should be valid table type"""
        table = self.min_sparse_otu

        table['type'] = 'otu table' # should not be case sensitive
        obs = self.cmd._valid_type(table)
        self.assertTrue(len(obs) == 0)

        table['type'] = 'Pathway table'
        obs = self.cmd._valid_type(table)
        self.assertTrue(len(obs) == 0)

        table['type'] = 'Function table'
        obs = self.cmd._valid_type(table)
        self.assertTrue(len(obs) == 0)

        table['type'] = 'Ortholog table'
        obs = self.cmd._valid_type(table)
        self.assertTrue(len(obs) == 0)

        table['type'] = 'Gene table'
        obs = self.cmd._valid_type(table)
        self.assertTrue(len(obs) == 0)

        table['type'] = 'Metabolite table'
        obs = self.cmd._valid_type(table)
        self.assertTrue(len(obs) == 0)

        table['type'] = 'OTU table'
        obs = self.cmd._valid_type(table)
        self.assertTrue(len(obs) == 0)

        table['type'] = 'Taxon table'
        obs = self.cmd._valid_type(table)
        self.assertTrue(len(obs) == 0)

        table['type'] = 'foo'
        obs = self.cmd._valid_type(table)
        self.assertTrue(len(obs) > 0)

    def test_valid_generated_by(self):
        """Should have some string for generated by"""
        table = self.min_sparse_otu
        obs = self.cmd._valid_generated_by(table)
        self.assertTrue(len(obs) == 0)

        table['generated_by'] = None
        obs = self.cmd._valid_generated_by(table)
        self.assertTrue(len(obs) > 0)

    def test_valid_nullable_id(self):
        """Should just work."""
        pass

    def test_valid_metadata(self):
        """Can be nullable or an object"""
        table = self.min_sparse_otu

        table['rows'][2]['metadata'] = None
        obs = self.cmd._valid_metadata(table['rows'][2])
        self.assertTrue(len(obs) == 0)

        table['rows'][2]['metadata'] = {10:20}
        obs = self.cmd._valid_metadata(table['rows'][2])
        self.assertTrue(len(obs) == 0)

        table['rows'][2]['metadata'] = ""
        obs = self.cmd._valid_metadata(table['rows'][2])
        self.assertTrue(len(obs) > 0)

        table['rows'][2]['metadata'] = "asdasda"
        obs = self.cmd._valid_metadata(table['rows'][2])
        self.assertTrue(len(obs) > 0)

        table['rows'][2]['metadata'] = [{'a':'b'},{'c':'d'}]
        obs = self.cmd._valid_metadata(table['rows'][2])
        self.assertTrue(len(obs) > 0)

    def test_valid_matrix_type(self):
        """Make sure we have a valid matrix type"""
        obs = self.cmd._valid_matrix_type(self.min_dense_otu)
        self.assertTrue(len(obs) == 0)

        obs = self.cmd._valid_matrix_type(self.min_sparse_otu)
        self.assertTrue(len(obs) == 0)

        table = self.min_dense_otu

        table['matrix_type'] = 'spARSe'
        obs = self.cmd._valid_matrix_type(table)
        self.assertTrue(len(obs) > 0)

        table['matrix_type'] = 'sparse_asdasd'
        obs = self.cmd._valid_matrix_type(table)
        self.assertTrue(len(obs) > 0)

    def test_valid_matrix_element_type(self):
        """Make sure we have a valid matrix type"""
        table = self.min_sparse_otu

        obs = self.cmd._valid_matrix_element_type(table)
        self.assertTrue(len(obs) == 0)

        table['matrix_element_type'] = u'int'
        obs = self.cmd._valid_matrix_element_type(table)
        self.assertTrue(len(obs) == 0)

        table['matrix_element_type'] = 'float'
        obs = self.cmd._valid_matrix_element_type(table)
        self.assertTrue(len(obs) == 0)

        table['matrix_element_type'] = u'float'
        obs = self.cmd._valid_matrix_element_type(table)
        self.assertTrue(len(obs) == 0)

        table['matrix_element_type'] = 'str'
        obs = self.cmd._valid_matrix_element_type(table)
        self.assertTrue(len(obs) == 0)

        table['matrix_element_type'] = u'str'
        obs = self.cmd._valid_matrix_element_type(table)
        self.assertTrue(len(obs) == 0)

        table['matrix_element_type'] = 'obj'
        obs = self.cmd._valid_matrix_element_type(table)
        self.assertTrue(len(obs) > 0)

        table['matrix_element_type'] = u'asd'
        obs = self.cmd._valid_matrix_element_type(table)
        self.assertTrue(len(obs) > 0)

    def test_valid_datetime(self):
        """Make sure we have a datetime stamp"""
        table = self.min_sparse_otu

        obs = self.cmd._valid_datetime(table)
        self.assertTrue(len(obs) == 0)

        table['date'] = "1999-11-11T10:11:12"
        obs = self.cmd._valid_datetime(table)
        self.assertTrue(len(obs) == 0)

        table['date'] = "10-11-1999 10:11:12"
        obs = self.cmd._valid_datetime(table)
        self.assertTrue(len(obs) == 0)

        table['date'] = "10-11-1asdfasd:12"
        obs = self.cmd._valid_datetime(table)
        self.assertTrue(len(obs) > 0)

    def test_valid_sparse_data(self):
        """Takes a sparse matrix field and validates"""
        table = self.min_sparse_otu

        obs = self.cmd._valid_sparse_data(table)
        self.assertTrue(len(obs) == 0)

        # incorrect type
        table['matrix_element_type'] = 'float'
        obs = self.cmd._valid_sparse_data(table)
        self.assertTrue(len(obs) > 0)
        
        # not balanced
        table['matrix_element_type'] = 'int'
        table['data'][5] = [0,10]
        obs = self.cmd._valid_sparse_data(table)
        self.assertTrue(len(obs) > 0)
        
        # odd type for index
        table['data'][5] = [1.2,5,10]
        obs = self.cmd._valid_sparse_data(table)
        self.assertTrue(len(obs) > 0)

    def test_valid_dense_data(self):
        """Takes a dense matrix field and validates"""
        table = self.min_dense_otu

        obs = self.cmd._valid_dense_data(table)
        self.assertTrue(len(obs) == 0)

        # incorrect type
        table['matrix_element_type'] = 'float'
        obs = self.cmd._valid_dense_data(table)
        self.assertTrue(len(obs) > 0)

        # not balanced
        table['matrix_element_type'] = 'int'
        table['data'][1] = [0,10]
        obs = self.cmd._valid_dense_data(table)
        self.assertTrue(len(obs) > 0)

        # bad type in a field
        table['data'][1] = [5, 1, 0, 2.3, 3, 1]
        obs = self.cmd._valid_dense_data(table)
        self.assertTrue(len(obs) > 0)

    def test_valid_shape(self):
        """validates shape information"""
        obs = self.cmd._valid_shape(self.min_sparse_otu)
        self.assertTrue(len(obs) == 0)

        obs = self.cmd._valid_shape(self.rich_sparse_otu)
        self.assertTrue(len(obs) == 0)

        bad_shape = self.min_sparse_otu.copy()
        bad_shape['shape'] = ['asd',10]
        obs = self.cmd._valid_shape(bad_shape)
        self.assertTrue(len(obs) > 0)

    def test_valid_rows(self):
        """validates rows: field"""
        table = self.rich_dense_otu

        obs = self.cmd._valid_rows(table)
        self.assertTrue(len(obs) == 0)

        table['rows'][0]['id'] = ""
        obs = self.cmd._valid_rows(table)
        self.assertTrue(len(obs) > 0)

        table['rows'][0]['id'] = None
        obs = self.cmd._valid_rows(table)
        self.assertTrue(len(obs) > 0)
        
        del table['rows'][0]['id']
        obs = self.cmd._valid_rows(table)
        self.assertTrue(len(obs) > 0)

        table['rows'][0]['id'] = 'asd'
        table['rows'][0]['metadata'] = None
        obs = self.cmd._valid_rows(table)
        self.assertTrue(len(obs) == 0)

        # since this is an OTU table, metadata is a required key
        del table['rows'][0]['metadata']
        obs = self.cmd._valid_rows(table)
        self.assertTrue(len(obs) > 0)

    def test_valid_columns(self):
        """validates table:columns: fields"""
        table = self.rich_dense_otu

        obs = self.cmd._valid_columns(table)
        self.assertTrue(len(obs) == 0)

        table['columns'][0]['id'] = ""
        obs = self.cmd._valid_columns(table)
        self.assertTrue(len(obs) > 0)

        table['columns'][0]['id'] = None
        obs = self.cmd._valid_columns(table)
        self.assertTrue(len(obs) > 0)
        
        del table['columns'][0]['id']
        obs = self.cmd._valid_columns(table)
        self.assertTrue(len(obs) > 0)

        table['columns'][0]['id'] = 'asd'
        table['columns'][0]['metadata'] = None
        obs = self.cmd._valid_columns(table)
        self.assertTrue(len(obs) == 0)

        # since this is an OTU table, metadata is a required key
        del table['columns'][0]['metadata']
        obs = self.cmd._valid_columns(table)
        self.assertTrue(len(obs) > 0)

    def test_valid_data(self):
        """validates data: fields"""
        # the burden of validating data is passed on to valid_sparse_data
        # and valid_dense_data
        table = self.rich_sparse_otu

        obs = self.cmd._valid_data(table)
        self.assertTrue(len(obs) == 0)
        
        table['matrix_type'] = 'foo'
        obs = self.cmd._valid_data(table)
        self.assertTrue(len(obs) > 0)


rich_sparse_otu = """{
     "id":null,
     "format": "Biological Observation Matrix 1.0.0",
     "format_url": "http://biom-format.org",
     "type": "OTU table",
     "generated_by": "QIIME revision XYZ",
     "date": "2011-12-19T19:00:00",
     "rows":[
        {"id":"GG_OTU_1", "metadata":{"taxonomy":["k__Bacteria", "p__Proteobacteria", "c__Gammaproteobacteria", "o__Enterobacteriales", "f__Enterobacteriaceae", "g__Escherichia", "s__"]}},
        {"id":"GG_OTU_2", "metadata":{"taxonomy":["k__Bacteria", "p__Cyanobacteria", "c__Nostocophycideae", "o__Nostocales", "f__Nostocaceae", "g__Dolichospermum", "s__"]}},
        {"id":"GG_OTU_3", "metadata":{"taxonomy":["k__Archaea", "p__Euryarchaeota", "c__Methanomicrobia", "o__Methanosarcinales", "f__Methanosarcinaceae", "g__Methanosarcina", "s__"]}},
        {"id":"GG_OTU_4", "metadata":{"taxonomy":["k__Bacteria", "p__Firmicutes", "c__Clostridia", "o__Halanaerobiales", "f__Halanaerobiaceae", "g__Halanaerobium", "s__Halanaerobiumsaccharolyticum"]}},
        {"id":"GG_OTU_5", "metadata":{"taxonomy":["k__Bacteria", "p__Proteobacteria", "c__Gammaproteobacteria", "o__Enterobacteriales", "f__Enterobacteriaceae", "g__Escherichia", "s__"]}}
        ],
     "columns":[
        {"id":"Sample1", "metadata":{
                                 "BarcodeSequence":"CGCTTATCGAGA",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"gut",
                                 "Description":"human gut"}},
        {"id":"Sample2", "metadata":{
                                 "BarcodeSequence":"CATACCAGTAGC",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"gut",
                                 "Description":"human gut"}},
        {"id":"Sample3", "metadata":{
                                 "BarcodeSequence":"CTCTCTACCTGT",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"gut",
                                 "Description":"human gut"}},
        {"id":"Sample4", "metadata":{
                                 "BarcodeSequence":"CTCTCGGCCTGT",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"skin",
                                 "Description":"human skin"}},
        {"id":"Sample5", "metadata":{
                                 "BarcodeSequence":"CTCTCTACCAAT",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"skin",
                                 "Description":"human skin"}},
        {"id":"Sample6", "metadata":{
                                 "BarcodeSequence":"CTAACTACCAAT",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"skin",
                                 "Description":"human skin"}}
        ],
     "matrix_type": "sparse",
     "matrix_element_type": "int",
     "shape": [5, 6], 
     "data":[[0,2,1],
             [1,0,5],
             [1,1,1],
             [1,3,2],
             [1,4,3],
             [1,5,1],
             [2,2,1],
             [2,3,4],
             [2,5,2],
             [3,0,2],
             [3,1,1],
             [3,2,1],
             [3,5,1],
             [4,1,1],
             [4,2,1]
            ]
    }"""

min_sparse_otu = """{
        "id":null,
        "format": "Biological Observation Matrix 1.0.0",
        "format_url": "http://biom-format.org",
        "type": "OTU table",
        "generated_by": "QIIME revision XYZ",
        "date": "2011-12-19T19:00:00",
        "rows":[
                {"id":"GG_OTU_1", "metadata":null},
                {"id":"GG_OTU_2", "metadata":null},
                {"id":"GG_OTU_3", "metadata":null},
                {"id":"GG_OTU_4", "metadata":null},
                {"id":"GG_OTU_5", "metadata":null}
            ],  
        "columns": [
                {"id":"Sample1", "metadata":null},
                {"id":"Sample2", "metadata":null},
                {"id":"Sample3", "metadata":null},
                {"id":"Sample4", "metadata":null},
                {"id":"Sample5", "metadata":null},
                {"id":"Sample6", "metadata":null}
            ],
        "matrix_type": "sparse",
        "matrix_element_type": "int",
        "shape": [5, 6], 
        "data":[[0,2,1],
                [1,0,5],
                [1,1,1],
                [1,3,2],
                [1,4,3],
                [1,5,1],
                [2,2,1],
                [2,3,4],
                [2,5,2],
                [3,0,2],
                [3,1,1],
                [3,2,1],
                [3,5,1],
                [4,1,1],
                [4,2,1]
               ]
    }"""

rich_dense_otu = """{
     "id":null,
     "format": "Biological Observation Matrix 1.0.0",
     "format_url": "http://biom-format.org",
     "type": "OTU table",
     "generated_by": "QIIME revision XYZ",
     "date": "2011-12-19T19:00:00",  
     "rows":[
        {"id":"GG_OTU_1", "metadata":{"taxonomy":["k__Bacteria", "p__Proteobacteria", "c__Gammaproteobacteria", "o__Enterobacteriales", "f__Enterobacteriaceae", "g__Escherichia", "s__"]}},
        {"id":"GG_OTU_2", "metadata":{"taxonomy":["k__Bacteria", "p__Cyanobacteria", "c__Nostocophycideae", "o__Nostocales", "f__Nostocaceae", "g__Dolichospermum", "s__"]}},
        {"id":"GG_OTU_3", "metadata":{"taxonomy":["k__Archaea", "p__Euryarchaeota", "c__Methanomicrobia", "o__Methanosarcinales", "f__Methanosarcinaceae", "g__Methanosarcina", "s__"]}},
        {"id":"GG_OTU_4", "metadata":{"taxonomy":["k__Bacteria", "p__Firmicutes", "c__Clostridia", "o__Halanaerobiales", "f__Halanaerobiaceae", "g__Halanaerobium", "s__Halanaerobiumsaccharolyticum"]}},
        {"id":"GG_OTU_5", "metadata":{"taxonomy":["k__Bacteria", "p__Proteobacteria", "c__Gammaproteobacteria", "o__Enterobacteriales", "f__Enterobacteriaceae", "g__Escherichia", "s__"]}}
        ],  
     "columns":[
        {"id":"Sample1", "metadata":{
                                 "BarcodeSequence":"CGCTTATCGAGA",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"gut",
                                 "Description":"human gut"}},
        {"id":"Sample2", "metadata":{
                                 "BarcodeSequence":"CATACCAGTAGC",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"gut",
                                 "Description":"human gut"}},
        {"id":"Sample3", "metadata":{
                                 "BarcodeSequence":"CTCTCTACCTGT",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"gut",
                                 "Description":"human gut"}},
        {"id":"Sample4", "metadata":{
                                 "BarcodeSequence":"CTCTCGGCCTGT",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"skin",
                                 "Description":"human skin"}},
        {"id":"Sample5", "metadata":{
                                 "BarcodeSequence":"CTCTCTACCAAT",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"skin",
                                 "Description":"human skin"}},
        {"id":"Sample6", "metadata":{
                                 "BarcodeSequence":"CTAACTACCAAT",
                                 "LinkerPrimerSequence":"CATGCTGCCTCCCGTAGGAGT",
                                 "BODY_SITE":"skin",
                                 "Description":"human skin"}}
                ],
     "matrix_type": "dense",
     "matrix_element_type": "int",
     "shape": [5,6],
     "data":  [[0,0,1,0,0,0], 
               [5,1,0,2,3,1],
               [0,0,1,4,2,0],
               [2,1,1,0,0,1],
               [0,1,1,0,0,0]]
    }"""

min_dense_otu = """ {
        "id":null,
        "format": "Biological Observation Matrix 1.0.0",
        "format_url": "http://biom-format.org",
        "type": "OTU table",
        "generated_by": "QIIME revision XYZ",
        "date": "2011-12-19T19:00:00",
        "rows":[
                {"id":"GG_OTU_1", "metadata":null},
                {"id":"GG_OTU_2", "metadata":null},
                {"id":"GG_OTU_3", "metadata":null},
                {"id":"GG_OTU_4", "metadata":null},
                {"id":"GG_OTU_5", "metadata":null}
            ],  
        "columns": [
                {"id":"Sample1", "metadata":null},
                {"id":"Sample2", "metadata":null},
                {"id":"Sample3", "metadata":null},
                {"id":"Sample4", "metadata":null},
                {"id":"Sample5", "metadata":null},
                {"id":"Sample6", "metadata":null}
            ],  
        "matrix_type": "dense",
        "matrix_element_type": "int",
        "shape": [5,6],
        "data":  [[0,0,1,0,0,0], 
                  [5,1,0,2,3,1],
                  [0,0,1,4,2,0],
                  [2,1,1,0,0,1],
                  [0,1,1,0,0,0]]
    }"""


if __name__ == "__main__":
    main()
