from   quex.engine.misc.tools import typed
from   quex.blackboard        import Lng, setup as Setup
import os

def do(Txt, OutputDir, OriginalPath=None):
    if not Txt: return Txt
    ## txt = declare_member_functions(txt)
    txt = produce_include_statements(OutputDir, Txt)
    txt = Lng.adapt_to_configuration(txt)
    if OriginalPath and Setup._debug_reference_original_paths_f:
        txt = "%s\n%s" % (Lng.LINE_PRAGMA(OriginalPath, 1), txt)
    return txt

class Symbol:
    @classmethod
    def type_and_name(cls, SubString):
        idx = SubString.find("=")
        if idx != -1:
            core_str    = SubString[:idx]
            default_str = SubString[idx+1:].strip()
        else:
            core_str    = SubString
            default_str = ""

        fields   = [x.strip() for x in core_str.split()]
        type_str = " ".join(fields[:-1])
        name_str = fields[-1]

        return type_str, name_str, default_str

    @classmethod
    def condition_str(cls, SubString):
        begin_i = SubString.find("<")
        if begin_i == -1: return None, SubString
        end_i     = SubString.find(">")
        condition = SubString[begin_i+1: end_i].strip()
        return condition, SubString[end_i+1:]

class Variable(Symbol):
    @typed(ConstantF=bool)
    def __init__(self, Type, Name, Size, Condition, ConstantF):
        self.type          = Type
        self.name          = Name
        self.size          = Size # None => scalar, else array.
        self.condition     = Condition
        self.constant_f    = ConstantF    # Does not change object's state

    @classmethod
    def from_String(cls, String):
        """SYNTAX: return-type; function-name; argument-list [const];

        argument-list:   type name [ '=' default ]','
        """
        condition,         \
        remainder          = cls.condition_str(String)
        variable_type,     \
        variable_name,     \
        initial_assignment = cls.type_and_name(remainder)

        remainder  = String.strip()
        constant_f = (remainder == "const")

        return cls(variable_type, variable_name, initial_assignment, 
                   condition, constant_f)

def member_variables(Txt):
    """YIELDS: [0] begin index of letter in 'Txt'
               [1] end index of letter in 'Txt'
               [2] signature of function
    """
    for begin_i, end_i, content in _marked_tags(Txt, "$$M:", "$$"):
        yield begin_i, end_i, Variable.from_String(content)
    return 

class Signature(Symbol):
    @typed(ConstantF=bool)
    def __init__(self, ReturnType, FunctionName, ArgumentList, Condition, ConstantF):
        self.return_type   = ReturnType
        self.function_name = FunctionName
        self.argument_list = ArgumentList # (type, name, default)
        self.condition     = Condition
        self.constant_f    = ConstantF    # Does not change object's state

    @classmethod
    def from_String(cls, String):
        """SYNTAX: return-type; function-name; argument-list [const];

        argument-list:   type name [ '=' default ]','
        """
        condition, string = cls.condition_str(String)

        open_i  = string.find("(")
        close_i = string.rfind(")")
        return_type, function_name, default_str = cls.type_and_name(string[:open_i])
        argument_list = [ 
            cls.type_and_name(x) 
            for x in string[open_i+1:close_i].split(",") if x.strip()
        ]

        remainder  = string[close_i+1:].strip()
        constant_f = (remainder == "const")

        return cls(return_type, function_name, argument_list, condition, constant_f)

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

def declare_member_variables(Txt):
    """RETURNS: 'Txt' with member variables declarations replaced.
    """
    txt = []
    last_i = 0
    for begin_i, end_i, signature in declare_member_variables(Txt):
        if signature is None: continue
        txt.append(Txt[last_i:begin_i])
        decl_txt = Lng.MEMBER_FUNCTION_DECLARATION(signature)
        decl_txt = decl_txt.replace("QUEX_NAME_Mode_", "QUEX_NAME(Mode)")
        decl_txt = decl_txt.replace("QUEX_NAME_Converter_", "QUEX_NAME(Converter)")
        decl_txt = decl_txt.replace("QUEX_NAME_ByteLoader_", "QUEX_NAME(ByteLoader)")
        decl_txt = decl_txt.replace("QUEX_NAME_callback_on_token_type_", "QUEX_NAME(callback_on_token_type)")
        txt.append(decl_txt)
        last_i = end_i
    txt.append(Txt[last_i:])
    return "".join(txt)

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
        decl_txt = decl_txt.replace("QUEX_NAME_Converter_", "QUEX_NAME(Converter)")
        decl_txt = decl_txt.replace("QUEX_NAME_ByteLoader_", "QUEX_NAME(ByteLoader)")
        decl_txt = decl_txt.replace("QUEX_NAME_callback_on_token_type_", "QUEX_NAME(callback_on_token_type)")
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
    subdir = "lib"
    for begin_i, end_i, content in _marked_tags(Txt, "$$INC:", "$$"):
        if content is None: continue
        condition, path = Symbol.condition_str(content)
        path       = path.strip()
        local_path = os.path.join(OutputDir, subdir, path.strip())
        txt.append(Txt[last_i:begin_i])
        txt.append(Lng.INCLUDE(local_path, condition))
        last_i = Txt.find("\n", end_i) # Step beyond the '\n'
        # include_file_list.append(local_path)
    txt.append(Txt[last_i:])
    return "".join(txt)

