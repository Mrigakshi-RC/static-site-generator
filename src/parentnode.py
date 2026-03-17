from htmlnode import HTMLNode
from leafnode import LeafNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag,None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError()
        if not self.children:
            raise ValueError("no child? best life")
        else:
            # print(self,"to html")
            return self.to_html_helper()

    def to_html_helper(self):
        res=""
        for child in self.children:
            if isinstance(child, LeafNode):
                res+= child.to_html()
            else:
                res+=child.to_html_helper()
        return f"<{self.tag}{self.props_to_html_tag()}>{res}</{self.tag}>"

    def props_to_html_tag(self):
        if not self.props:
            return ""
        res = ""
        for item, value in self.props.items():
            res += f" {item}={value}"
