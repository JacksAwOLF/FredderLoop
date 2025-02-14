"""Module containing basic print wrapper to mask sensitive information"""

import os


# This should be only place where "print" is called to avoid leaking sensitive
# information into Github Actions output
def log(*args):
    """Base print wrapper to mask potential emails and Google Drive folder/file id"""
    if "ALLOW_SENSITIVE_OUTPUT" in os.environ:
        # backdoor to allow default printing
        print(" ".join(map(str, args)))
    new_args = []
    for arg in args:
        # mask potential emails
        if "@" in arg:
            # split into chunks
            tmp_arg = arg.split(" ")
            final_tmp_arg = []
            # only remove chunks with "@"
            for a in tmp_arg:
                if "@" in a:
                    final_tmp_arg.append("***")
                else:
                    final_tmp_arg.append(a)
            new_args.append(" ".join(final_tmp_arg))
        else:
            # mask Google Drive folder/file IDs
            # basing numbers off random stackoverflow
            # https://stackoverflow.com/questions/38780572/is-there-any-specific-for-google-drive-file-id#comment133192830_38780572

            # check by chunk
            tmp_arg = arg.split(" ")
            final_tmp_arg = []
            for a in tmp_arg:
                if len(a) == 33 or len(a) == 44:
                    final_tmp_arg.append("***")
                else:
                    final_tmp_arg.append(a)
            potential_new_arg = " ".join(final_tmp_arg)

            # repeat with "/"
            tmp_arg = potential_new_arg.split("/")
            final_tmp_arg = []
            for a in tmp_arg:
                if len(a) == 33 or len(a) == 44:
                    final_tmp_arg.append("***")
                else:
                    final_tmp_arg.append(a)
            new_args.append("/".join(final_tmp_arg))
    print(" ".join(map(str, new_args)))
