# spelllang_interpreter.py

import sys

class SpellLangInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.classes = {}
        self.current_class = None
        self.call_stack = []

    def run(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
        self.execute_lines(lines)

    def execute_lines(self, lines):
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line or line.startswith("#"):
                i += 1
                continue
            # Handle multi-line comments
            if line.startswith("/*"):
                while i < len(lines) and not lines[i].strip().endswith("*/"):
                    i += 1
                i += 1
                continue
            tokens = line.split()
            command = tokens[0]

            if command == "Wand":
                self.handle_wand(tokens)
            elif command == "Incantation":
                i = self.handle_incantation(lines, i)
            elif command == "Cast":
                self.handle_cast(tokens)
            elif command == "Illuminate":
                self.handle_illuminate(tokens)
            elif command == "Ifar":
                i = self.handle_ifar(lines, i)
            elif command == "Elsear":
                # Else is handled within Ifar
                i += 1
                continue
            elif command == "Loopus":
                i = self.handle_loopus(lines, i)
            elif command == "Persistus":
                i = self.handle_persistus(lines, i)
            elif command == "Cauldron":
                self.handle_cauldron(tokens)
            elif command == "SpellBooks":
                self.handle_spellbooks(tokens)
            elif command == "Protego":
                i = self.handle_protego(lines, i)
            elif command == "Magical":
                if len(tokens) >1 and tokens[1] == "Creature":
                    i = self.handle_magical_creature(lines, i)
                else:
                    print("Unknown Magical command.")
            else:
                print(f"Unknown command: {command}")
            i += 1

    def handle_wand(self, tokens):
        # Syntax: Wand variable = value
        var_name = tokens[1]
        if tokens[2] != "=":
            print("Syntax Error in Wand declaration.")
            return
        value = self.parse_expression(' '.join(tokens[3:]))
        self.variables[var_name] = value

    def handle_cauldron(self, tokens):
        # Syntax: Cauldron variable = [item1, item2, ...]
        var_name = tokens[1]
        if tokens[2] != "=":
            print("Syntax Error in Cauldron declaration.")
            return
        list_content = ' '.join(tokens[3:]).strip()
        if not (list_content.startswith("[") and list_content.endswith("]")):
            print("Syntax Error: Cauldron must be a list enclosed in [].")
            return
        items = list_content[1:-1].split(',')
        parsed_items = [self.parse_value(item.strip()) for item in items]
        self.variables[var_name] = parsed_items

    def handle_spellbooks(self, tokens):
        # Syntax: SpellBooks variable = {key1: value1, key2: value2, ...}
        var_name = tokens[1]
        if tokens[2] != "=":
            print("Syntax Error in SpellBooks declaration.")
            return
        dict_content = ' '.join(tokens[3:]).strip()
        if not (dict_content.startswith("{") and dict_content.endswith("}")):
            print("Syntax Error: SpellBooks must be a dictionary enclosed in {}.")
            return
        items = dict_content[1:-1].split(',')
        parsed_dict = {}
        for item in items:
            if ':' not in item:
                print("Syntax Error: SpellBooks entries must be key: value.")
                continue
            key, value = item.split(':', 1)
            parsed_dict[self.parse_value(key.strip())] = self.parse_value(value.strip())
        self.variables[var_name] = parsed_dict

    def handle_incantation(self, lines, current_index):
        # Syntax: Incantation name(params) {
        line = lines[current_index].strip()
        parts = line.split()
        incantation_def = parts[1]
        func_name, params = incantation_def.split('(')
        params = params.rstrip(')')
        params = params.split(',') if params else []
        params = [p.strip() for p in params]
        # Extract function body
        body = []
        current_index += 1
        while current_index < len(lines):
            line = lines[current_index].strip()
            if line == "}":
                break
            body.append(line)
            current_index += 1
        self.functions[func_name] = {'params': params, 'body': body}
        return current_index

    def handle_cast(self, tokens):
        # Syntax: Cast function(args)
        func_call = ' '.join(tokens[1:])
        func_name, args = func_call.split('(')
        args = args.rstrip(')')
        args = args.split(',') if args else []
        args = [self.parse_expression(arg.strip()) for arg in args]
        # Check if it's a class constructor
        if func_name in self.classes:
            class_def = self.classes[func_name]
            instance = {'__class__': func_name}
            for idx, param in enumerate(class_def['params']):
                if idx < len(args):
                    instance[param] = args[idx]
                else:
                    instance[param] = None
            # Handle methods if needed
            return instance
        elif func_name in self.functions:
            func = self.functions[func_name]
            # Setup local variables
            local_vars = dict(zip(func['params'], args))
            # Save current variables
            saved_vars = self.variables.copy()
            # Update variables with local
            self.variables.update(local_vars)
            # Execute function body
            self.execute_lines(func['body'])
            # Restore variables
            self.variables = saved_vars
        else:
            print(f"Function or class {func_name} not defined.")

    def handle_illuminate(self, tokens):
        # Syntax: Illuminate("message") or Illuminate(variable + "text")
        expression = ' '.join(tokens[1:])
        value = self.parse_expression(expression)
        print(value)

    def handle_ifar(self, lines, current_index):
        # Syntax: Ifar condition {
        line = lines[current_index].strip()
        condition = line[len("Ifar"):].strip()
        if condition.endswith("{"):
            condition = condition[:-1].strip()
        result = self.evaluate_condition(condition)
        # Extract if block
        if_block, next_index = self.extract_block(lines, current_index +1)
        # Check for Elsear
        else_block = []
        if next_index < len(lines):
            line = lines[next_index].strip()
            if line.startswith("Elsear"):
                else_block, final_index = self.extract_block(lines, next_index +1)
                next_index = final_index
        if result:
            self.execute_lines(if_block)
        else:
            self.execute_lines(else_block)
        return next_index -1

    def handle_loopus(self, lines, current_index):
        # Syntax: Loopus initialization; condition; increment {
        line = lines[current_index].strip()
        parts = line.split(None, 1)[1].split('{')[0].strip()
        init, condition, increment = parts.split(';')
        init = init.strip()
        condition = condition.strip()
        increment = increment.strip()
        # Execute initialization
        self.execute_line(init)
        # Extract loop body
        body, next_index = self.extract_block(lines, current_index +1)
        while self.evaluate_condition(condition):
            self.execute_lines(body)
            self.execute_line(increment)
        return next_index -1

    def handle_persistus(self, lines, current_index):
        # Syntax: Persistus condition {
        line = lines[current_index].strip()
        condition = line[len("Persistus"):].strip()
        if condition.endswith("{"):
            condition = condition[:-1].strip()
        # Extract loop body
        body, next_index = self.extract_block(lines, current_index +1)
        while self.evaluate_condition(condition):
            self.execute_lines(body)
        return next_index -1

    def handle_protego(self, lines, current_index):
        # Syntax:
        # Protego {
        #     # try block
        # } Alohomora {
        #     # catch block
        # }
        try_block, i = self.extract_block(lines, current_index +1)
        # Check for Alohomora
        if i < len(lines):
            line = lines[i].strip()
            if line.startswith("Alohomora"):
                catch_block, final_index = self.extract_block(lines, i +1)
                try:
                    self.execute_lines(try_block)
                except Exception as e:
                    self.variables['error'] = str(e)
                    self.execute_lines(catch_block)
                return final_index
        print("Syntax Error: Protego without Alohomora.")
        return i

    def handle_magical_creature(self, lines, current_index):
        # Syntax: Magical Creature ClassName(params) {
        line = lines[current_index].strip()
        parts = line.split()
        class_def = parts[2]
        params = ' '.join(parts[3:]).split('(')[1].rstrip(')').split(',')
        params = [p.strip() for p in params]
        # Extract class body
        body = []
        current_index +=1
        while current_index < len(lines):
            line = lines[current_index].strip()
            if line == "}":
                break
            body.append(line)
            current_index +=1
        # Store class definition
        self.classes[class_def] = {'params': params, 'body': body}
        return current_index

    def execute_line(self, line):
        if not line or line.startswith("#"):
            return
        tokens = line.split()
        command = tokens[0]
        if command == "Wand":
            self.handle_wand(tokens)
        elif command == "Cauldron":
            self.handle_cauldron(tokens)
        elif command == "SpellBooks":
            self.handle_spellbooks(tokens)
        elif command == "Illuminate":
            self.handle_illuminate(tokens)
        else:
            print(f"Unsupported command in loop: {command}")

    def extract_block(self, lines, start_index):
        block = []
        i = start_index
        while i < len(lines):
            line = lines[i].strip()
            if line == "}":
                break
            block.append(line)
            i +=1
        return block, i +1

    def evaluate_condition(self, condition):
        # Replace variables in condition
        for var in self.variables:
            if var in condition:
                condition = condition.replace(var, str(self.variables[var]))
        try:
            return eval(condition)
        except Exception as e:
            print(f"Condition Evaluation Error: {e}")
            return False

    def compare(self, left, right, operator):
        if operator == "==":
            return left == right
        elif operator == "!=":
            return left != right
        elif operator == "<":
            return left < right
        elif operator == ">":
            return left > right
        elif operator == "<=":
            return left <= right
        elif operator == ">=":
            return left >= right
        else:
            return False

    def parse_expression(self, expression):
        # Replace variables with their values
        for var in self.variables:
            if var in expression:
                if isinstance(self.variables[var], str):
                    expression = expression.replace(var, f'"{self.variables[var]}"')
                else:
                    expression = expression.replace(var, str(self.variables[var]))
        try:
            # Evaluate the expression safely
            return eval(expression)
        except Exception as e:
            print(f"Expression Evaluation Error: {e}")
            return None

    def parse_value(self, value):
        # Remove quotes if string
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            return value[1:-1]
        elif value.isdigit():
            return int(value)
        else:
            # Return variable value if exists
            return self.variables.get(value, value)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python spelllang_interpreter.py <filename.spell>")
    else:
        interpreter = SpellLangInterpreter()
        interpreter.run(sys.argv[1])
