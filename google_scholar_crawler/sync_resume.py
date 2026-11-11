"""Update a resume's Scholar total while retaining its Word and WPS PDF layout.

Run with the bundled document Python runtime, which supplies lxml and pypdf.
The PDF updater retains text positions and embeds the matching font's digits.
"""

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import tempfile
import zipfile

from lxml import etree
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ByteStringObject, ContentStream, NameObject
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


COUNT = re.compile(r'Google\s*Scholar\s*总引用\s*(\d+)\s*次')
W = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def number_match(text):
    matches = list(COUNT.finditer(text))
    if len(matches) != 1:
        raise ValueError(f'Expected one Scholar total, found {len(matches)}')
    return matches[0]


def update_docx(data, total):
    with zipfile.ZipFile(io.BytesIO(data)) as source:
        xml = source.read('word/document.xml')
        root = etree.fromstring(xml)
        nodes = root.xpath('//w:t', namespaces=W)
        text = ''.join(node.text or '' for node in nodes)
        match = number_match(text)
        old = match[1]
        if old == total:
            return data
        offset = 0
        remaining = total
        # Preserve each text run and all character/paragraph formatting.
        for node in nodes:
            value = node.text or ''
            start = max(0, match.start(1) - offset)
            end = min(len(value), match.end(1) - offset)
            if start < end:
                replacement = remaining if offset + end == match.end(1) else remaining[:end - start]
                remaining = remaining[len(replacement):]
                node.text = value[:start] + replacement + value[end:]
            offset += len(value)
        xml = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
        output = io.BytesIO()
        with zipfile.ZipFile(output, 'w') as target:
            for entry in source.infolist():
                target.writestr(entry, xml if entry.filename == 'word/document.xml' else source.read(entry))
        return output.getvalue()


def font_map(font):
    cmap = font.get_object()['/ToUnicode'].get_data().decode('ascii')
    mapping = {
        bytes.fromhex(code): bytes.fromhex(char).decode('utf-16-be')
        for block in re.findall(r'beginbfchar(.*?)endbfchar', cmap, re.S)
        for code, char in re.findall(r'<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>', block)
    }
    for block in re.findall(r'beginbfrange(.*?)endbfrange', cmap, re.S):
        for start, end, target in re.findall(r'<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>', block):
            for code in range(int(start, 16), int(end, 16) + 1):
                mapping[code.to_bytes(len(start) // 2, 'big')] = chr(int(target, 16) + code - int(start, 16))
    return mapping


def digit_font(writer):
    # Embed all digits because WPS's original subset can omit unused digits.
    path = '/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf'
    pdfmetrics.registerFont(TTFont('ResumeCitationDigits', path))
    buffer = io.BytesIO()
    document = canvas.Canvas(buffer)
    document.setFont('ResumeCitationDigits', 11)
    document.drawString(0, 0, '0123456789')
    document.save()
    page = PdfReader(buffer).pages[0]
    font = next(f for f in page['/Resources']['/Font'].values() if f.get_object().get('/Subtype') == '/TrueType')
    return font.clone(writer)


def update_pdf(data, total):
    reader = PdfReader(io.BytesIO(data))
    writer = PdfWriter(clone_from=reader)
    parts = []
    streams = []
    for page in writer.pages:
        fonts = {name: font_map(font) for name, font in page['/Resources']['/Font'].items()}
        stream = ContentStream(page['/Contents'], writer)
        font = None
        size = None
        stack = []
        for operation_index, (operands, operation) in enumerate(stream.operations):
            if operation == b'q':
                stack.append((font, size))
            elif operation == b'Q':
                font, size = stack.pop()
            elif operation == b'Tf':
                font, size = operands
            elif operation in (b'Tj', b'TJ'):
                strings = operands if operation == b'Tj' else operands[0]
                for index, value in enumerate(strings):
                    if not isinstance(value, (str, bytes)):
                        continue
                    raw = value.original_bytes
                    mapping = fonts[font]
                    width = len(next(iter(mapping)))
                    text = ''.join(mapping.get(raw[i:i + width], '\ufffd') for i in range(0, len(raw), width))
                    parts.append((text, strings, index, page, stream, operation_index, font, size))
        streams.append((page, stream))
    text = ''.join(part[0] for part in parts)
    match = number_match(text)
    if match[1] == total:
        return data
    if len(match[1]) != len(total):
        raise ValueError('PDF citation digit count changed; re-export the updated Word resume with WPS')
    replacement_font = digit_font(writer)
    insertions = {}
    offset = 0
    for value, strings, index, page, stream, operation_index, font, size in parts:
        start = max(0, match.start(1) - offset)
        end = min(len(value), match.end(1) - offset)
        if start < end:
            replacement = total[offset + start - match.start(1):offset + end - match.start(1)]
            revised = value[:start] + replacement + value[end:]
            if not revised.isascii() or not revised.isdigit():
                raise ValueError('Expected citation digits in their own PDF text operand')
            if 'TimesNewRomanPS-BoldMT' not in page['/Resources']['/Font'][font]['/BaseFont']:
                raise ValueError('Unexpected citation font; inspect the updated resume before syncing')
            page['/Resources']['/Font'][NameObject('/ResumeCitations')] = replacement_font
            strings[index] = ByteStringObject(revised.encode('ascii'))
            insertions[(id(stream), operation_index)] = (font, size)
        offset += len(value)
    for page, stream in streams:
        operations = []
        for index, operation in enumerate(stream.operations):
            original_font = insertions.get((id(stream), index))
            if original_font:
                operations.append(([NameObject('/ResumeCitations'), original_font[1]], b'Tf'))
            operations.append(operation)
            if original_font:
                operations.append((list(original_font), b'Tf'))
        stream.operations = operations
        page.replace_contents(stream)
        page.compress_content_streams()
    output = io.BytesIO()
    writer.write(output)
    result = output.getvalue()
    extracted = ''.join(page.extract_text() for page in PdfReader(io.BytesIO(result)).pages)
    assert number_match(extracted)[1] == total
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--metrics', type=Path, required=True)
    parser.add_argument('--docx', type=Path, required=True)
    parser.add_argument('--pdf', type=Path, action='append', required=True)
    parser.add_argument('--backup-dir', type=Path, required=True)
    args = parser.parse_args()
    total = str(json.loads(args.metrics.read_text())['total_citations'])
    if not total.isdigit():
        raise ValueError('Invalid citation total')
    changes = []
    for path, transform in [(args.docx, update_docx), *[(p, update_pdf) for p in args.pdf]]:
        original = path.read_bytes()
        updated = transform(original, total)
        if updated != original:
            changes.append((path, original, updated))
    # Prepare and validate every format before updating any file.
    for path, original, updated in changes:
        if path.read_bytes() != original:
            raise RuntimeError(f'Resume changed during synchronization: {path}')
    args.backup_dir.mkdir(parents=True, exist_ok=True)
    for path, original, updated in changes:
        backup = args.backup_dir / (path.name + '.' + hashlib.sha256(original).hexdigest()[:12])
        if not backup.exists():
            backup.write_bytes(original)
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as temp:
            temp.write(updated)
            temp_path = Path(temp.name)
        os.chmod(temp_path, path.stat().st_mode)
        os.replace(temp_path, path)
        print(f'Updated {path} to {total} citations')
    if not changes:
        print(f'Resume already has {total} citations')


if __name__ == '__main__':
    main()
