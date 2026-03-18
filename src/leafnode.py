from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value,None, props)
    def to_html(self):
        if self.value is None:
            raise ValueError()
        if not self.tag:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html_tag()}>{self.value}</{self.tag}>"
    def props_to_html_tag(self):
        if not self.props:
            return ""
        res=""
        for item,value in self.props.items():
            res+=f" {item}={value}"
        return res
    def props_to_html(self):
        if not self.props:
            return ""
        res=""
        for item,value in self.props.items():
            res+=f"{item}: {value} "
        return res
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props_to_html()})"
