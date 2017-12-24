from   quex.input.setup                 import NotificationDB
from   quex.input.code.base             import SourceRef
import quex.engine.misc.error           as     error
from   quex.engine.misc.file_operations import get_file_content_or_die, \
                                               open_file_or_die

from   quex.engine.misc.file_in         import delete_comment
from   quex.blackboard                  import setup as Setup, \
                                               Lng
from   quex.token_db                    import token_id_db, \
                                               token_id_db_enter, \
                                               token_id_foreign_set
from   itertools import chain
import re
import os

def parse(ForeignTokenIdFile):
    """This function tries to interpret an externally defined token id file--if
    there is one. It does this in order to find the names of defined token ids.
    It does some basic interpretation and include file following, but: **it is
    in no way perfect**. Since its only purpose is to avoid warnings about
    token ids that are not defined it is not essential that it may fail
    sometimes.

    It is more like a nice feature that quex tries to find definitions on its
    own.  Nevertheless, it should work in the large majority of cases.
    """
    CommentDelimiterList = Lng.CommentDelimiterList

    # validate(...) ensured, that the file exists.
    work_list      = [ ForeignTokenIdFile ] 
    done_list      = []
    not_found_list = []
    recursive_list = []
    found_db       = {}
    while work_list:
        file_name = work_list.pop()
        file_name = os.path.normpath(file_name)
        if file_name in done_list: continue
        done_list.append(file_name)
        
        fh      = get_file_content_or_die(file_name, Mode     = "rb")
        content = __delete_comments(fh, CommentDelimiterList)
        text    = __get_token_section(content)

        token_id_list = __extract_token_ids(text, file_name)

        __sort_token_ids(token_id_list, file_name, token_id_db, found_db, token_id_foreign_set)

        included_file_name_set = set(Lng.Match_include.findall(content))

        __sort_included_files(included_file_name_set, file_name, done_list, 
                              work_list, not_found_list, recursive_list)

    if Setup.extern_token_id_file_show_f:
        __show_extern_token_id_definitions(found_db)

    __error_detection(not_found_list, recursive_list)

def cut_token_id_prefix(TokenName, FH_Error=False):
    if TokenName.startswith(Setup.token_id_prefix):
        return TokenName[len(Setup.token_id_prefix):]
    elif TokenName.startswith(Setup.token_id_prefix_plain):
        return TokenName[len(Setup.token_id_prefix_plain):]
    elif not FH_Error:
        return TokenName
    else:
        error.log("Token identifier does not begin with token prefix '%s'\n" % Setup.token_id_prefix + \
                  "found: '%s'" % TokenName, FH_Error)

def __delete_comments(Content, CommentDelimiterList):
    content = Content
    for opener, closer in CommentDelimiterList:
        content = delete_comment(content, opener, closer, LeaveNewlineDelimiter=True)
    return content

def __get_token_section(content):
    region_begin_re = Setup.token_id_foreign_definition_file_region_begin_re
    region_end_re   = Setup.token_id_foreign_definition_file_region_end_re
    begin_i         = 0
    end_i           = len(content)
    if region_begin_re is not None:
        match = region_begin_re.search(content)
        if match is not None:
            begin_i = match.end()

    if region_end_re is not None:
        match = region_end_re.search(content, pos=begin_i)
        if match is not None:
            end_i = match.start()

    return content[begin_i:end_i]

def __extract_token_ids(PlainContent, FileName):
    """PlainContent     -- File content without comments.
    """
    DefineRE      = r"#[ \t]*define[ \t]+([^ \t\n\r]+)[ \t]+[^ \t\n]+"
    AssignRE      = r"([^ \t]+)[ \t]*=[ \t]*[^ \t]+"
    EnumRE        = r"enum[^{]*{([^}]*)}"
    EnumConst     = r"([^=, \n\t]+)"
    define_re_obj = re.compile(DefineRE)
    assign_re_obj = re.compile(AssignRE)
    enum_re_obj   = re.compile(EnumRE)
    const_re_obj  = re.compile(EnumConst)

    def check_and_append(found_list, Name):
        if    not Setup.token_id_prefix_plain \
           or Name.startswith(Setup.token_id_prefix_plain) \
           or Name.startswith(Setup.token_id_prefix):
            found_list.append(Name)

    result = []
    for name in chain(define_re_obj.findall(PlainContent), 
                      assign_re_obj.findall(PlainContent)):
        # Either there is no plain token prefix, or it matches well.
        check_and_append(result, name)

    for enum_txt in enum_re_obj.findall(PlainContent):
        for name in const_re_obj.findall(enum_txt):
            check_and_append(result, name.strip())

    return result

def space(L, Name):
    return " " * (L - len(Name))

def __show_extern_token_id_definitions(found_db):
    if not found_db:
        error.log(  "No token ids with prefix '%s' found in " % Setup.token_id_prefix
                  + "'%s' or included files." % Setup.extern_token_id_file, 
                 NoteF=True)
        return

    txt = [] 
    for file_name, result in found_db.iteritems():
        if not result: continue
        result = set(result)
        L = max(map(len, result))
        txt.append("Token ids found in file '%s' {" % file_name)
        for name in sorted(result):
            shorty = cut_token_id_prefix(name)
            fully  = Setup.token_id_prefix + shorty
            txt.append("     %s %s=> '%s'" % (fully, space(L, name), shorty))
        txt.append("}")

    error.log("\n".join(txt), NoteF=True)

def __error_detection(not_found_list, recursive_list):
    ErrorN = NotificationDB.token_id_ignored_files_report
    if ErrorN not in Setup.suppressed_notification_list:
        if not_found_list:
            not_found_list.sort()
            sr = SourceRef(not_found_list[0][0], LineN=not_found_list[0][1]) 
            error.warning("Files not found:", sr)
            for file_name, line_n, included_file in not_found_list:
                error.warning("%s" % included_file, SourceRef(file_name, line_n))

        if recursive_list:
            recursive_list.sort()
            sr = SourceRef(recursive_list[0][0], LineN=recursive_list[0][1]) 
            error.warning("Files recursively included (ignored second inclusion):", 
                          sr)
            for file_name, line_n, included_file in recursive_list:
                error.warning("%s" % included_file, SourceRef(file_name, line_n))

        if not_found_list or recursive_list:
            # source reference is taken from last setting
            error.log("\nQuex does not handle C-Preprocessor instructions.",
                      sr, NoteF=True, DontExitF=True, SuppressCode=ErrorN)

def __sort_included_files(include_file_set, file_name, done_list, work_list, not_found_list, recursive_list):
    #     -- ensure that included files exist and are not included twice
    for included_file in include_file_set:
        normed_included_file = os.path.normpath(included_file)
        if included_file in done_list:
            line_n = __get_line_n_of_include(file_name, included_file)
            recursive_list.append((file_name, line_n, included_file))
        elif not os.access(normed_included_file, os.F_OK): 
            line_n = __get_line_n_of_include(file_name, included_file)
            not_found_list.append((file_name, line_n, included_file))
        elif normed_included_file not in done_list:
            work_list.append(included_file)

def __sort_token_ids(token_id_list, file_name, token_id_db, found_db, token_id_foreign_set):
    found_db[file_name] = token_id_list

    token_id_foreign_set.update(token_id_list)
    for token_name in token_id_list:
        # NOTE: The line number might be wrong, because of the comment deletion
        line_n = 0
        # NOTE: The actual token value is not important, since the token's numeric
        #       identifier is defined in the user's header. We do not care.
        prefix_less_token_name = cut_token_id_prefix(token_name)
        token_id_db_enter(SourceRef(file_name, line_n), 
                          prefix_less_token_name)
    
def __get_line_n_of_include(FileName, IncludedFileName):
    fh = open_file_or_die(FileName, Mode="rb")
    line_n = 0
    for line in fh.readlines():
        line_n += 1
        if Lng.Match_include.search(line) is not None and line.find(IncludedFileName) != -1:
            break
    else:
        # Included file must appear in including file, but tolerate for safety.
        pass

    fh.close()
    return line_n

