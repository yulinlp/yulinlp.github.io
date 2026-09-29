import unittest
from main import merge

class SyncTests(unittest.TestCase):
    def setUp(self):
        self.groups = [dict(id='safety', papers=[dict(title='A paper!', authors='Weixiang Zhao, Yulin Hu', co_first_author=True, student_first_author=True, distinction='Oral', tags=[{'label':'Safety'}], citations=31)])]
        self.snapshot = dict(total=400, papers=[dict(id='id:1', title='A paper', citations=35, url='https://scholar.google.com/citations?citation_for_view=id:1')])

    def test_preserves_editorial_fields_and_matches_title(self):
        groups, metrics = merge(self.groups, {}, self.snapshot, '2026-09-29')
        p=groups[0]['papers'][0]
        self.assertTrue(p['co_first_author'])
        self.assertEqual(p['distinction'], 'Oral')
        self.assertEqual(p['tags'], [{'label':'Safety'}])
        self.assertEqual(p['citations'],35)
        self.assertEqual(self.groups[0]['papers'][0]['citations'],31)
        self.assertEqual(metrics['total_citations'],400)

    def test_new_paper_and_idempotence(self):
        self.snapshot['papers'].append(dict(id='id:2', title='New paper', authors='Yulin Hu, Someone Else', full_authors=True, citations=1, url='https://scholar.google.com/citations?citation_for_view=id:2'))
        groups, metrics=merge(self.groups, {}, self.snapshot, '2026-09-29')
        again, _=merge(groups, metrics, self.snapshot, '2026-09-29')
        self.assertEqual(groups,again)
        self.assertEqual(groups[0]['id'],'recent-publications')
        self.assertTrue(groups[0]['papers'][0]['first_author'])

    def test_incomplete_data_fails_without_mutation(self):
        with self.assertRaises(ValueError):
            merge(self.groups, {}, dict(total=0,papers=[]), '2026-09-29')
        self.snapshot['papers'][0]['title']='Unknown paper'
        with self.assertRaises(ValueError):
            merge(self.groups, {}, self.snapshot, '2026-09-29')
        self.assertEqual(self.groups[0]['papers'][0]['citations'],31)

if __name__ == '__main__':
    unittest.main()
