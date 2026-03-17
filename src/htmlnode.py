class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag=tag 
        self.value=value 
        self.children=children 
        self.props =props  
    def to_html(self):
        raise NotImplementedError("not")
    def props_to_html(self):
        if not self.props:
            return ""
        res=""
        for item,value in self.props.items():
            res+=f"{item}: {value} "
        return res
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"
