import re

class Dox2Rst:

    REGEX = re.compile(r"(?P<before>[\s\S]*\n)?(?P<dox>\s*##.*\n(?:\s*#.*)*\n)(?P<def>\s*def.*)(?P<after>[\s\S]*)")

    COMMENT_INDENT_PATTERN = re.compile(r"^\s*#", re.MULTILINE)
    COMMENT_INDENT_SUB = "  \g<0>"

    INDENT_PATTERN = re.compile(r"\s*")
    DOX_CONTINUATION_PREFIX_PATTERN = re.compile(r"( +#) *", re.MULTILINE)


    def convert(self):

        with open("plugins/CuraProfileWriter/CuraProfileWriter.py", "r") as f:
            contents = f.read()
            match = self.REGEX.match(contents)
            if match is not None:
                comment_block = match.group("dox")
                comment_block = self.add_indent(comment_block)
                comment_block = self.convert_comment_block(comment_block)
                contents = "{before}{definition}\n{rst}{after}".format(
                    before=match.group("before"),
                    definition=match.group("def"),
                    rst=comment_block,
                    after=match.group("after")
                )
                print(contents)
            else:
                print("not found")

    def convert_comment_block(self, dox_block: str):
        """

        :param dox_block:
        """
        indent = self.INDENT_PATTERN.search(dox_block)
        if indent is None:
            indent = ""
        else:
            indent = indent.group()

        # replace opening
        output = dox_block.replace("##", '"""')
        output = re.sub(self.DOX_CONTINUATION_PREFIX_PATTERN, indent, output)
        # replace keyword escapes ie. \return -> :return
        output = output.replace('\\', ":")

        output = output.replace(":code", "")
        output = output.replace(":endcode", "")
        # Add closing """
        output = "{before}\n{indent}\"\"\"\n{indent}".format(before=output, indent=indent)
        return output

    def add_indent(self, comment_block: str):
        return re.sub(self.COMMENT_INDENT_PATTERN, self.COMMENT_INDENT_SUB, comment_block)



if __name__ == "__main__":
    Dox2Rst().convert()


