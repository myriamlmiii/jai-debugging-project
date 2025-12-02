"""
Person 2 : Debugging features for Jai Language Project
Implements Type Registry (AVL), Object Inspector (BFS), and Template Expansion (DP)
"""

from collections import deque
import time


# ====== AVL TREE - BALANCED TYPE REGISTRY ======

class AVLNode:
    """A node in the AVL tree that stores type info"""
    
    def __init__(self, name, meta=None):
        self.name = name
        self.meta = meta if meta else {}
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    """
    AVL Tree to store types with automatic balancing
    - Insert: O(log n)
    - Search: O(log n)
    - Space: O(n)
    """
    
    def __init__(self):
        self.root = None
        self.count = 0
    
    def add(self, name, meta=None):
        
        self.root = self._add_node(self.root, name, meta)
    
    def _add_node(self, node, name, meta):
        if node is None:
            self.count += 1
            return AVLNode(name, meta)
        
        if name < node.name:
            node.left = self._add_node(node.left, name, meta)
        elif name > node.name:
            node.right = self._add_node(node.right, name, meta)
        else:
            # Type already exists, update metadata
            if meta:
                node.meta.update(meta)
            return node
        
        # Update height and check balance
        node.height = 1 + max(self._get_h(node.left), self._get_h(node.right))
        return self._rebalance(node)
    
    def find(self, name):
       
        node = self._find_node(self.root, name)
        return node.meta if node else None
    
    def _find_node(self, node, name):
        if node is None:
            return None
        if name == node.name:
            return node
        elif name < node.name:
            return self._find_node(node.left, name)
        else:
            return self._find_node(node.right, name)
    
    def _get_h(self, node):
        
        return node.height if node else 0
    
    def _get_balance(self, node):
        
        if node is None:
            return 0
        return self._get_h(node.left) - self._get_h(node.right)
    
    def _rebalance(self, node):
        
        balance = self._get_balance(node)
        
        # Left side too heavy
        if balance > 1:
            if self._get_balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        # Right side too heavy
        if balance < -1:
            if self._get_balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def _rotate_left(self, node):
       
        right = node.right
        node.right = right.left
        right.left = node
        
        node.height = 1 + max(self._get_h(node.left), self._get_h(node.right))
        right.height = 1 + max(self._get_h(right.left), self._get_h(right.right))
        
        return right
    
    def _rotate_right(self, node):
       
        left = node.left
        node.left = left.right
        left.right = node
        
        node.height = 1 + max(self._get_h(node.left), self._get_h(node.right))
        left.height = 1 + max(self._get_h(left.left), self._get_h(left.right))
        
        return left
    
    def all_types(self):
        
        result = []
        self._traverse(self.root, result)
        return result
    
    def _traverse(self, node, result):
        if node is None:
            return
        self._traverse(node.left, result)
        result.append((node.name, node.meta))
        self._traverse(node.right, result)


# ====== SIMPLE BST - FOR COMPARISON ======

class BSTNode:
    
    
    def __init__(self, name, meta=None):
        self.name = name
        self.meta = meta if meta else {}
        self.left = None
        self.right = None


class SimpleBST:
    """
    Basic Binary Search Tree without balancing
    Shows why we need AVL - can get slow!
    - Insert: O(n) worst case
    - Search: O(n) worst case
    - Space: O(n)
    """
    
    def __init__(self):
        self.root = None
        self.count = 0
    
    def add(self, name, meta=None):
        
        if self.root is None:
            self.root = BSTNode(name, meta)
            self.count = 1
        else:
            self._add_to_node(self.root, name, meta)
    
    def _add_to_node(self, node, name, meta):
        if name < node.name:
            if node.left is None:
                node.left = BSTNode(name, meta)
                self.count += 1
            else:
                self._add_to_node(node.left, name, meta)
        elif name > node.name:
            if node.right is None:
                node.right = BSTNode(name, meta)
                self.count += 1
            else:
                self._add_to_node(node.right, name, meta)
        else:
            if meta:
                node.meta.update(meta)
    
    def find(self, name):
        
        node = self._find_node(self.root, name)
        return node.meta if node else None
    
    def _find_node(self, node, name):
        if node is None:
            return None
        if name == node.name:
            return node
        elif name < node.name:
            return self._find_node(node.left, name)
        else:
            return self._find_node(node.right, name)
    
    def all_types(self):
        
        result = []
        self._traverse(self.root, result)
        return result
    
    def _traverse(self, node, result):
        if node is None:
            return
        self._traverse(node.left, result)
        result.append((node.name, node.meta))
        self._traverse(node.right, result)


# ====== BFS OBJECT INSPECTOR ======

class ObjectInspector:
    """
    Look at object internals using BFS
    - Visits attributes level by level
    - Catches circular references
    - Returns nice formatted object structure
    """
    
    def __init__(self, max_depth=10, max_items=1000):
        self.max_depth = max_depth
        self.max_items = max_items
    
    def inspect(self, obj):
       
        visited = set()
        circles = []
        count = [0]
        
        result = self._do_inspect(obj, visited, circles, 0, count)
        result['circles'] = circles
        result['too_big'] = count[0] >= self.max_items
        
        return result
    
    def _do_inspect(self, obj, visited, circles, depth, count):
        
        obj_id = id(obj)
        
        info = {
            'type': type(obj).__name__,
            'value': None,
            'attrs': {}
        }
        
        # Simple types - just show value
        if isinstance(obj, (int, float, str, bool, type(None))):
            info['value'] = repr(obj)
            return info
        
        # Already seen this object? It's circular
        if obj_id in visited:
            circles.append(f"{type(obj).__name__} (id={obj_id})")
            return info
        
        visited.add(obj_id)
        count[0] += 1
        
        # Hit our limits?
        if count[0] > self.max_items or depth > self.max_depth:
            return info
        
        # Now do BFS through attributes
        try:
            q = deque([(obj, depth)])
            attrs = {}
            
            while q:
                curr, curr_depth = q.popleft()
                
                if curr_depth > self.max_depth or count[0] > self.max_items:
                    break
                
                # Get what attributes this object has
                try:
                    obj_attrs = vars(curr)
                except (TypeError, AttributeError):
                    obj_attrs = {}
                
                for attr_name, attr_val in obj_attrs.items():
                    if attr_name in attrs:
                        continue
                    
                    attr_id = id(attr_val)
                    count[0] += 1
                    
                    if attr_id in visited:
                        attrs[attr_name] = f"<circle: {type(attr_val).__name__}>"
                        circles.append(f"{attr_name}: {type(attr_val).__name__}")
                    elif isinstance(attr_val, (int, float, str, bool, type(None))):
                        attrs[attr_name] = repr(attr_val)
                    else:
                        # Dig deeper
                        visited.add(attr_id)
                        try:
                            nested = self._do_inspect(attr_val, visited, circles,
                                                     curr_depth + 1, count)
                            attrs[attr_name] = nested
                            if count[0] > self.max_items:
                                break
                        except:
                            attrs[attr_name] = f"<{type(attr_val).__name__}>"
            
            info['attrs'] = attrs
        except Exception as e:
            info['error'] = str(e)
        
        return info


# ====== TEMPLATE EXPANSION ======

class TemplateExpander:
   
    
    def __init__(self, vars=None):
        self.vars = vars if vars else {}
        self.cache = {}
    
    def expand_simple(self, template):
       
        # No placeholders left?
        if '{{' not in template:
            return template
        
        # Find the first {{
        start = template.find('{{')
        if start == -1:
            return template
        
        # Find matching }}
        end = template.find('}}', start)
        if end == -1:
            return template
        
        # Get variable name
        var_name = template[start+2:end].strip()
        var_value = self.vars.get(var_name, template[start:end+2])
        
        # Keep going with the rest
        before = template[:start]
        after = template[end+2:]
        
        return before + var_value + self.expand_simple(after)
    
    def expand_smart(self, template):
       
        # Check if we've done this already
        if template in self.cache:
            return self.cache[template]
        
        # Go through string once, replacing as we go
        result = []
        i = 0
        
        while i < len(template):
            # Check for placeholder start
            if i < len(template) - 1 and template[i:i+2] == '{{':
                # Find the end
                end = template.find('}}', i)
                if end == -1:
                    result.append(template[i])
                    i += 1
                else:
                    var_name = template[i+2:end].strip()
                    var_value = self.vars.get(var_name, template[i:end+2])
                    result.append(var_value)
                    i = end + 2
            else:
                result.append(template[i])
                i += 1
        
        expanded = ''.join(result)
        self.cache[template] = expanded
        return expanded
    
    def set_vars(self, new_vars):
       
        self.vars = new_vars
        self.cache.clear()
    
    def clear_cache(self):
       
        self.cache.clear()


# ====== COMPARISON FUNCTIONS ======

def compare_trees(type_list):
    """
    Test AVL vs BST insertion speed
    Returns (avl_time, bst_time)
    """
    
    # Test AVL
    avl = AVLTree()
    start = time.perf_counter()
    for t in type_list:
        avl.add(t, {'len': len(t)})
    avl_time = time.perf_counter() - start
    
    # Test BST
    bst = SimpleBST()
    start = time.perf_counter()
    for t in type_list:
        bst.add(t, {'len': len(t)})
    bst_time = time.perf_counter() - start
    
    return avl_time, bst_time


def compare_template_expansion(template, variables):
   
    
    expander = TemplateExpander(variables)
    
    # Simple way
    start = time.perf_counter()
    result1 = expander.expand_simple(template)
    simple_time = time.perf_counter() - start
    
    # Smart way
    expander.clear_cache()
    start = time.perf_counter()
    result2 = expander.expand_smart(template)
    smart_time = time.perf_counter() - start
    
    return simple_time, smart_time
