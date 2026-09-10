from src.parser.ParserFactory import ParserFactory
from src.parser.impl.MRI_Parser import MRI_Parser


available_img_parsers = {
    "MRI_Parser": MRI_Parser
}

def register_parsers():

    for p_name, p_cls in available_img_parsers.items():
        ParserFactory.register_imgparser(p_name, p_cls)
