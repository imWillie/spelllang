# spelllang
# SpellLang Documentation

Welcome to **SpellLang**, a magical programming language inspired by the enchanting world of Harry Potter. SpellLang transforms coding into a spellcasting experience, allowing you to create and execute programs using wizarding terminology and concepts. Whether you're a seasoned developer or a Hogwarts enthusiast, SpellLang offers a unique and captivating way to bring your ideas to life.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Basic Syntax](#basic-syntax)
    - [Variables](#variables)
    - [Data Types](#data-types)
4. [Control Structures](#control-structures)
    - [If Statements](#if-statements)
    - [Loops](#loops)
        - [For Loop (`Loopus`)](#for-loop-loopus)
        - [While Loop (`Persistus`)](#while-loop-persistus)
5. [Functions (Incantations)](#functions-incantations)
6. [Object-Oriented Programming](#object-oriented-programming)
    - [Classes (`Magical Creatures`)](#classes-magical-creatures)
    - [Inheritance (`Bloodlines`)](#inheritance-bloodlines)
7. [Data Structures](#data-structures)
    - [Lists (`Cauldron`)](#lists-cauldron)
    - [Dictionaries (`SpellBooks`)](#dictionaries-spellbooks)
8. [Error Handling](#error-handling)
    - [Try-Catch (`Protego-Alohomora`)](#try-catch-protego-alohomora)
9. [Built-in Functions (Spells)](#built-in-functions-spells)
10. [Comments and Multi-line Strings](#comments-and-multi-line-strings)
11. [Example Programs](#example-programs)
12. [Running SpellLang Programs](#running-spelllang-programs)
13. [Future Enhancements](#future-enhancements)
14. [Conclusion](#conclusion)

---

## Introduction

**SpellLang** is designed to merge the world of programming with the magic of Harry Potter. By using spell-inspired keywords and structures, SpellLang makes coding feel like casting spells. This documentation will guide you through the language's features, syntax, and best practices to help you master SpellLang.

---

## Getting Started

### Prerequisites

- **Python 3.x** installed on your system.
- Basic knowledge of programming concepts.

### Installation

1. **Download the Interpreter:**
   
   Save the optimized interpreter code provided in `spelllang_interpreter.py`.

2. **Set Up Your Environment:**
   
   Ensure that Python is added to your system's PATH. You can verify this by running:

   ```bash
   python --version

    Create Your First SpellLang Program:

    Create a file named hello.spell with the following content:

# Declare a wand (variable)
Wand greeting = "Hello, Hogwarts!"

# Illuminate (print) the greeting
Illuminate(greeting)

Run the Interpreter:

Execute your SpellLang program using the command line:

python spelllang_interpreter.py hello.spell

Expected Output:

Hello, Hogwarts!

Basic Syntax
Variables

Variables in SpellLang are referred to as Wands. They store data that can be used and manipulated throughout your program.

Syntax:

Wand <variable_name> = <value>

Example:

Wand harry = "Harry Potter"
Wand age = 17

Data Types

SpellLang supports various data types, including:

    Strings: Enclosed in double quotes (" ").
    Numbers: Integer values.
    Lists (Cauldron): Ordered collections of items.
    Dictionaries (SpellBooks): Key-value pairs for storing related data.

Examples:

Wand name = "Hermione Granger"       # String
Wand score = 95                       # Number
Cauldron spells = ["Expelliarmus", "Lumos", "Expecto Patronum"]  # List
SpellBooks wizard_ages = {
    "Harry": 17,
    "Ron": 18,
    "Hermione": 19
}                                     # Dictionary

Control Structures
If Statements

Conditional execution is handled using Ifar and Elsear.

Syntax:

Ifar <condition> {
    # Code to execute if condition is true
} Elsear {
    # Code to execute if condition is false
}

Example:

Ifar age >= 17 {
    Illuminate("You're ready to attend Hogwarts.")
} Elsear {
    Illuminate("You are too young for Hogwarts.")
}

Loops
For Loop (Loopus)

The Loopus keyword creates a for-loop, allowing iteration over a range or collection.

Syntax:

Loopus <initialization>; <condition>; <increment> {
    # Code to execute in each iteration
}

Example:

Loopus i = 0; i < 5; i = i + 1 {
    Illuminate("Counting: " + str(i))
}

While Loop (Persistus)

The Persistus keyword creates a while-loop, executing code repeatedly while a condition remains true.

Syntax:

Persistus <condition> {
    # Code to execute while condition is true
}

Example:

Persistus counter >= 1 {
    Illuminate("Counting down: " + str(counter))
    counter = counter - 1
}

Functions (Incantations)

Functions in SpellLang are called Incantations. They allow you to encapsulate reusable code blocks.

Syntax:

Incantation <function_name>(<parameters>) {
    # Function body
}

Example:

Incantation greet(name) {
    Illuminate("Hello, " + name + "!")
}

# Calling the function
Cast greet("Ron")

Object-Oriented Programming
Classes (Magical Creatures)

Classes in SpellLang are referred to as Magical Creatures. They define blueprints for creating objects with specific attributes and behaviors.

Syntax:

Magical Creature <ClassName>(<parameters>) {
    # Class body (methods and attributes)
}

Example:

Magical Creature Wizard(name, house) {
    Illuminate("A wizard named " + name + " from " + house + " house has arrived.")

    Incantation cast_spell(spell) {
        Illuminate(name + " casts " + spell + "!")
    }
}

# Creating an instance of the class
Wand harry = Cast Wizard("Harry", "Gryffindor")
harry.cast_spell("Expecto Patronum")

Inheritance (Bloodlines)

Inheritance allows a class to inherit attributes and methods from another class using the Bloodline keyword.

Syntax:

Magical Creature <ChildClass>(<parameters>) Bloodline <ParentClass> {
    # Additional attributes and methods
}

Example:

Magical Creature ElderWizard(name, house) Bloodline Wizard {
    Incantation perform_ritual(ritual) {
        Illuminate(name + " performs the " + ritual + " ritual.")
    }
}

# Creating an instance of the subclass
Wand albus = Cast ElderWizard("Albus Dumbledore", "Gryffindor")
albus.cast_spell("Fawkes")
albus.perform_ritual("Phoenix")

Data Structures
Lists (Cauldron)

Cauldron represents an ordered collection of items. You can perform operations like adding, removing, and accessing elements.

Syntax:

Cauldron <list_name> = [<item1>, <item2>, ...]

Example:

Cauldron spells = ["Expecto Patronum", "Wingardium Leviosa", "Expelliarmus"]
Illuminate(spells[0])  # Outputs: Expecto Patronum

Dictionaries (SpellBooks)

SpellBooks are key-value stores, allowing you to map unique keys to specific values.

Syntax:

SpellBooks <dict_name> = {
    "<key1>": <value1>,
    "<key2>": <value2>,
    ...
}

Example:

SpellBooks wizard_ages = {
    "Harry": 17,
    "Ron": 18,
    "Hermione": 19
}
Illuminate(wizard_ages["Harry"])  # Outputs: 17

Error Handling
Try-Catch (Protego-Alohomora)

Handle exceptions gracefully using the Protego and Alohomora keywords, similar to try-catch blocks in other languages.

Syntax:

Protego {
    # Code that may throw an error
} Alohomora {
    # Code to handle the error
}

Example:

Protego {
    Illuminate("Attempting to divide by zero.")
    Wand result = 10 / 0
} Alohomora {
    Illuminate("Caught an error: Division by zero is forbidden!")
}

Built-in Functions (Spells)

SpellLang includes built-in spells (functions) for common operations:

    len(<collection>): Returns the length of a list or dictionary.
    str(<value>): Converts a value to a string.
    int(<value>): Converts a value to an integer.

Examples:

Wand numbers = [1, 2, 3, 4, 5]
Illuminate(len(numbers))  # Outputs: 5

Wand number = 10
Illuminate(str(number))   # Outputs: "10"

Comments and Multi-line Strings
Comments

    Single-line Comments: Use # to add comments to your code.

    # This is a single-line comment

Multi-line Comments: Use /* and */ to add multi-line comments.

    /*
        This is a multi-line comment.
        It spans multiple lines.
    */

Multi-line Strings

Use triple quotes (""") to define multi-line strings.

Example:

Wand prophecy = """
The one with the power to vanquish the Dark Lord approaches...
"""
Illuminate(prophecy)

Example Programs
Example 1: Basic Variables and Printing

# Declare wands (variables)
Wand harry = "Harry Potter"
Wand age = 17

# Print variables
Illuminate("Name: " + harry)
Illuminate("Age: " + str(age))

Output:

Name: Harry Potter
Age: 17

Example 2: Function (Incantation) Usage

# Define an incantation to greet
Incantation greet(name) {
    Illuminate("Hello, " + name + "!")
}

# Call the incantation
Cast greet("Hermione")

Output:

Hello, Hermione!

Example 3: Class and Inheritance

# Define a base class
Magical Creature Wizard(name, house) {
    Illuminate("A wizard named " + name + " from " + house + " house has arrived.")

    Incantation cast_spell(spell) {
        Illuminate(name + " casts " + spell + "!")
    }
}

# Define a subclass with inheritance
Magical Creature ElderWizard(name, house) Bloodline Wizard {
    Incantation perform_ritual(ritual) {
        Illuminate(name + " performs the " + ritual + " ritual.")
    }
}

# Create instances
Wand albus = Cast ElderWizard("Albus Dumbledore", "Gryffindor")
albus.cast_spell("Fawkes")
albus.perform_ritual("Phoenix")

Output:

A wizard named Albus Dumbledore from Gryffindor house has arrived.
Albus Dumbledore casts Fawkes!
Albus Dumbledore performs the Phoenix ritual.

Example 4: Error Handling and Loops

# Try-Catch example
Protego {
    Illuminate("Attempting to access undefined variable.")
    Wand mystery = undefined_variable
} Alohomora {
    Illuminate("Caught an error: Variable 'undefined_variable' is not defined.")
}

# While loop to count down
Persistus counter >= 1 {
    Illuminate("Counting down: " + str(counter))
    counter = counter - 1
}
Illuminate("Liftoff!")

# Multi-line string
Wand prophecy = """
The one with the power to vanquish the Dark Lord approaches...
"""
Illuminate(prophecy)

# Working with Cauldron
Cauldron spells = ["Expecto Patronum", "Wingardium Leviosa", "Expelliarmus"]
Illuminate("Spells in the cauldron:")
Loopus i = 0; i < len(spells); i = i + 1 {
    Illuminate("- " + spells[i])
}

# Working with SpellBooks
SpellBooks wizard_ages = {
    "Harry": 17,
    "Ron": 18,
    "Hermione": 19
}
Illuminate("Wizard Ages:")
Forar wizard, age in wizard_ages {
    Illuminate(wizard + " is " + str(age) + " years old.")
}

Output:

Attempting to access undefined variable.
Caught an error: Variable 'undefined_variable' is not defined.
Counting down: 3
Counting down: 2
Counting down: 1
Liftoff!
The one with the power to vanquish the Dark Lord approaches...
Spells in the cauldron:
- Expecto Patronum
- Wingardium Leviosa
- Expelliarmus
Wizard Ages:
Harry is 17 years old.
Ron is 18 years old.
Hermione is 19 years old.

Running SpellLang Programs

    Write Your SpellLang Code:

    Create a .spell file (e.g., my_program.spell) and write your SpellLang code using your favorite text editor.

    Run the Interpreter:

    Execute your SpellLang program using the command line:

    python spelllang_interpreter.py my_program.spell

    View the Output:

    The interpreter will execute your program and display the output in the terminal.

Future Enhancements

While SpellLang is already feature-rich, there are several areas for future improvement:

    Advanced Object-Oriented Features:
        Encapsulation: Support private and public attributes and methods.
        Polymorphism: Allow objects to be treated as instances of their parent classes.

    Enhanced Standard Library:
        Built-in Spells: Add more built-in functions for mathematical operations, string manipulation, and list handling.

    Garbage Collection and Memory Management:
        Implement automatic memory management to handle object lifetimes and resource cleanup.

    Interactive Features:
        REPL (Read-Eval-Print Loop): Develop an interactive shell for real-time experimentation with SpellLang commands.

    Compiler and Bytecode Interpreter:
        Transition from an interpreter to a compiler or bytecode interpreter for improved performance and additional features like optimization and debugging support.

    Tooling and Documentation:
        SpellLang Documentation: Expand documentation with comprehensive guides, tutorials, and reference materials.
        IDE Support: Develop plugins for code editors with syntax highlighting, auto-completion, and debugging capabilities.

    Error Recovery Mechanisms:
        Implement strategies to recover from errors during parsing and execution, allowing the interpreter to continue running and report multiple errors in a single run.

    Extensibility:
        Allow users to define custom built-in spells or integrate external libraries to extend SpellLang's functionality.

Conclusion

SpellLang bridges the gap between programming and the magical universe of Harry Potter, offering a unique and engaging way to code. By leveraging spell-inspired syntax and structures, SpellLang transforms traditional programming tasks into an enchanting experience. Whether you're casting spells, managing magical creatures, or handling complex data structures, SpellLang provides the tools and flexibility to bring your magical ideas to life.

Embrace the magic of coding with SpellLang and embark on a journey to create spellbinding applications!

Happy Spellcasting and Coding!