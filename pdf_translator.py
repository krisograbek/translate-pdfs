import pdfplumber
from googletrans import Translator, LANGUAGES
from googletrans.models import Translated
from googletrans.constants import DEFAULT_USER_AGENT
import requests


class PDFTranslator:
    def __init__(self, source_pdf, target_language):
        self.source_pdf = source_pdf
        self.target_language = target_language
        self.translator = Translator()
        self.url = "http://translate.googleapis.com/translate_a/single"

    def _translate_text(self, text, src="nl", dest="pl"):
        if src == dest:
            return Translated(
                src=src, dest=dest, origin=text, text=text, pronunciation=text
            )

        headers = {
            "User-Agent": DEFAULT_USER_AGENT,
        }

        print("Language origin:", src)
        print("Language destination:", dest)

        params = {
            "client": "gtx",
            "sl": src,
            "tl": dest,
            "dt": "t",
            "q": text,
        }

        r = requests.get(self.url, params=params, headers=headers)
        if r.status_code != 200:
            return Translated(
                src=src,
                dest=dest,
                origin=text,
                text="Error translating this segment.",
                pronunciation=text,
            )

        result = r.json()[0]
        translated_text = "".join([item[0] for item in result])
        return Translated(
            src=src, dest=dest, origin=text, text=translated_text, pronunciation=text
        )

    def translate(self):
        translated_text = ""

        with pdfplumber.open(self.source_pdf) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                translated_text += (
                    self._translate_text(text, src="nl", dest=self.target_language).text
                    + "\n\n"
                )

        return translated_text
