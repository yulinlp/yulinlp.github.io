"""Refresh Scholar counts; preserve curated metadata and safely add new papers."""
import copy
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
PROFILE = 'https://scholar.google.com/citations?user=ZhV-ua0AAAAJ&hl=en'


def title_key(title):
    return re.sub(r'[^\w]', '', title).casefold()


def merge(groups, metrics, snapshot, today):
    if not isinstance(snapshot['total'], int) or snapshot['total'] < 0 or not snapshot['papers']:
        raise ValueError('Incomplete Scholar response; keeping saved data')
    groups, metrics = copy.deepcopy(groups), copy.deepcopy(metrics)
    known = [p for g in groups for p in g['papers']]
    added = []
    for row in snapshot['papers']:
        paper = next((p for p in known if (p.get('scholar_url') and parse_qs(urlparse(p['scholar_url']).query).get('citation_for_view') == [row['id']]) or title_key(p['title']) == title_key(row['title'])), None)
        if paper is None:
            if not row.get('authors') or not row.get('full_authors'):
                raise ValueError('Missing full authors for new paper')
            paper = dict(title=row['title'], authors=row['authors'], venue=row.get('venue') or 'New publication', venue_type='preprint', paper_url=row['url'], links=[], tags=[], distinction='', distinction_source='', first_author=row['authors'].split(',')[0].strip() == 'Yulin Hu')
            added.append(paper)
            known.append(paper)
        paper.update(citations=row['citations'], scholar_url=row['url'], citation_checked=today, featured_citations=row['citations'] >= 100)
    if added:
        group = next((g for g in groups if g['id'] == 'recent-publications'), None)
        if group is None:
            group = dict(icon='📄', name='Recent Publications', id='recent-publications', papers=[])
            groups.insert(0, group)
        group['papers'] = added + group['papers']
    metrics.update(total_citations=snapshot['total'], checked_on=datetime.strptime(today, '%Y-%m-%d').strftime('%B %d, %Y').replace(' 0', ' '))
    return groups, metrics


def fetch(groups):
    import requests
    from bs4 import BeautifulSoup
    session = requests.Session()
    session.headers['User-Agent'] = 'Mozilla/5.0'
    def get(url):
        response = session.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.select_one('#gs_captcha_ccl') or 'unusual traffic' in soup.get_text().lower():
            raise RuntimeError('Scholar access restricted; keeping saved data')
        return soup
    rows = []
    total = None
    known_titles = {title_key(p['title']) for g in groups for p in g['papers']}
    known_ids = {parse_qs(urlparse(p.get('scholar_url', '')).query).get('citation_for_view', [''])[0] for g in groups for p in g['papers']}
    for start in range(0, 2000, 100):
        soup = get(PROFILE + f'&pagesize=100&cstart={start}')
        if start == 0:
            cell = soup.select_one('#gsc_rsb_st tbody tr td:nth-of-type(2)')
            if cell is None:
                raise RuntimeError('Missing Scholar total; keeping saved data')
            total = int(cell.get_text().replace(',', ''))
        entries = soup.select('.gsc_a_tr')
        if not entries:
            raise RuntimeError('Missing publication list; keeping saved data')
        for entry in entries:
            link = entry.select_one('.gsc_a_at')
            url = urljoin(PROFILE, link['href'])
            pid = parse_qs(urlparse(url).query)['citation_for_view'][0]
            count = entry.select_one('.gsc_a_ac').get_text(strip=True).replace(',', '')
            if count and not count.isdigit():
                raise ValueError('Unexpected citation count')
            row = dict(id=pid, title=link.get_text(strip=True), url=url, citations=int(count or '0'))
            if pid not in known_ids and title_key(row['title']) not in known_titles:
                time.sleep(2)
                detail = get(url)
                fields = {r.select_one('.gsc_oci_field').get_text(strip=True): r.select_one('.gsc_oci_value').get_text(strip=True) for r in detail.select('.gs_scl') if r.select_one('.gsc_oci_field') and r.select_one('.gsc_oci_value')}
                row.update(authors=fields.get('Authors'), full_authors=bool(fields.get('Authors')), venue=fields.get('Conference') or fields.get('Journal'))
            rows.append(row)
        more = soup.select_one('#gsc_bpf_more')
        if more is None:
            raise RuntimeError('Missing pagination control')
        if more.has_attr('disabled'):
            break
        time.sleep(2)
    else:
        raise RuntimeError('Pagination did not finish')
    return dict(total=total, papers=rows)


if __name__ == '__main__':
    data = ROOT / '_data'
    groups = json.loads((data / 'publications.json').read_text())
    metrics = json.loads((data / 'scholar_metrics.json').read_text())
    snapshot = fetch(groups)
    groups, metrics = merge(groups, metrics, snapshot, datetime.now(timezone.utc).date().isoformat())
    for name, value in [('publications.json', groups), ('scholar_metrics.json', metrics)]:
        (data / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    print(f"Updated {len(snapshot['papers'])} papers; {snapshot['total']} citations")
