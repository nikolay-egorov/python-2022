import ast
import itertools
import networkx as nx
import matplotlib.pyplot as plt

import os

os.environ["PATH"] += os.pathsep + 'V:/Program Files (x86)/Graphviz2.38/bin/'


class Traverser:
    def __init__(self) -> None:
        self.G = nx.DiGraph()
        self.parent = None
        self.stmt_count = 1
        self.op_pref = ""
        self.parent_of_body = None
        self.local_count = 1

        self.mapping = {
            ast.Module: self.visit_module,
            ast.FunctionDef: self.visitFunc,
            ast.arguments: self.visit_args,
            ast.Assign: self.visit_assign,
            ast.BinOp: self.visit_binop,
            ast.For: self.visit_for,
            ast.Constant: self.visit_const,
            ast.Return: self.visit_return,
            ast.Name: self.visit_name,
            ast.Call: self.visit_call
        }

        self.opDict = {
            ast.Sub: "-",
            ast.Add: "+",
            ast.Mult: "*",
            ast.Div: "/",
            ast.Mod: 'mod',
            ast.Or: 'or',
            ast.And: "and",
            ast.BitXor: 'xor',
            ast.Eq: '==',
            ast.NotEq: '!='
        }



    def visit_module(self, module: ast.Module):
        self.visit_elem(module.body)

    def visit_elem(self, elem):
        a = self.mapping[type(elem)]
        return a(elem)

    def visit_assign(self, assgn: ast.Assign):
        node = f"{self.stmt_count}. Assignment"
        prev_stmt_c = self.stmt_count
        # self.stmt_count += 1
        self.G.add_node(node)
        self.G.add_edge(self.parent, node)
        self.local_count = 1

        if len(assgn.targets) == 1:
            i = f'{prev_stmt_c}.{self.local_count}.{self.visit_elem(assgn.targets[0])}'
            self.local_count += 1
            self.G.add_node(i, parent=node)
            self.G.add_edge(node, i)
        else:
            self.G.add_node("Lhs")
            self.G.add_edge(node, 'Lhs')
            for el in assgn.targets:
                i = f'{prev_stmt_c}.{self.local_count}. {self.visit_elem(el)}'
                self.local_count += 1
                self.G.add_node(i, parent='Lhs')
                self.G.add_edge('Lhs', i)

        t = type(assgn.value)
        if t is ast.Name or t is ast.Constant:
            i = f'{prev_stmt_c}.{self.local_count}. {self.visit_elem(assgn.value)}'
            self.stmt_count += 1
            self.G.add_node(i, parent=node)
            self.G.add_edge(node, i)
        else:
            prev_p = self.parent
            self.parent = node
            self.stmt_count += 1
            self.visit_elem(assgn.value)
            self.parent = prev_p
        # print(f"lhs: {assgn.targets}, rhs: {assgn.value}")

    def visit_const(self, el: ast.Constant):
        # print(f"const: {el.value}")
        return f"Const: {el.value}\n"

    def visit_call(self, call: ast.Call):
        # print(f"call: {self.visit_elem(call.func)}")
        node = f"{self.op_pref}\nCall: '{self.visit_elem(call.func)}'"
        self.G.add_node(node)
        self.G.add_edge(self.parent, node)

        if len(call.args) != 0:
            prev_p = self.parent
            self.parent = node
            # print("\targs:")
            for i in call.args:
                if type(i) is ast.Name or type(i) is ast.Constant:
                    el = f"{self.visit_elem(i)}"
                    self.G.add_node(el)
                    self.G.add_edge(node, el)
                else:
                    self.visit_elem(i)
                    self.parent = prev_p

    def visitFunc(self, func: ast.FunctionDef):
        node = f"{self.stmt_count}. FunctionDef\n{func.name}"
        self.G.add_node(node)
        self.G.add_edge(self.parent, node)
        self.parent = node
        self.parent_of_body = self.parent

        # print(f"Func: {func.name}")
        self.G.add_node("Arguments")
        self.G.add_edge(self.parent, "Arguments")
        self.parent = "Arguments"

        self.visit_args(func.args)
        self.stmt_count += 1

        self.parent = node
        # self.G.add_node("body block")
        # self.G.add_edge(self.parent, "body block")
        # self.parent = "body block"

        self.op_pref = "Func"
        self.visit_body(func.body)
        self.parent = node
        self.op_pref = ''

    def visit_arg(self, arg: ast.arg, default):
        if default is not None:
            node = f"{self.stmt_count}.{self.local_count}. Arg: {arg.arg} with default: {default}"
            # print(f"Arg: {arg.arg} with default: {default}")
        else:
            node = f"{self.stmt_count}.{self.local_count}. Arg: {arg.arg}"
            # print(f"Arg: {arg.arg}")
        self.local_count += 1
        self.G.add_node(node)
        self.G.add_edge(self.parent, node)

    def visit_args(self, args: ast.arguments):
        self.local_count = 1
        for a, df in itertools.zip_longest(args.args, args.defaults):
            self.visit_arg(a, df)

    def visit_binop(self, op: ast.BinOp):
        node = f"binOp\n{self.opDict[type(op.op)]}"
        self.G.add_node(node)
        self.G.add_edge(self.parent, node)
        # self.local_count = 1

        el = f"{self.stmt_count - 1}.{self.local_count}. {self.visit_elem(op.left)}"
        self.local_count += 1
        self.G.add_node(el, parent=node)
        self.G.add_edge(node, el)
        el = f"{self.stmt_count - 1}.{self.local_count}. {self.visit_elem(op.right)}"
        self.local_count += 1
        self.G.add_node(el, parent=node)
        self.G.add_edge(node, el)
        # print(f"binop: {op.op} with: lhs: {self.visit_elem(op.left)}, rhs: {self.visit_elem(op.right)}")

    def visit_for(self, for_: ast.For):
        node = f"{self.stmt_count}. For Statement"
        self.stmt_count += 1
        self.G.add_node(node, parent=self.parent)
        self.G.add_edge(self.parent, node)

        prev_p = self.parent
        self.parent = node
        i = f'iteration params'
        self.G.add_node(i)
        self.G.add_edge(self.parent, i)
        self.local_count = 1
        el = f'{self.stmt_count -1}.{self.local_count}. Target\n{self.visit_elem(for_.target)}'
        self.local_count += 1
        self.G.add_node(el)
        self.G.add_edge(i, el)

        # i = f"in\n{self.visit_elem(for_.iter)}"
        # self.G.add_node(i)
        # self.G.add_edge(self.parent, i)
        self.op_pref = "in"
        self.parent = i
        self.visit_elem(for_.iter)
        self.op_pref = 'Loop'
        self.parent = node

        self.visit_body(for_.body)
        self.parent = prev_p

        if len(for_.orelse) != 0:
            i = "OrElse"
            self.G.add_node(i)
            self.G.add_edge(self.parent, i)
            prev_p = self.parent
            self.parent = i
            self.visit_elem(for_.orelse)
            self.parent = prev_p
            # print(f"orelse: {for_.orelse}")

        # print(f"it param: {self.visit_elem(for_.target)}")
        # print(f"it range: {self.visit_elem(for_.iter)}")
        # if for_.orelse is not None:
        #     print(f"orelse: {for_.orelse}")

    def visit_body(self, body):
        node = f"{self.op_pref} statements"
        self.G.add_node(node)
        self.G.add_edge(self.parent, node)
        self.parent = node

        # print("\tbody")
        for el in body:
            self.visit_elem(el)
            self.parent = node

    def visit_return(self, ret: ast.Return):
        node = f"Return\n{self.visit_elem(ret.value)}"
        self.G.add_node(node)
        self.G.add_edge(self.parent_of_body, node)
        # print(f"return: {self.visit_elem(ret.value)}")

    def visit_name(self, n: ast.Name):
        n_ = ast.unparse(n)
        # print(n_)
        return f"Name\n{n_}"

    def process(self, el: ast.Module):
        d = f"{self.stmt_count}. Module decl"
        self.stmt_count += 1
        # self.G.add_node("Module decl")
        # self.parent = "Module decl"
        self.G.add_node(d)
        self.parent = d
        for i in el.body:
            self.visit_elem(i)

        # self.G.remove_nodes_from(list(nx.isolates(self.G)))

    def try_print(self):
        nx.draw(self.G, with_labels=True)
        plt.show()
        p = nx.drawing.nx_pydot.to_pydot(self.G)
        p.write_png('ast.png')
