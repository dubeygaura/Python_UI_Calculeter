
import tkinter as tk
import math, ast, operator


_ALLOWED_NAMES = {
    'pi': math.pi, 'e': math.e, 'sqrt': math.sqrt,
    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
    'log': math.log, 'log10': math.log10, 'abs': abs, 'round': round
}
_ALLOWED_OPERATORS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}

class SafeEvaluator(ast.NodeVisitor):
    def visit(self, node):
        if isinstance(node, ast.Expression):
            return self.visit(node.body)
        return super().visit(node)
    def visit_BinOp(self, node):
        return _ALLOWED_OPERATORS[type(node.op)](
            self.visit(node.left), self.visit(node.right)
        )
    def visit_UnaryOp(self, node):
        return _ALLOWED_OPERATORS[type(node.op)](self.visit(node.operand))
    def visit_Call(self, node):
        func = _ALLOWED_NAMES[node.func.id]
        args = [self.visit(a) for a in node.args]
        return func(*args)
    def visit_Constant(self, node):
        return node.value
    def visit_Name(self, node):
        return _ALLOWED_NAMES[node.id]

def safe_eval(expr):
    expr = expr.replace('^', '**').replace('×','*').replace('÷','/').replace('√','sqrt')
    return SafeEvaluator().visit(ast.parse(expr, mode='eval'))


class ProCalc(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gaurav Dubey —  Calculator")
        self.geometry("420x500")
        self.resizable(False, False)

        
        self.configure(bg="#0b1220")

        self.expression = ''
        self.display_value = tk.StringVar(value='0')
        self.memory = 0.0

        self._build_ui()
        self.bind_all('<Key>', self._on_key)

    def _build_ui(self):
       
        disp = tk.Label(self, textvariable=self.display_value,
                        font=('Inter', 28), anchor='e',
                        bg="#ffffff", fg="black", relief="sunken")
        disp.pack(fill='x', pady=10, padx=10, ipady=10)

        
        btns = [
            ['MC','MR','M+','÷'],
            ['7','8','9','×'],
            ['4','5','6','-'],
            ['1','2','3','+'],
            ['0','.','%','=']
        ]
        frame = tk.Frame(self, bg="#0b1220")
        frame.pack(expand=True)
        for r,row in enumerate(btns):
            for c,lab in enumerate(row):
                b = tk.Button(frame, text=lab, width=8, height=2,
                              bg="#f8a5c2", fg="black", activebackground="#ffb8d1",
                              command=lambda L=lab: self._on_button(L))
                b.grid(row=r, column=c, padx=5, pady=5, ipadx=5, ipady=5)

        
        ctrl = tk.Frame(self, bg="#0b1220"); ctrl.pack(pady=6)
        for lab,cmd in [
            ('Back', self._back),
            ('C', self._clear),
            ('AC', self._all_clear),
            ('√', lambda:self._on_button('√')),
            ('^', lambda:self._on_button('^'))
        ]:
            tk.Button(ctrl,text=lab,bg="#e84393",fg="white",
                      activebackground="#fd79a8",command=cmd)\
                .pack(side='left',padx=5, ipadx=10, ipady=5)

    
    def _on_button(self, lab):
        if lab=='MC': self.memory=0
        elif lab=='MR': self.expression=str(self.memory); self.display_value.set(self.expression)
        elif lab=='M+':
            try: self.memory+=float(self.display_value.get())
            except: pass
        elif lab=='=': self._calculate()
        elif lab=='C': self._clear()
        elif lab=='AC': self._all_clear()
        elif lab=='√': self.expression+='sqrt('; self.display_value.set(self.expression)
        else:
            token=lab.replace('×','*').replace('÷','/').replace('^','**')
            self.expression+=token; self.display_value.set(self.expression)

    def _back(self): self.expression=self.expression[:-1]; self.display_value.set(self.expression or '0')
    def _clear(self): self.expression=''; self.display_value.set('0')
    def _all_clear(self): self.expression=''; self.display_value.set('0'); self.memory=0

    def _calculate(self):
        try:
            expr=self.expression.replace('%','/100')
            result=safe_eval(expr)
            if isinstance(result,float) and result.is_integer(): result=int(result)
            self.display_value.set(str(result))
            self.expression=str(result)
        except: self.display_value.set('Error'); self.expression=''

    def _on_key(self,e):
        k=e.keysym; ch=e.char
        if ch.isdigit() or ch in '.+-*/':
            self.expression+=ch; self.display_value.set(self.expression)
        elif k in ('Return','KP_Enter'): self._calculate()
        elif k=='BackSpace': self._back()
        elif k=='Escape': self._all_clear()
        elif ch=='^': self.expression+='**'; self.display_value.set(self.expression)

if __name__=='__main__':
    ProCalc().mainloop()
