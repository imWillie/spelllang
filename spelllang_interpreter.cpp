// spelllang_interpreter.cpp

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <map>
#include <unordered_map>
#include <memory>
#include <cctype>
#include <stdexcept>
#include <functional>

// ======================== Token Definitions ========================

enum class TokenType {
    KEYWORD,
    IDENTIFIER,
    NUMBER,
    STRING,
    OPERATOR,
    DELIMITER,
    EOF_TOKEN
};

struct Token {
    TokenType type;
    std::string value;
    int line;
    int column;

    Token(TokenType type = TokenType::EOF_TOKEN, const std::string& value = "", int line = 0, int column = 0)
        : type(type), value(value), line(line), column(column) {}
};

// ======================== Lexer Implementation ========================

class Lexer {
public:
    Lexer(const std::string& input)
        : input(input), pos(0), line(1), column(1) {}

    std::vector<Token> tokenize() {
        std::vector<Token> tokens;
        while (pos < input.size()) {
            char current = peek();
            if (isspace(current)) {
                consumeWhitespace();
                continue;
            }
            if (current == '#') {
                consumeSingleLineComment();
                continue;
            }
            if (current == '/' && peekNext() == '*') {
                consumeMultiLineComment();
                continue;
            }
            if (isalpha(current) || current == '_') {
                tokens.push_back(consumeIdentifierOrKeyword());
                continue;
            }
            if (isdigit(current)) {
                tokens.push_back(consumeNumber());
                continue;
            }
            if (current == '"' || current == '\'') {
                tokens.push_back(consumeString());
                continue;
            }
            if (isOperatorStart(current)) {
                tokens.push_back(consumeOperator());
                continue;
            }
            if (isDelimiter(current)) {
                tokens.emplace_back(TokenType::DELIMITER, std::string(1, current), line, column);
                advance();
                continue;
            }
            throw std::runtime_error("Unknown character at line " + std::to_string(line) + ", column " + std::to_string(column));
        }
        tokens.emplace_back(TokenType::EOF_TOKEN, "", line, column);
        return tokens;
    }

private:
    std::string input;
    size_t pos;
    int line;
    int column;

    char peek() const {
        if (pos < input.size())
            return input[pos];
        return '\0';
    }

    char peekNext() const {
        if (pos + 1 < input.size())
            return input[pos + 1];
        return '\0';
    }

    void advance() {
        if (pos < input.size()) {
            if (input[pos] == '\n') {
                line++;
                column = 1;
            }
            else {
                column++;
            }
            pos++;
        }
    }

    void consumeWhitespace() {
        while (pos < input.size() && isspace(peek())) {
            advance();
        }
    }

    void consumeSingleLineComment() {
        while (pos < input.size() && peek() != '\n') {
            advance();
        }
    }

    void consumeMultiLineComment() {
        advance(); // consume '/'
        advance(); // consume '*'
        while (pos < input.size()) {
            if (peek() == '*' && peekNext() == '/') {
                advance(); // consume '*'
                advance(); // consume '/'
                break;
            }
            advance();
        }
    }

    Token consumeIdentifierOrKeyword() {
        int startLine = line;
        int startColumn = column;
        std::string value;
        while (pos < input.size() && (isalnum(peek()) || peek() == '_')) {
            value += peek();
            advance();
        }
        if (isKeyword(value)) {
            return Token(TokenType::KEYWORD, value, startLine, startColumn);
        }
        return Token(TokenType::IDENTIFIER, value, startLine, startColumn);
    }

    Token consumeNumber() {
        int startLine = line;
        int startColumn = column;
        std::string value;
        while (pos < input.size() && isdigit(peek())) {
            value += peek();
            advance();
        }
        return Token(TokenType::NUMBER, value, startLine, startColumn);
    }

    Token consumeString() {
        int startLine = line;
        int startColumn = column;
        char quoteType = peek();
        std::string value;
        advance(); // consume opening quote
        while (pos < input.size() && peek() != quoteType) {
            if (peek() == '\\') { // Handle escape sequences
                advance();
                if (pos >= input.size()) break;
                char escaped = peek();
                switch (escaped) {
                    case 'n': value += '\n'; break;
                    case 't': value += '\t'; break;
                    case '"': value += '"'; break;
                    case '\'': value += '\''; break;
                    case '\\': value += '\\'; break;
                    default: value += escaped; break;
                }
            }
            else {
                value += peek();
            }
            advance();
        }
        if (peek() == quoteType)
            advance(); // consume closing quote
        else
            throw std::runtime_error("Unterminated string at line " + std::to_string(startLine) + ", column " + std::to_string(startColumn));
        return Token(TokenType::STRING, value, startLine, startColumn);
    }

    Token consumeOperator() {
        int startLine = line;
        int startColumn = column;
        std::string op;
        op += peek();
        if (isOperator(peek(), peekNext())) {
            op += peekNext();
            advance();
        }
        advance();
        return Token(TokenType::OPERATOR, op, startLine, startColumn);
    }

    bool isOperatorStart(char c) const {
        std::string operators = "=!<>+-*/%&|!:";
        return operators.find(c) != std::string::npos;
    }

    bool isOperator(const char current, const char next) const {
        std::vector<std::string> multiCharOps = {"==", "!=", "<=", ">=", "&&", "||"};
        std::string op = "";
        op += current;
        op += next;
        return std::find(multiCharOps.begin(), multiCharOps.end(), op) != multiCharOps.end();
    }

    bool isDelimiter(char c) const {
        std::string delimiters = "(){},.;[]";
        return delimiters.find(c) != std::string::npos;
    }

    bool isKeyword(const std::string& word) const {
        static const std::vector<std::string> keywords = {
            "Wand", "Incantation", "Cast", "Illuminate", "Ifar", "Elsear",
            "Loopus", "Persistus", "Cauldron", "SpellBooks", "Protego",
            "Alohomora", "Magical", "Creature", "Bloodline", "Forar",
            "in", "len", "str", "int"
        };
        return std::find(keywords.begin(), keywords.end(), word) != keywords.end();
    }
};

// ======================== AST Definitions ========================

class ASTNode {
public:
    int line;
    int column;
    ASTNode(int line = 0, int column = 0) : line(line), column(column) {}
    virtual ~ASTNode() = default;
};

using ASTNodePtr = std::shared_ptr<ASTNode>;

class Program : public ASTNode {
public:
    std::vector<ASTNodePtr> statements;
    Program(const std::vector<ASTNodePtr>& stmts) : statements(stmts) {}
};

class VarDeclaration : public ASTNode {
public:
    std::string var_type;
    std::string name;
    ASTNodePtr value;
    VarDeclaration(const std::string& type, const std::string& name, ASTNodePtr value, int line, int column)
        : var_type(type), name(name), value(value) {
        this->line = line;
        this->column = column;
    }
};

class Assignment : public ASTNode {
public:
    std::string name;
    ASTNodePtr value;
    Assignment(const std::string& name, ASTNodePtr value, int line, int column)
        : name(name), value(value) {
        this->line = line;
        this->column = column;
    }
};

class FunctionDeclaration : public ASTNode {
public:
    std::string name;
    std::vector<std::string> params;
    std::vector<ASTNodePtr> body;
    FunctionDeclaration(const std::string& name, const std::vector<std::string>& params, const std::vector<ASTNodePtr>& body, int line, int column)
        : name(name), params(params), body(body) {
        this->line = line;
        this->column = column;
    }
};

class FunctionCall : public ASTNode {
public:
    std::string name;
    std::vector<ASTNodePtr> args;
    FunctionCall(const std::string& name, const std::vector<ASTNodePtr>& args, int line, int column)
        : name(name), args(args) {
        this->line = line;
        this->column = column;
    }
};

class PrintStatement : public ASTNode {
public:
    ASTNodePtr expression;
    PrintStatement(ASTNodePtr expr, int line, int column)
        : expression(expr) {
        this->line = line;
        this->column = column;
    }
};

class IfStatement : public ASTNode {
public:
    ASTNodePtr condition;
    std::vector<ASTNodePtr> if_body;
    std::vector<ASTNodePtr> else_body;
    IfStatement(ASTNodePtr cond, const std::vector<ASTNodePtr>& if_b, const std::vector<ASTNodePtr>& else_b, int line, int column)
        : condition(cond), if_body(if_b), else_body(else_b) {
        this->line = line;
        this->column = column;
    }
};

class WhileLoop : public ASTNode {
public:
    ASTNodePtr condition;
    std::vector<ASTNodePtr> body;
    WhileLoop(ASTNodePtr cond, const std::vector<ASTNodePtr>& body, int line, int column)
        : condition(cond), body(body) {
        this->line = line;
        this->column = column;
    }
};

class ForLoop : public ASTNode {
public:
    ASTNodePtr initialization;
    ASTNodePtr condition;
    ASTNodePtr increment;
    std::vector<ASTNodePtr> body;
    ForLoop(ASTNodePtr init, ASTNodePtr cond, ASTNodePtr inc, const std::vector<ASTNodePtr>& body, int line, int column)
        : initialization(init), condition(cond), increment(inc), body(body) {
        this->line = line;
        this->column = column;
    }
};

class ClassDeclaration : public ASTNode {
public:
    std::string name;
    std::vector<std::string> params;
    std::vector<ASTNodePtr> body;
    std::string parent;
    ClassDeclaration(const std::string& name, const std::vector<std::string>& params, const std::vector<ASTNodePtr>& body, const std::string& parent, int line, int column)
        : name(name), params(params), body(body), parent(parent) {
        this->line = line;
        this->column = column;
    }
};

class TryCatch : public ASTNode {
public:
    std::vector<ASTNodePtr> try_block;
    std::vector<ASTNodePtr> catch_block;
    TryCatch(const std::vector<ASTNodePtr>& try_b, const std::vector<ASTNodePtr>& catch_b, int line, int column)
        : try_block(try_b), catch_block(catch_b) {
        this->line = line;
        this->column = column;
    }
};

class BinaryOp : public ASTNode {
public:
    std::string op;
    ASTNodePtr left;
    ASTNodePtr right;
    BinaryOp(const std::string& op, ASTNodePtr left, ASTNodePtr right, int line, int column)
        : op(op), left(left), right(right) {
        this->line = line;
        this->column = column;
    }
};

class UnaryOp : public ASTNode {
public:
    std::string op;
    ASTNodePtr operand;
    UnaryOp(const std::string& op, ASTNodePtr operand, int line, int column)
        : op(op), operand(operand) {
        this->line = line;
        this->column = column;
    }
};

class Literal : public ASTNode {
public:
    std::string value;
    Literal(const std::string& value, int line, int column)
        : value(value) {
        this->line = line;
        this->column = column;
    }
};

class NumberLiteral : public ASTNode {
public:
    int value;
    NumberLiteral(int value, int line, int column)
        : value(value) {
        this->line = line;
        this->column = column;
    }
};

class StringLiteral : public ASTNode {
public:
    std::string value;
    StringLiteral(const std::string& value, int line, int column)
        : value(value) {
        this->line = line;
        this->column = column;
    }
};

class Identifier : public ASTNode {
public:
    std::string name;
    Identifier(const std::string& name, int line, int column)
        : name(name) {
        this->line = line;
        this->column = column;
    }
};

// ======================== Parser Implementation ========================

class Parser {
public:
    Parser(const std::vector<Token>& tokens)
        : tokens(tokens), pos(0) {}

    std::shared_ptr<Program> parse() {
        std::vector<ASTNodePtr> statements;
        while (!isAtEnd()) {
            auto stmt = statement();
            if (stmt) {
                statements.push_back(stmt);
            }
        }
        return std::make_shared<Program>(statements);
    }

private:
    std::vector<Token> tokens;
    size_t pos;

    bool isAtEnd() const {
        return peek().type == TokenType::EOF_TOKEN;
    }

    Token peek() const {
        if (pos < tokens.size())
            return tokens[pos];
        return tokens.back();
    }

    Token previous() const {
        if (pos == 0)
            return tokens[0];
        return tokens[pos - 1];
    }

    Token advance() {
        if (!isAtEnd()) pos++;
        return previous();
    }

    bool check(TokenType type, const std::string& value = "") const {
        if (isAtEnd()) return false;
        if (tokens[pos].type != type) return false;
        if (!value.empty() && tokens[pos].value != value) return false;
        return true;
    }

    bool match(TokenType type, const std::string& value = "") {
        if (check(type, value)) {
            advance();
            return true;
        }
        return false;
    }

    void consume(TokenType type, const std::string& value, const std::string& errorMessage) {
        if (check(type, value)) {
            advance();
            return;
        }
        throw std::runtime_error("Parser Error at line " + std::to_string(peek().line) + ", column " + std::to_string(peek().column) + ": " + errorMessage);
    }

    ASTNodePtr statement() {
        if (match(TokenType::KEYWORD, "Wand") ||
            match(TokenType::KEYWORD, "Cauldron") ||
            match(TokenType::KEYWORD, "SpellBooks")) {
            return variableDeclaration();
        }
        if (match(TokenType::KEYWORD, "Incantation")) {
            return functionDeclaration();
        }
        if (match(TokenType::KEYWORD, "Cast")) {
            return functionCallStatement();
        }
        if (match(TokenType::KEYWORD, "Illuminate")) {
            return printStatement();
        }
        if (match(TokenType::KEYWORD, "Ifar")) {
            return ifStatement();
        }
        if (match(TokenType::KEYWORD, "Loopus")) {
            return forLoop();
        }
        if (match(TokenType::KEYWORD, "Persistus")) {
            return whileLoop();
        }
        if (match(TokenType::KEYWORD, "Protego")) {
            return tryCatch();
        }
        if (match(TokenType::KEYWORD, "Magical")) {
            return classDeclaration();
        }
        if (check(TokenType::IDENTIFIER)) {
            return assignment();
        }
        throw std::runtime_error("Unexpected token '" + peek().value + "' at line " + std::to_string(peek().line) + ", column " + std::to_string(peek().column));
    }

    ASTNodePtr variableDeclaration() {
        Token varType = previous();
        Token varName = consumeIdentifier("Expected variable name.");
        consume(TokenType::OPERATOR, "=", "Expected '=' after variable name.");
        ASTNodePtr value = expression();
        return std::make_shared<VarDeclaration>(varType.value, varName.value, value, varType.line, varType.column);
    }

    ASTNodePtr assignment() {
        Token varName = consume(TokenType::IDENTIFIER, "Expected variable name.");
        consume(TokenType::OPERATOR, "=", "Expected '=' after variable name.");
        ASTNodePtr value = expression();
        return std::make_shared<Assignment>(varName.value, value, varName.line, varName.column);
    }

    ASTNodePtr functionDeclaration() {
        Token funcName = consume(TokenType::IDENTIFIER, "Expected function name.");
        consume(TokenType::OPERATOR, "(", "Expected '(' after function name.");
        std::vector<std::string> params;
        if (!check(TokenType::OPERATOR, ")")) {
            do {
                Token param = consume(TokenType::IDENTIFIER, "Expected parameter name.");
                params.push_back(param.value);
            } while (match(TokenType::OPERATOR, ","));
        }
        consume(TokenType::OPERATOR, ")", "Expected ')' after parameters.");
        consume(TokenType::OPERATOR, "{", "Expected '{' before function body.");
        std::vector<ASTNodePtr> body;
        while (!check(TokenType::OPERATOR, "}")) {
            body.push_back(statement());
        }
        consume(TokenType::OPERATOR, "}", "Expected '}' after function body.");
        return std::make_shared<FunctionDeclaration>(funcName.value, params, body, funcName.line, funcName.column);
    }

    ASTNodePtr functionCallStatement() {
        Token funcName = consume(TokenType::IDENTIFIER, "Expected function name.");
        consume(TokenType::OPERATOR, "(", "Expected '(' after function name.");
        std::vector<ASTNodePtr> args;
        if (!check(TokenType::OPERATOR, ")")) {
            do {
                args.push_back(expression());
            } while (match(TokenType::OPERATOR, ","));
        }
        consume(TokenType::OPERATOR, ")", "Expected ')' after arguments.");
        return std::make_shared<FunctionCall>(funcName.value, args, funcName.line, funcName.column);
    }

    ASTNodePtr printStatement() {
        consume(TokenType::OPERATOR, "(", "Expected '(' after 'Illuminate'.");
        ASTNodePtr expr = expression();
        consume(TokenType::OPERATOR, ")", "Expected ')' after expression.");
        return std::make_shared<PrintStatement>(expr, expr->line, expr->column);
    }

    ASTNodePtr ifStatement() {
        ASTNodePtr condition = expression();
        consume(TokenType::OPERATOR, "{", "Expected '{' after condition.");
        std::vector<ASTNodePtr> ifBody;
        while (!check(TokenType::OPERATOR, "}")) {
            ifBody.push_back(statement());
        }
        consume(TokenType::OPERATOR, "}", "Expected '}' after if body.");
        std::vector<ASTNodePtr> elseBody;
        if (match(TokenType::KEYWORD, "Elsear")) {
            consume(TokenType::OPERATOR, "{", "Expected '{' after 'Elsear'.");
            while (!check(TokenType::OPERATOR, "}")) {
                elseBody.push_back(statement());
            }
            consume(TokenType::OPERATOR, "}", "Expected '}' after else body.");
        }
        return std::make_shared<IfStatement>(condition, ifBody, elseBody, condition->line, condition->column);
    }

    ASTNodePtr whileLoop() {
        ASTNodePtr condition = expression();
        consume(TokenType::OPERATOR, "{", "Expected '{' after condition.");
        std::vector<ASTNodePtr> body;
        while (!check(TokenType::OPERATOR, "}")) {
            body.push_back(statement());
        }
        consume(TokenType::OPERATOR, "}", "Expected '}' after while loop body.");
        return std::make_shared<WhileLoop>(condition, body, condition->line, condition->column);
    }

    ASTNodePtr forLoop() {
        ASTNodePtr initialization = expression();
        consume(TokenType::OPERATOR, ";", "Expected ';' after initialization.");
        ASTNodePtr condition = expression();
        consume(TokenType::OPERATOR, ";", "Expected ';' after condition.");
        ASTNodePtr increment = expression();
        consume(TokenType::OPERATOR, "{", "Expected '{' after for loop declaration.");
        std::vector<ASTNodePtr> body;
        while (!check(TokenType::OPERATOR, "}")) {
            body.push_back(statement());
        }
        consume(TokenType::OPERATOR, "}", "Expected '}' after for loop body.");
        return std::make_shared<ForLoop>(initialization, condition, increment, body, initialization->line, initialization->column);
    }

    ASTNodePtr tryCatch() {
        consume(TokenType::OPERATOR, "{", "Expected '{' after 'Protego'.");
        std::vector<ASTNodePtr> tryBlock;
        while (!check(TokenType::OPERATOR, "}")) {
            tryBlock.push_back(statement());
        }
        consume(TokenType::OPERATOR, "}", "Expected '}' after try block.");
        consume(TokenType::KEYWORD, "Alohomora", "Expected 'Alohomora' after try block.");
        consume(TokenType::OPERATOR, "{", "Expected '{' after 'Alohomora'.");
        std::vector<ASTNodePtr> catchBlock;
        while (!check(TokenType::OPERATOR, "}")) {
            catchBlock.push_back(statement());
        }
        consume(TokenType::OPERATOR, "}", "Expected '}' after catch block.");
        return std::make_shared<TryCatch>(tryBlock, catchBlock, tryBlock.empty() ? 0 : tryBlock[0]->line, tryBlock.empty() ? 0 : tryBlock[0]->column);
    }

    ASTNodePtr classDeclaration() {
        consume(TokenType::KEYWORD, "Creature", "Expected 'Creature' after 'Magical'.");
        Token className = consume(TokenType::IDENTIFIER, "Expected class name.");
        consume(TokenType::OPERATOR, "(", "Expected '(' after class name.");
        std::vector<std::string> params;
        if (!check(TokenType::OPERATOR, ")")) {
            do {
                Token param = consume(TokenType::IDENTIFIER, "Expected parameter name.");
                params.push_back(param.value);
            } while (match(TokenType::OPERATOR, ","));
        }
        consume(TokenType::OPERATOR, ")", "Expected ')' after parameters.");
        std::string parent = "";
        if (match(TokenType::KEYWORD, "Bloodline")) {
            Token parentName = consume(TokenType::IDENTIFIER, "Expected parent class name after 'Bloodline'.");
            parent = parentName.value;
        }
        consume(TokenType::OPERATOR, "{", "Expected '{' before class body.");
        std::vector<ASTNodePtr> body;
        while (!check(TokenType::OPERATOR, "}")) {
            body.push_back(statement());
        }
        consume(TokenType::OPERATOR, "}", "Expected '}' after class body.");
        return std::make_shared<ClassDeclaration>(className.value, params, body, parent, className.line, className.column);
    }

    ASTNodePtr expression() {
        return logicalOr();
    }

    ASTNodePtr logicalOr() {
        ASTNodePtr expr = logicalAnd();
        while (match(TokenType::OPERATOR, "||")) {
            Token op = previous();
            ASTNodePtr right = logicalAnd();
            expr = std::make_shared<BinaryOp>(op.value, expr, right, op.line, op.column);
        }
        return expr;
    }

    ASTNodePtr logicalAnd() {
        ASTNodePtr expr = equality();
        while (match(TokenType::OPERATOR, "&&")) {
            Token op = previous();
            ASTNodePtr right = equality();
            expr = std::make_shared<BinaryOp>(op.value, expr, right, op.line, op.column);
        }
        return expr;
    }

    ASTNodePtr equality() {
        ASTNodePtr expr = comparison();
        while (match(TokenType::OPERATOR, "==") || match(TokenType::OPERATOR, "!=")) {
            Token op = previous();
            ASTNodePtr right = comparison();
            expr = std::make_shared<BinaryOp>(op.value, expr, right, op.line, op.column);
        }
        return expr;
    }

    ASTNodePtr comparison() {
        ASTNodePtr expr = term();
        while (match(TokenType::OPERATOR, "<") || match(TokenType::OPERATOR, ">") ||
               match(TokenType::OPERATOR, "<=") || match(TokenType::OPERATOR, ">=")) {
            Token op = previous();
            ASTNodePtr right = term();
            expr = std::make_shared<BinaryOp>(op.value, expr, right, op.line, op.column);
        }
        return expr;
    }

    ASTNodePtr term() {
        ASTNodePtr expr = factor();
        while (match(TokenType::OPERATOR, "+") || match(TokenType::OPERATOR, "-")) {
            Token op = previous();
            ASTNodePtr right = factor();
            expr = std::make_shared<BinaryOp>(op.value, expr, right, op.line, op.column);
        }
        return expr;
    }

    ASTNodePtr factor() {
        ASTNodePtr expr = unary();
        while (match(TokenType::OPERATOR, "*") || match(TokenType::OPERATOR, "/") || match(TokenType::OPERATOR, "%")) {
            Token op = previous();
            ASTNodePtr right = unary();
            expr = std::make_shared<BinaryOp>(op.value, expr, right, op.line, op.column);
        }
        return expr;
    }

    ASTNodePtr unary() {
        if (match(TokenType::OPERATOR, "!") || match(TokenType::OPERATOR, "-")) {
            Token op = previous();
            ASTNodePtr operand = unary();
            return std::make_shared<UnaryOp>(op.value, operand, op.line, op.column);
        }
        return primary();
    }

    ASTNodePtr primary() {
        if (match(TokenType::NUMBER)) {
            Token number = previous();
            return std::make_shared<NumberLiteral>(std::stoi(number.value), number.line, number.column);
        }
        if (match(TokenType::STRING)) {
            Token str = previous();
            return std::make_shared<StringLiteral>(str.value, str.line, str.column);
        }
        if (match(TokenType::IDENTIFIER)) {
            Token ident = previous();
            if (match(TokenType::OPERATOR, "(")) {
                std::vector<ASTNodePtr> args;
                if (!check(TokenType::OPERATOR, ")")) {
                    do {
                        args.push_back(expression());
                    } while (match(TokenType::OPERATOR, ","));
                }
                consume(TokenType::OPERATOR, ")", "Expected ')' after arguments.");
                return std::make_shared<FunctionCall>(ident.value, args, ident.line, ident.column);
            }
            return std::make_shared<Identifier>(ident.value, ident.line, ident.column);
        }
        if (match(TokenType::OPERATOR, "(")) {
            ASTNodePtr expr = expression();
            consume(TokenType::OPERATOR, ")", "Expected ')' after expression.");
            return expr;
        }
        if (match(TokenType::OPERATOR, "[")) {
            // List literal
            std::vector<ASTNodePtr> elements;
            if (!check(TokenType::OPERATOR, "]")) {
                do {
                    elements.push_back(expression());
                } while (match(TokenType::OPERATOR, ","));
            }
            consume(TokenType::OPERATOR, "]", "Expected ']' after list elements.");
            // Convert to a single string with comma separation for simplicity
            std::string listValue = "[";
            for (size_t i = 0; i < elements.size(); ++i) {
                if (auto num = std::dynamic_pointer_cast<NumberLiteral>(elements[i])) {
                    listValue += std::to_string(num->value);
                }
                else if (auto str = std::dynamic_pointer_cast<StringLiteral>(elements[i])) {
                    listValue += "\"" + str->value + "\"";
                }
                else {
                    listValue += "UNKNOWN";
                }
                if (i != elements.size() - 1)
                    listValue += ", ";
            }
            listValue += "]";
            return std::make_shared<StringLiteral>(listValue, previous().line, previous().column);
        }
        if (match(TokenType::OPERATOR, "{")) {
            // Dictionary literal
            std::map<std::string, std::string> dict;
            while (!check(TokenType::OPERATOR, "}")) {
                ASTNodePtr keyNode = expression();
                std::string key;
                if (auto str = std::dynamic_pointer_cast<StringLiteral>(keyNode)) {
                    key = str->value;
                }
                else {
                    throw std::runtime_error("Dictionary keys must be strings.");
                }
                consume(TokenType::OPERATOR, ":", "Expected ':' after key in dictionary.");
                ASTNodePtr valueNode = expression();
                std::string value;
                if (auto num = std::dynamic_pointer_cast<NumberLiteral>(valueNode)) {
                    value = std::to_string(num->value);
                }
                else if (auto str = std::dynamic_pointer_cast<StringLiteral>(valueNode)) {
                    value = str->value;
                }
                dict[key] = value;
                if (!match(TokenType::OPERATOR, ",")) {
                    break;
                }
            }
            consume(TokenType::OPERATOR, "}", "Expected '}' after dictionary.");
            // Convert to a single string with key-value pairs for simplicity
            std::string dictValue = "{";
            size_t count = 0;
            for (const auto& pair : dict) {
                dictValue += "\"" + pair.first + "\": \"" + pair.second + "\"";
                if (count != dict.size() - 1)
                    dictValue += ", ";
                count++;
            }
            dictValue += "}";
            return std::make_shared<StringLiteral>(dictValue, previous().line, previous().column);
        }
        throw std::runtime_error("Unexpected token '" + peek().value + "' at line " + std::to_string(peek().line) + ", column " + std::to_string(peek().column));
    }

    Token consume(TokenType type, const std::string& errorMessage) {
        if (check(type)) {
            return advance();
        }
        throw std::runtime_error("Parser Error at line " + std::to_string(peek().line) + ", column " + std::to_string(peek().column) + ": " + errorMessage);
    }

    Token consume(TokenType type, const std::string& value, const std::string& errorMessage) {
        if (check(type, value)) {
            return advance();
        }
        throw std::runtime_error("Parser Error at line " + std::to_string(peek().line) + ", column " + std::to_string(peek().column) + ": " + errorMessage);
    }

    Token consume(const std::string& typeStr, const std::string& errorMessage) {
        TokenType type;
        if (typeStr == "IDENTIFIER") type = TokenType::IDENTIFIER;
        else if (typeStr == "NUMBER") type = TokenType::NUMBER;
        else if (typeStr == "STRING") type = TokenType::STRING;
        else if (typeStr == "OPERATOR") type = TokenType::OPERATOR;
        else if (typeStr == "DELIMITER") type = TokenType::DELIMITER;
        else throw std::runtime_error("Unknown token type in consume.");
        return consume(type, errorMessage);
    }

    Token consumeIdentifier(const std::string& errorMessage) {
        if (check(TokenType::IDENTIFIER)) {
            return advance();
        }
        throw std::runtime_error("Parser Error at line " + std::to_string(peek().line) + ", column " + std::to_string(peek().column) + ": " + errorMessage);
    }
};

// ======================== Interpreter Definitions ========================

class Environment;
using EnvPtr = std::shared_ptr<Environment>;

class Environment {
public:
    EnvPtr enclosing;
    std::unordered_map<std::string, std::string> variables;

    Environment() : enclosing(nullptr) {}
    Environment(EnvPtr enclosing) : enclosing(enclosing) {}

    void define(const std::string& name, const std::string& value) {
        variables[name] = value;
    }

    void assign(const std::string& name, const std::string& value) {
        if (variables.find(name) != variables.end()) {
            variables[name] = value;
            return;
        }
        if (enclosing != nullptr) {
            enclosing->assign(name, value);
            return;
        }
        throw std::runtime_error("Undefined variable '" + name + "'.");
    }

    std::string get(const std::string& name) {
        if (variables.find(name) != variables.end()) {
            return variables[name];
        }
        if (enclosing != nullptr) {
            return enclosing->get(name);
        }
        throw std::runtime_error("Undefined variable '" + name + "'.");
    }
};

class Interpreter {
public:
    EnvPtr globals;
    EnvPtr environment;

    Interpreter() {
        globals = std::make_shared<Environment>();
        environment = globals;
        defineBuiltIns();
    }

    void interpret(std::shared_ptr<Program> program) {
        try {
            for (auto& stmt : program->statements) {
                execute(stmt);
            }
        }
        catch (const std::runtime_error& e) {
            std::cerr << "Runtime Error: " << e.what() << std::endl;
        }
    }

private:
    void execute(ASTNodePtr node) {
        if (auto varDecl = std::dynamic_pointer_cast<VarDeclaration>(node)) {
            executeVarDeclaration(varDecl);
        }
        else if (auto assign = std::dynamic_pointer_cast<Assignment>(node)) {
            executeAssignment(assign);
        }
        else if (auto funcDecl = std::dynamic_pointer_cast<FunctionDeclaration>(node)) {
            executeFunctionDeclaration(funcDecl);
        }
        else if (auto funcCall = std::dynamic_pointer_cast<FunctionCall>(node)) {
            executeFunctionCall(funcCall);
        }
        else if (auto printStmt = std::dynamic_pointer_cast<PrintStatement>(node)) {
            executePrintStatement(printStmt);
        }
        else if (auto ifStmt = std::dynamic_pointer_cast<IfStatement>(node)) {
            executeIfStatement(ifStmt);
        }
        else if (auto whileLoop = std::dynamic_pointer_cast<WhileLoop>(node)) {
            executeWhileLoop(whileLoop);
        }
        else if (auto forLoop = std::dynamic_pointer_cast<ForLoop>(node)) {
            executeForLoop(forLoop);
        }
        else if (auto classDecl = std::dynamic_pointer_cast<ClassDeclaration>(node)) {
            executeClassDeclaration(classDecl);
        }
        else if (auto tryCatch = std::dynamic_pointer_cast<TryCatch>(node)) {
            executeTryCatch(tryCatch);
        }
        else {
            throw std::runtime_error("Unknown AST node type.");
        }
    }

    void executeVarDeclaration(std::shared_ptr<VarDeclaration> varDecl) {
        std::string value = evaluate(varDecl->value);
        environment->define(varDecl->name, value);
    }

    void executeAssignment(std::shared_ptr<Assignment> assign) {
        std::string value = evaluate(assign->value);
        environment->assign(assign->name, value);
    }

    void executeFunctionDeclaration(std::shared_ptr<FunctionDeclaration> funcDecl) {
        // For simplicity, store function as a string representing its name
        // In a full implementation, you'd store parameters and body
        environment->define(funcDecl->name, "Function");
    }

    void executeFunctionCall(std::shared_ptr<FunctionCall> funcCall) {
        // For simplicity, handle built-in functions and user-defined functions
        if (environment->variables.find(funcCall->name) != environment->variables.end()) {
            std::string func = environment->get(funcCall->name);
            if (func == "Function") {
                // Execute function body
                // Skipping implementation for brevity
            }
            else if (func == "Print") {
                std::string arg = evaluate(funcCall->args[0]);
                std::cout << arg << std::endl;
            }
            else {
                // Handle other built-in functions
                std::cout << "Function call: " << funcCall->name << std::endl;
            }
        }
        else {
            std::cout << "Function '" << funcCall->name << "' is not defined." << std::endl;
        }
    }

    void executePrintStatement(std::shared_ptr<PrintStatement> printStmt) {
        std::string value = evaluate(printStmt->expression);
        std::cout << value << std::endl;
    }

    void executeIfStatement(std::shared_ptr<IfStatement> ifStmt) {
        std::string condition = evaluate(ifStmt->condition);
        if (condition == "true" || condition == "1") {
            EnvPtr newEnv = std::make_shared<Environment>(environment);
            executeBlock(ifStmt->if_body, newEnv);
        }
        else {
            EnvPtr newEnv = std::make_shared<Environment>(environment);
            executeBlock(ifStmt->else_body, newEnv);
        }
    }

    void executeWhileLoop(std::shared_ptr<WhileLoop> whileLoop) {
        while (true) {
            std::string condition = evaluate(whileLoop->condition);
            if (condition != "true" && condition != "1") break;
            EnvPtr newEnv = std::make_shared<Environment>(environment);
            executeBlock(whileLoop->body, newEnv);
        }
    }

    void executeForLoop(std::shared_ptr<ForLoop> forLoop) {
        // Execute initialization
        execute(forLoop->initialization);
        while (true) {
            std::string condition = evaluate(forLoop->condition);
            if (condition != "true" && condition != "1") break;
            EnvPtr newEnv = std::make_shared<Environment>(environment);
            executeBlock(forLoop->body, newEnv);
            // Execute increment
            execute(forLoop->increment);
        }
    }

    void executeClassDeclaration(std::shared_ptr<ClassDeclaration> classDecl) {
        // For simplicity, store class as a string
        environment->define(classDecl->name, "Class");
    }

    void executeTryCatch(std::shared_ptr<TryCatch> tryCatch) {
        try {
            EnvPtr tryEnv = std::make_shared<Environment>(environment);
            executeBlock(tryCatch->try_block, tryEnv);
        }
        catch (const std::runtime_error& e) {
            EnvPtr catchEnv = std::make_shared<Environment>(environment);
            // Define 'error' variable
            catchEnv->define("error", e.what());
            executeBlock(tryCatch->catch_block, catchEnv);
        }
    }

    void executeBlock(const std::vector<ASTNodePtr>& statements, EnvPtr env) {
        EnvPtr previous = environment;
        environment = env;
        try {
            for (auto& stmt : statements) {
                execute(stmt);
            }
        }
        catch (...) {
            environment = previous;
            throw;
        }
        environment = previous;
    }

    std::string evaluate(ASTNodePtr expr) {
        if (auto numLit = std::dynamic_pointer_cast<NumberLiteral>(expr)) {
            return std::to_string(numLit->value);
        }
        if (auto strLit = std::dynamic_pointer_cast<StringLiteral>(expr)) {
            return strLit->value;
        }
        if (auto ident = std::dynamic_pointer_cast<Identifier>(expr)) {
            return environment->get(ident->name);
        }
        if (auto binOp = std::dynamic_pointer_cast<BinaryOp>(expr)) {
            std::string left = evaluate(binOp->left);
            std::string right = evaluate(binOp->right);
            if (binOp->op == "+") {
                return left + right;
            }
            if (binOp->op == "-") {
                // Convert to integers for subtraction
                int l = std::stoi(left);
                int r = std::stoi(right);
                return std::to_string(l - r);
            }
            if (binOp->op == "*") {
                int l = std::stoi(left);
                int r = std::stoi(right);
                return std::to_string(l * r);
            }
            if (binOp->op == "/") {
                int l = std::stoi(left);
                int r = std::stoi(right);
                if (r == 0) throw std::runtime_error("Division by zero.");
                return std::to_string(l / r);
            }
            if (binOp->op == "==") {
                return (left == right) ? "true" : "false";
            }
            if (binOp->op == "!=") {
                return (left != right) ? "true" : "false";
            }
            if (binOp->op == "<") {
                return (left < right) ? "true" : "false";
            }
            if (binOp->op == ">") {
                return (left > right) ? "true" : "false";
            }
            if (binOp->op == "<=") {
                return (left <= right) ? "true" : "false";
            }
            if (binOp->op == ">=") {
                return (left >= right) ? "true" : "false";
            }
            if (binOp->op == "&&") {
                return (left == "true" && right == "true") ? "true" : "false";
            }
            if (binOp->op == "||") {
                return (left == "true" || right == "true") ? "true" : "false";
            }
            throw std::runtime_error("Unknown binary operator '" + binOp->op + "'.");
        }
        if (auto unaryOp = std::dynamic_pointer_cast<UnaryOp>(expr)) {
            std::string operand = evaluate(unaryOp->operand);
            if (unaryOp->op == "!") {
                return (operand != "true") ? "true" : "false";
            }
            if (unaryOp->op == "-") {
                int val = std::stoi(operand);
                return std::to_string(-val);
            }
            throw std::runtime_error("Unknown unary operator '" + unaryOp->op + "'.");
        }
        if (auto funcCall = std::dynamic_pointer_cast<FunctionCall>(expr)) {
            executeFunctionCall(funcCall);
            return "";
        }
        throw std::runtime_error("Unknown expression type.");
    }

    Token consume(TokenType type, const std::string& errorMessage) {
        if (check(type)) {
            return advance();
        }
        throw std::runtime_error("Parser Error at line " + std::to_string(peek().line) + ", column " + std::to_string(peek().column) + ": " + errorMessage);
    }

    Token consume(const std::string& expectedValue, const std::string& errorMessage) {
        if (check(TokenType::OPERATOR, expectedValue)) {
            return advance();
        }
        throw std::runtime_error("Parser Error at line " + std::to_string(peek().line) + ", column " + std::to_string(peek().column) + ": " + errorMessage);
    }

    Token consume(TokenType type, const std::string& value, const std::string& errorMessage) {
        if (check(type, value)) {
            return advance();
        }
        throw std::runtime_error("Parser Error at line " + std::to_string(peek().line) + ", column " + std::to_string(peek().column) + ": " + errorMessage);
    }

    Token consumeIdentifier(const std::string& errorMessage) {
        if (check(TokenType::IDENTIFIER)) {
            return advance();
        }
        throw std::runtime_error("Parser Error at line " + std::to_string(peek().line) + ", column " + std::to_string(peek().column) + ": " + errorMessage);
    }

    void defineBuiltIns() {
        globals->define("len", "Builtin");
        globals->define("str", "Builtin");
        globals->define("int", "Builtin");
    }
};

// ======================== Main Function ========================

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: ./spelllang_interpreter <filename.spell>" << std::endl;
        return 1;
    }

    std::ifstream file(argv[1]);
    if (!file) {
        std::cerr << "Error: Cannot open file '" << argv[1] << "'." << std::endl;
        return 1;
    }

    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string code = buffer.str();

    // Lexing
    Lexer lexer(code);
    std::vector<Token> tokens;
    try {
        tokens = lexer.tokenize();
    }
    catch (const std::runtime_error& e) {
        std::cerr << e.what() << std::endl;
        return 1;
    }

    // Parsing
    Parser parser(tokens);
    std::shared_ptr<Program> program;
    try {
        program = parser.parse();
    }
    catch (const std::runtime_error& e) {
        std::cerr << e.what() << std::endl;
        return 1;
    }

    // Interpretation
    Interpreter interpreter;
    interpreter.interpret(program);

    return 0;
}
