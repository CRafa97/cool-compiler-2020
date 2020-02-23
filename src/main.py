from tools.reader import Reader
from cl_lexer import CoolLexer
from cl_parser import CoolParser
from pipeline import Pipeline

import sys

def main():
    program = sys.argv[1]
    
    pipeline = Pipeline()

    pipeline.submit_state(Reader('Reader'))
    pipeline.submit_state(CoolParser('Parser'))

    pipeline.run_pipeline(program)
    pipeline.report_errors()

    if pipeline.pipeline_errors:
        exit(1)

if __name__ == "__main__":
    main()