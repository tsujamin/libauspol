from unittest import TestCase
from bs4 import BeautifulSoup
from auspol.minutes import HouseOfRepsMinutes
import time

__author__ = 'Benjamin Roberts'


class TestMinutes(TestCase):
    def test_get_minutes(self):
        minutes = HouseOfRepsMinutes().get_minutes()
        self.assertIsNotNone(minutes)
        self.assertTrue(len(minutes) > 0)

        # assert types
        for item in minutes:
            self.assertIn("timestamp", item)
            self.assertIsInstance(item["timestamp"], time.struct_time)
            self.assertIn("content", item)
            self.assertTrue(len(item["content"]) > 0)
            self.assertIn("children", item)
            for child in item["children"]:
                self.assertIn("timestamp", child)
                self.assertIsInstance(child["timestamp"], time.struct_time)
                self.assertIn("content", child)
                self.assertTrue(len(child["content"]) > 0)

    def test__parse_program_item(self):
        self.fail()

    def test__update_document_id(self):
        m = HouseOfRepsMinutes()
        # First parse of new document_id should return true as there was an update
        self.assertTrue(m._update_document_id(DOCUMENT_ID_EXAMPLE))
        # Second parse of document_id should return false as same id
        self.assertFalse(m._update_document_id(DOCUMENT_ID_EXAMPLE))

    def test__parse_item_content(self):
        m = HouseOfRepsMinutes()
        item_content = m._parse_item_content(ITEM_CONTENT_EXAMPLE)
        self.assertEqual(item_content, ITEM_CONTENT_EXEMPLAR)

    def test__parse_time_stamp(self):
        m = HouseOfRepsMinutes()
        self.assertIsNotNone(m._parse_time_stamp(TIMESTAMP_EXAMPLE))


DOCUMENT_ID_EXAMPLE = BeautifulSoup("""
<div class="box draft" xmlns:aph="http://aph.gov.au/xsl"><script>
    var loadedDocumentId = 20150305152724;
    $( document ).ready(function() {
</script><div>""")

ITEM_CONTENT_EXAMPLE = BeautifulSoup("""<p style=""><span id="bbbbbb" style="">&nbsp;</span><span id="sdtSpan" class="sdtSpan" title="num:Paragraph-Number"><span
style="">12</span></span></span><span style=""></span><span style="">First anniversary of the loss of Malaysia Airlines Flight
MH370</span><span style=""></span></p><p style=""><span style="">Mr Abbott</span><span style="">&nbsp;</span><span
style="">(</span><span style="">Prime Minister</span><span style="">)</span><span style="">,</span><span style="">&nbsp;</span><span
style="">having amended, by leave, notice No. 3, government business</span><span style="">, moved</span><span style="">—</span><span
style="">That</span><span style="">&nbsp;this House:</span></p><p style=""><span id="222" style=""><span id="333" style="">
</span>(1)<span style=""> </span></span><span style="">note that the 8th of March will mark 12 months since Malaysia Airlines Flight
MH370 disappeared from radar over the South China Sea;</span></p><p style=""><span id="222" style=""><span id="333" style="">
</span>(2)<span style=""> </span></span><span style="">extend&nbsp;</span><span style="">its heartfelt sympathies to the family and
friends of the 239 passengers and crew on board, including six Australian citizens and one Australian resident, who have suffered a
harrowing 12 months of uncertainty and sorrow</span><span style="">;</span></p><p style=""><span id="222" style=""><span id="333"
style=""> </span>(3)<span style=""> </span></span><span style="">acknowledge the hard work and perseverance of all those working on the
international search and recovery effort, led by Australia, to locate the missing aircraft; and</span></p><p style=""><span id="222"
style=""><span id="333" style=""> </span>(4)<span style=""> </span></span><span style="">note the work of Airservices Australia and
their counterparts in Malaysia and Indonesia in leading global efforts</span><span style="">&nbsp;to enhance aircraft flight
tracking.</span></p>
""")

ITEM_CONTENT_EXEMPLAR = """1212
Mr Abbott(Prime Minister),having amended, by leave, notice No. 3, government business, moved—Thatthis House:
(1) note that the 8th of March will mark 12 months since Malaysia Airlines Flight
MH370 disappeared from radar over the South China Sea;
(2) extend its heartfelt sympathies to the family and
friends of the 239 passengers and crew on board, including six Australian citizens and one Australian resident, who have suffered a
harrowing 12 months of uncertainty and sorrow;
(3) acknowledge the hard work and perseverance of all those working on the
international search and recovery effort, led by Australia, to locate the missing aircraft; and
(4) note the work of Airservices Australia and
their counterparts in Malaysia and Indonesia in leading global effortsto enhance aircraft flight
tracking."""

TIMESTAMP_EXAMPLE = BeautifulSoup(
    '<div class="timeStamp">-  11:16:51 AM</div>')