import logging

from src.parser.impl.MRI_Parser import MRI_Parser


class ParserFactory:

    available_img_parsers = {
        "MRI_Parser": MRI_Parser
    }

    @staticmethod
    def create_img_parser(parser_name, **kwargs):
        parser_class = ParserFactory.available_img_parsers.get(parser_name)
        if parser_class:
            return parser_class(**kwargs)
        else:
            logging.error("Parser not available: {}. Available parsers: {}".format(parser_name, list(ParserFactory.available_img_parsers.keys())))
            raise ValueError(f"Parser {parser_name} not found")