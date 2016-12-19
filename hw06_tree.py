class Tree:
    class _Node:
        def __init__(self,element,parent=None,children=None, state=None, player=None):
            """
            generates a node of the general tree

            :param _element: the element(game board) stored in the node
            :param _parent: the parent  node of this node
            :param _children: a python list of nodes of all the children of this node
            :param _state: the state/score of the node
            :param _player: the player who will make a move on this board/node
            """
            self._element = element
            self._parent = parent
            if children is None:
                self._children = []
            self._state = state
            self._player = player

    class Position:
        """represents the position of a single node(for users to access the node)"""
        def __init__(self, container, node):
            self._container = container
            self._node = node

        def element(self):
            """returns the element in the node"""
            return self._node._element

        def state(self):
            """returns the state/score of the node"""
            return self._node._state

        def player(self):
            """returns the player of this node/board"""
            return self._node._player

        def __eq__(self, other):
            """Return True if other is a Position representing the same location."""
            return type(other) is type(self) and other._node is self._node

    def _validate(self,p):
        """
        Return assiciated node, if position is valid
        """
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:  # convention for deprecated nodes
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        """Return Position instance for given node(or None if no node)"""
        return self.Position(self, node) if node is not None else None

    def __init__(self):
        self._root = None
        self._size = 0

    def __len__(self):
        """allows len() to give the total number of nodes in the tree"""
        return self._size

    def is_empty(self):
        """returns True if the tree is empty"""
        return self._size == 0

    def add_root(self, e):
        """
        Place element e at the root of an empty tree and return new Position.
        Raise ValueError if tree nonempty.
        """
        if self._root is not None:
            raise ValueError('Root exists')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def root(self):
        """Return the root Position of the tree(or None if tree is empty)
        """
        return self._make_position(self._root)

    def parent(self,p):
        """Return the Position of p's parent(or None if p is root)"""
        node = self._validate(p)
        return self._make_position(node._parent)

    def is_root(self,p):
        """Return True if Position p represents the root of the tree."""
        return self.root() == p

    def is_leaf(self,p):
        """Return True if Position p does not have any children."""
        node = self._validate(p)
        return self.children_num(p) == 0

    def get_element(self,p):
        """Return the element in the node of given position"""
        self._validate(p)
        return p.element()

    def full_board(self,p):
        """returns True if the board is full"""
        board = self.get_element(p)
        for row in board:
            for col in row:
                if col == ' ':
                    return False
        return True

    def children(self,parent):
        """Generate an iteration of Positions representing p's children.(p is the position of the parent)"""
        node = self._validate(parent)
        children_pos_list = [self._make_position(child) for child in node._children]
        for child in children_pos_list:
            yield child

    def children_num(self,p):
        """Return the number of children of givne parent"""
        counter = 0
        for child in self.children(p):
            counter += 1
        return counter

    def add_child(self, element, parent):
        """add the position of child to the given parent"""
        parent_node = self._validate(parent)
        child_node = self._Node(element,parent_node)
        parent_node._children.append(child_node)
        self._size += 1

    def depth(self,p):
        """Return the number of levels separating Position p from the root."""
        return 0 if self.is_root(p) else 1 + self.depth(self.parent(p))

    def _height2(self, p):  # time is linear in size of subtree
        """Return the height of the subtree rooted at Position p."""
        if self.is_leaf(p):
            return 0
        else:
            return 1 + max(self._height2(c) for c in self.children(p))

    def height(self, p=None):
        """
        Return the height of the subtree rooted at Position p.
        If p is None, return the height of the entire tree.
        """
        if p is None:
            p = self.root()
        return self._height2(p)        # start _height2 recursion

    def state_update(self, p, state):
        """update the state/score of a node given the position"""
        node = self._validate(p)
        node._state = state

    def get_state(self,p):
        """returns the score/state of a node given the position"""
        self._validate(p)
        return p.state()

    def player_update(self,p,player):
        """update the player who will make a move in node of the given position"""
        node = self._validate(p)
        node._player = player

    def get_player(self,p):
        """returns the player who will make a move in the node of the given position"""
        self._validate(p)
        return p.player()