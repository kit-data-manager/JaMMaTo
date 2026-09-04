import logging


class ParserFactory:
    """Registry and factory for JaMMaTo image parsers."""

    available_img_parsers = {}

    @classmethod
    def register_imgparser(cls, name, parser_cls):
        cls.available_img_parsers[name] = parser_cls

    @classmethod
    def create_img_parser(cls, parser_name, **kwargs):
        parser_class = cls.available_img_parsers.get(parser_name)
        if parser_class is None:
            logging.error(
                "Parser not available: %s. Available parsers: %s",
                parser_name,
                list(cls.available_img_parsers),
            )
            raise ValueError(f"Parser {parser_name} not found")
        return parser_class(**kwargs)
