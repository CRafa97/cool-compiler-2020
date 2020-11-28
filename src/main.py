from pipeline import Pipeline
from tools.reader import Reader
from cl_lexer import CoolLexer
from cl_parser import CoolParser
from visitors import *

import sys

def main():
    program = sys.argv[1]

    # out_program = sys.argv[2]

    # mkdir(out_program, mode=0o777, *, dir_fd=None)

    # fd = open(out_program, 'rw')
    
    pipeline = Pipeline()

    pipeline.submit_state(Reader('Reader'))
    pipeline.submit_state(CoolParser('Parser'))
    pipeline.submit_state(TypeCollector('TCollector'))
    pipeline.submit_state(TypeBuilder('TBuilder'))
    pipeline.submit_state(VarCollector('VCollector'))
    pipeline.submit_state(TypeChecker('TChecker'))

    #temporal
    try:
        ast, context, scope = pipeline.run_pipeline(program)
    except:
        pass

    pipeline.report_errors()

    if pipeline.pipeline_errors:
        exit(1)
    else:
        cv = codeVisitor(context)
        cv.visit(ast)

        mips = MIPS(cv.code, cv.data)
        code = mips.start()

        # for c in cv.data:
        #     print(str(c))
        # for c in cv.code:
        #     print(str(c))

        path = program[:-1]
        path = path[:-1]
        path += 'mips'
        # print(path)
        f = open(path, "w+")

        for line in code:
            f.write(line)
        
        f.close()

        # except:
        #     pass

    

    # print('-------------------Done mips-------------------------------')
    # for line in code:
    #     print(code)
# except:
#     pass


if __name__ == "__main__":
    main()