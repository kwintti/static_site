class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not implemented")

    def props_to_html_method(self):
        output = ""
        for i, val in self.props.items():
            output += " " + i + '="' + val + '"'
        if self.props:
            return output

    def __repr__(self):
        print(self.tag, self.value, self.children, self.props)


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None,  props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        props = ""
        if self.tag is None:
            return self.value
        if self.props:
            for i, val in self.props.items():
                props += " " + i + '="' + val + '"'

        tag_open = "<" + self.tag
        tag_close = "</" + self.tag + ">"
        output = tag_open + props + ">" + self.value + tag_close
        return output


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Not tag provided")
        if self.children is None:
            raise ValueError("Children is not provided") 
        tag_open = "<" + self.tag
        tag_close = "</" + self.tag + ">"
        props = ""
        nodes = ""
        if self.props:
            for i, val in self.props.items():
                props += " " + i + '="' + val + '"'
        for node in self.children:
            nodes += node.to_html()
        output = tag_open + props + ">" + nodes + tag_close
        return output
