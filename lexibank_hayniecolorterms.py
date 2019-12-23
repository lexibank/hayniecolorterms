from pathlib import Path
import pylexibank

SUPPLEMENT = "http://www.pnas.org/content/suppl/2016/11/10/1613666113.DCSupplemental/pnas.1613666113.st01.docx"

class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "hayniecolorterms"

    # define the way in which forms should be handled
    form_spec = pylexibank.FormSpec(
        brackets={"(": ")", "[": "]"},  # characters that function as brackets
        separators=";/,",  # characters that split forms e.g. "a, b".
        missing_data=('?', '-'),  # characters that denote missing data.
        strip_inside_brackets=True   # do you want data removed in brackets or not?
    )

    def cmd_download(self, args):
        # Note this downloads the raw data, but we're using a hand-edited version,
        # so make this a no-op.
        # self.raw_dir.download(SUPPLEMENT, "pnas.1613666113.st01.docx")
        pass
    
    def cmd_makecldf(self, args):
        args.writer.add_sources()
        languages = args.writer.add_languages(lookup_factory="Name")
        
        # TODO concepts
        
        for row in self.raw_dir.read_csv("pnas.1613666113.st01.txt", dicts=True, delimiter="\t"):
            lang = row.pop("")
            for concept in row:
                lex = args.writer.add_forms_from_value(
                    Language_ID=languages[lang],
                    Parameter_ID=concept,
                    Value=row[concept],
                    Source=['Haynie2016'],
                )
