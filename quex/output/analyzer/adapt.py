from   quex.blackboard  import Lng

def do(Txt, OutputDir, OriginalPath=None):
    ## txt = declare_member_functions(txt)
    txt = produce_include_statements(OutputDir, Txt)
    if OriginalPath:
        txt = "%s%s" % (Lng.LINE_PRAGMA(OriginalPath, 1), txt)
    return txt

class Signature:
    def __init__(self, ReturnType, FunctionName, ArgumentList):
        self.return_type   = ReturnType
        self.function_name = FunctionName
        self.argument_list = ArgumentList

    @classmethod
    def from_String(cls, String):
        """SYNTAX: return-type; function-name; argument-list;

        argument-list:   type ':' name ','
        """
        def type_and_name(SubString):
            fields   = [x.strip() for x in SubString.split()]
            type_str = " ".join(fields[:-1])
            name_str = fields[-1]
            return type_str, name_str

        open_i  = String.find("(")
        close_i = String.rfind(")")
        return_type, function_name = type_and_name(String[:open_i])
        argument_list = [ 
            type_and_name(x) 
            for x in String[open_i+1:close_i].split(",") if x.strip()
        ]

        return cls(return_type, function_name, argument_list)

def member_functions(Txt):
    """YIELDS: [0] begin index of letter in 'Txt'
               [1] end index of letter in 'Txt'
               [2] signature of function
    """
    for begin_i, end_i, content in _marked_tags(Txt, "$$MF:", "$$"):
        yield begin_i, end_i, Signature.from_String(content)
    return 

def _marked_tags(Txt, Begin, End):
    """YIELDS: [0] begin index of letter in 'Txt'
               [1] end index of letter in 'Txt'
               [2] signature of function
    """
    BeginL  = len(Begin)
    start_i = -1
    while 1 + 1 == 2:
        begin_i = Txt.find(Begin, start_i+1)
        if begin_i == -1: break
        end_i   = Txt.find(End, begin_i+1)
        if end_i == -1: break
        yield begin_i, end_i+2, Txt[begin_i+BeginL:end_i]
        start_i = end_i + 2
    return 

def declare_member_functions(Txt):
    """RETURNS: [0] 'Txt' with member function declarations replaced.
                [1] list of function signatures in the sequence of their appearance.
    """
    txt = []
    signature_list = []
    last_i = 0
    for begin_i, end_i, signature in member_functions(Txt):
        if signature is None: continue
        txt.append(Txt[last_i:begin_i])
        decl_txt = Lng.MEMBER_FUNCTION_DECLARATION(signature)
        decl_txt = decl_txt.replace("QUEX_NAME_Mode_", "QUEX_NAME(Mode)")
        txt.append(decl_txt)
        last_i = end_i
        signature_list.append(signature)
    txt.append(Txt[last_i:])
    return "".join(txt), signature_list

def produce_include_statements(OutputDir, Txt):
    assert OutputDir != "--"
    if not Txt: return Txt

    txt = []
    # include_file_list = []
    last_i = 0
    for begin_i, end_i, path in _marked_tags(Txt, "$$INC:", "$$"):
        if path is None: continue
        local_path = "%s/lib/%s" % (OutputDir, path.strip())
        txt.append(Txt[last_i:begin_i])
        txt.append(Lng.INCLUDE(local_path))
        last_i = Txt.find("\n", end_i) # Step beyond the '\n'
        # include_file_list.append(local_path)
    txt.append(Txt[last_i:])
    return "".join(txt)
