class LeafNode:
    def __init__(self, tag = None, value = None, children = None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __str__(self):
        attr_str = ' '.join(f'{key}="{value}"' for key, value in self.props.items())
        attr_str = f' {attr_str}' if attr_str else ''
        if isinstance(self.children, str):
            return f'<{self.tag}{attr_str}>{self.value}{self.children}</{self.tag}>'
        else:
            inner_html = ''.join(str(item) for item in self.children)
            return f'<{self.tag}{attr_str}>{self.value}{inner_html}</{self.tag}>'

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    def to_html(self):
        """
        Convert the HTMLNode to an HTML string.
        """
        # return str(self)
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        """
        Convert the props of the HTMLNode to an HTML string.
        """
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def add_child(self, child):
        """
        Add a child node to the HTMLNode.
        """
        self.children.append(child)
