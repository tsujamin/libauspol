from bs4 import BeautifulSoup
from datetime import datetime
import requests
import logging
import re

__author__ = 'Benjamin Roberts'


class LiveMinutes:
    """
    This class provides an abstraction of the Live Draft Minutes offered by the Parliament of Australia

    #TODO add date support
    """

    def __init__(self, url):
        """
        Initialise the LiveMinutes instance

        :param url: the live minutes web page to use
        """
        self.document_id = 0
        self.minutes = {}
        self.minute_url = url

    def get_minutes(self, min_date, flat=False):
        """Get the cached copy of the minutes from the provided date

        :param min_date: date object to retrieve
        :param flat: flatten the return to a single string

        :return: minutes or None
        """

        if min_date not in self.minutes:
            return None

        if flat:
            return self._flatten_minutes(self.minutes[min_date])
        else:
            return self.minutes[min_date]

    def get_live_minutes(self, flat=False):
        """Queries the APH website for todays minutes and update the cached copy

        :param flat: flatten the return to a single string

        :return: the latest minutes or None
        """

        minute_req = requests.get(self.minute_url)

        if minute_req.status_code is not 200:
            return None

        # Parse HTML document
        minute_root = BeautifulSoup(minute_req.text)
        div_box_draft = minute_root.find("div", "box draft")
        minute_date = datetime.strptime(div_box_draft.find_all("p")[1].text,
                                        "%A, %d %B %Y").date()

        # Check if there is an update
        if self._update_document_id(div_box_draft):
            self.minutes[minute_date] = self._parse_program_items(div_box_draft)

        # Check for string flattening
        if flat:
            return self._flatten_minutes(self.minutes[minute_date])
        else:
            return self.minutes[minute_date]

    def _parse_program_items(self, div_box_draft):
        """Parses the "box draft" div and constructs a dictionary of program
        item entries.

        Minutes are represented as a list to avoid timestamp collisions

        :param div_box_draft: element of the live minutes page

        :return: minute list structure
        """
        minutes_list = []

        # Get the date from the 2nd <p> of draft box
        min_date = div_box_draft.find_all("p")[1].text

        for prog_item in div_box_draft.find_all("div", "programItem itemRow"):
            prog_item_dict = self._parse_item_row(prog_item, min_date)

            # is a program item, resolve children rows
            prog_item_dict["children"] = []
            for div_item_row in prog_item.find_all("div", "itemRow"):
                prog_item_dict["children"].append(
                    self._parse_item_row(div_item_row, min_date))

            # append this programItem to the minutes list
            minutes_list.append(prog_item_dict)

        return minutes_list

    def _parse_item_row(self, div_item_row, min_date):
        """Parses the item_row div, extracting the content and the timestamp

        :param div_item_row: of the element to process

        :param min_date: date in form found on minutes webpage

        :return: Dict with content and timestamp elements
        """
        item_row = {}
        # Get timestamp, use find_all to keep outer tags
        for div_ts in div_item_row.find_all("div", "timeStamp", limit=1):
            item_row["timestamp"] = self._parse_time_stamp(div_ts, min_date)

        for div_cont in div_item_row.find_all("div", "itemContent", limit=1):
            item_row["content"] = self._parse_item_content(div_cont)

        return item_row

    @staticmethod
    def _parse_item_content(item_content):
        """Parses an item_content tag. These are terrible and consist of
        numerous spans with sentence fragments.

        String parsing was trial and error, if the source HTML was properly
        understood a more intelligent parser could be written

        :param item_content: an item_content tag

        :return: reconstructed content string"""

        content = ""
        for p_tag in item_content.find_all("p"):
            for fragment in p_tag.find_all("span"):
                # fragments are weird. This seems to clean them up well
                content += fragment.text.strip("\n\t")
            content += "\n"

        # Remove any trailing or leading new lines
        return content.strip()

    @staticmethod
    def _parse_time_stamp(div_timestamp, min_date):
        """ Parses the timestamp form used by the minutes

        :param div_timestamp: div containing the timestamp string
        :param min_date: date in form found on minutes webpage

        :return: struct_time or None
        """
        time_re = re.compile("(\d{1,2}:\d{2}:\d{2} \w{2})")
        match = time_re.search(div_timestamp.text.strip())
        if match:
            time = match.group(1)
            return datetime.strptime("{0} {1}".format(min_date, time),
                                     "%A, %d %B %Y %I:%M:%S %p")
        else:
            logging.error("failed to parse timestamp: {0}".format(
                div_timestamp.text
            ))
            return None

    def _update_document_id(self, div_box_draft):
        """Extract the document id from the <script> element of the class
        containing the program_items

        :param div_box_draft" element of the live minutes page

        :return: new revision available as boolean
        """

        # Make re to match the id
        id_re = re.compile("var loadedDocumentId = (\d+);")

        for script in div_box_draft.find_all("script"):
            match = id_re.search(script.text)
            if match:
                new_id = int(match.group(1))
                # Check if an update happened
                updated = new_id > self.document_id
                self.document_id = new_id
                return updated

        logging.error("unable to parse document_id")
        return False

    @staticmethod
    def _flatten_minutes(minutes):
        """Flatten the minutes into a single string of text

        :param minutes: minute structure
        :return: minutes as a string
        """

        ret_str = ""
        for i in minutes:
            ret_str += i["content"] + "\n"
            for j in i["children"]:
                ret_str += j["content"] + "\n"

        return ret_str


class HouseOfRepsMinutes(LiveMinutes):
    """Provides an interface to retrieve live House of Representatives minutes
    """
    __minute_url = "http://www.aph.gov.au/Parliamentary_Business/Chamber_documents/Live_Minutes"

    def __init__(self):
        super(HouseOfRepsMinutes, self).__init__(HouseOfRepsMinutes.__minute_url)


class FederationChamberMinutes(LiveMinutes):
    """Provides an interface to retrieve live Federation Chamber minutes
    """
    __minute_url = "http://www.aph.gov.au/Parliamentary_Business/Chamber_documents/Live_Federation_Chamber_Minutes"

    def __init__(self):
        super(FederationChamberMinutes, self).__init__(FederationChamberMinutes.__minute_url)

