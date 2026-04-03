"""
GuruDev® Lexer — Versão 1.1.0-alpha
Analisador Léxico para a linguagem GuruDev®
Autor: Guilherme Gonçalves Machado
Ferramenta: PLY (Python Lex-Yacc)
"""

import ply.lex as lex
import sys
from typing import List, Optional

# ============================================================
# 1. LISTA DE TOKENS
# ============================================================

tokens = (
    'BLOCO_START', 'BLOCO_END',
    'SOBRESCRITA_START', 'SOBRESCRITA_END',
    'SUBESCRITAS_START', 'SUBESCRITAS_END',
    'CODIGO_START', 'CODIGO_END',
    'COMPENSACAO_START', 'COMPENSACAO_END',
    'ERRO_START', 'ERRO_END',
    'DESEMPENHO_START', 'DESEMPENHO_END',
    'ALTERNATIVA_START', 'ALTERNATIVA_END',
    'PLASTICO_START', 'PLASTICO_END',
    'MODULACAO_START', 'MODULACAO_END',
    'PYTHON_START', 'PYTHON_END',
    'RUST_START', 'RUST_END',
    'JAVASCRIPT_START', 'JAVASCRIPT_END',
    'CSHARP_START', 'CSHARP_END',
    'WASM_START', 'WASM_END',
    'CPP_START', 'CPP_END',
    'JAVA_START', 'JAVA_END',
    'SQL_START', 'SQL_END',
    'R_START', 'R_END',
    'FOREIGN_CODE_CONTENT',
    'NIVEL_ATTR', 'RAIZ_ATTR', 'CLAVE_ATTR', 'ONT_ATTR',
    'NIVEL_LITERAL', 'NIVEL_ALEGORICO', 'NIVEL_MORAL', 'NIVEL_MISTICO',
    'NIVEL_FUNCIONAL', 'NIVEL_ESTETICO', 'NIVEL_ONTOLOGICO', 'NIVEL_HOLISTICO',
    'NIVEL_MATEMATICO', 'NIVEL_SIMBOLICO', 'NIVEL_PARABOLICO', 'NIVEL_HISTORICO',
    'NIVEL_LINGUISTICO',
    'CLAVE_ARTE', 'CLAVE_CIENCIA', 'CLAVE_FILOSOFIA', 'CLAVE_TRADICAO', 'CLAVE_GERAL',
    'ONT_SUBSTANCIA', 'ONT_QUANTIDADE', 'ONT_QUALIDADE', 'ONT_RELACAO',
    'ONT_LUGAR', 'ONT_TEMPO', 'ONT_SITUACAO', 'ONT_CONDICAO', 'ONT_ACAO', 'ONT_PAIXAO',
    'VOC', 'NOM', 'ACU', 'DAT', 'GEN', 'INS', 'LOC', 'ABL',
    'FUNCAO', 'CLASSE', 'EXTENDS', 'IMPLEMENTS',
    'BOOL_TYPE', 'STRING_TYPE', 'INT_TYPE', 'FLOAT_TYPE', 'VOID_TYPE',
    'ARRAY_TYPE', 'OBJECT_TYPE', 'FORMULA_TYPE', 'TEMPORAL_TYPE',
    'IMAGEM_TYPE', 'AUDIO_TYPE', 'VIDEO_TYPE', 'TABELA_TYPE', 'GRAFO_TYPE',
    'IF_KEYWORD', 'ELSE_KEYWORD', 'FOR_KEYWORD', 'WHILE_KEYWORD',
    'RETURN_KEYWORD', 'BREAK_KEYWORD', 'CONTINUE_KEYWORD',
    'SERIE_KEYWORD', 'PARALELO_KEYWORD', 'EM_KEYWORD',
    'PUBLICO', 'PRIVADO', 'PROTEGIDO',
    'STRING_LITERAL', 'INT_LITERAL', 'FLOAT_LITERAL', 'BOOLEAN_LITERAL',
    'ID',
    'EQUALS', 'NOT_EQUALS', 'LESS_EQUAL', 'GREATER_EQUAL',
    'AND', 'OR', 'ARROW',
    'ASSIGN', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MODULO',
    'LESS_THAN', 'GREATER_THAN', 'NOT',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
    'SEMICOLON', 'COMMA', 'DOT', 'COLON',
    'NEWLINE',
)

# ============================================================
# 2. ESTADOS DO LEXER
# ============================================================

states = (
    ('sobrescrita', 'exclusive'),
    ('gurudevcode', 'exclusive'),
    ('compensacao', 'exclusive'),
    ('plastico', 'exclusive'),
    ('modulacao', 'exclusive'),
    ('pythoncode', 'exclusive'),
    ('rustcode', 'exclusive'),
    ('javascriptcode', 'exclusive'),
    ('csharpcode', 'exclusive'),
    ('wasmcode', 'exclusive'),
    ('cppcode', 'exclusive'),
    ('javacode', 'exclusive'),
    ('sqlcode', 'exclusive'),
    ('rcode', 'exclusive'),
)

# ============================================================
# 3. PALAVRAS RESERVADAS E MAPAS
# ============================================================

reserved = {
    'VOC': 'VOC', 'NOM': 'NOM', 'ACU': 'ACU', 'DAT': 'DAT',
    'GEN': 'GEN', 'INS': 'INS', 'LOC': 'LOC', 'ABL': 'ABL',
    'funcao': 'FUNCAO', 'classe': 'CLASSE',
    'extends': 'EXTENDS', 'implements': 'IMPLEMENTS',
    'if': 'IF_KEYWORD', 'se': 'IF_KEYWORD',
    'else': 'ELSE_KEYWORD', 'senao': 'ELSE_KEYWORD',
    'for': 'FOR_KEYWORD', 'para': 'FOR_KEYWORD',
    'while': 'WHILE_KEYWORD', 'enquanto': 'WHILE_KEYWORD',
    'return': 'RETURN_KEYWORD', 'retorna': 'RETURN_KEYWORD',
    'break': 'BREAK_KEYWORD', 'quebra': 'BREAK_KEYWORD',
    'continue': 'CONTINUE_KEYWORD', 'continua': 'CONTINUE_KEYWORD',
    'serie': 'SERIE_KEYWORD', 'paralelo': 'PARALELO_KEYWORD', 'em': 'EM_KEYWORD',
    'publico': 'PUBLICO', 'privado': 'PRIVADO', 'protegido': 'PROTEGIDO',
    'Bool': 'BOOL_TYPE', 'String': 'STRING_TYPE', 'Int': 'INT_TYPE',
    'Float': 'FLOAT_TYPE', 'Void': 'VOID_TYPE', 'Array': 'ARRAY_TYPE',
    'Object': 'OBJECT_TYPE', 'Formula': 'FORMULA_TYPE', 'Temporal': 'TEMPORAL_TYPE',
    'Imagem': 'IMAGEM_TYPE', 'Audio': 'AUDIO_TYPE', 'Video': 'VIDEO_TYPE',
    'Tabela': 'TABELA_TYPE', 'Grafo': 'GRAFO_TYPE',
    'true': 'BOOLEAN_LITERAL', 'false': 'BOOLEAN_LITERAL',
    'verdadeiro': 'BOOLEAN_LITERAL', 'falso': 'BOOLEAN_LITERAL',
}

nivel_map = {
    'literal': 'NIVEL_LITERAL', 'alegorico': 'NIVEL_ALEGORICO',
    'moral': 'NIVEL_MORAL', 'mistico': 'NIVEL_MISTICO',
    'funcional': 'NIVEL_FUNCIONAL', 'estetico': 'NIVEL_ESTETICO',
    'ontologico': 'NIVEL_ONTOLOGICO', 'holistico': 'NIVEL_HOLISTICO',
    'matematico': 'NIVEL_MATEMATICO', 'simbolico': 'NIVEL_SIMBOLICO',
    'parabolico': 'NIVEL_PARABOLICO', 'historico': 'NIVEL_HISTORICO',
    'linguistico': 'NIVEL_LINGUISTICO',
}

clave_map = {
    'arte': 'CLAVE_ARTE', 'ciencia': 'CLAVE_CIENCIA',
    'filosofia': 'CLAVE_FILOSOFIA', 'tradicao': 'CLAVE_TRADICAO',
    'geral': 'CLAVE_GERAL',
}

ont_map = {
    'substancia': 'ONT_SUBSTANCIA', 'quantidade': 'ONT_QUANTIDADE',
    'qualidade': 'ONT_QUALIDADE', 'relacao': 'ONT_RELACAO',
    'lugar': 'ONT_LUGAR', 'tempo': 'ONT_TEMPO',
    'situacao': 'ONT_SITUACAO', 'condicao': 'ONT_CONDICAO',
    'acao': 'ONT_ACAO', 'paixao': 'ONT_PAIXAO',
}

# ============================================================
# 4. REGRAS DO ESTADO INITIAL
# ============================================================

t_ignore = ' \t'

# Funções de tags complexas primeiro para prioridade sobre [ e ]
def t_BLOCO_START(t):
    r'\[bloco\]'
    return t

def t_BLOCO_END(t):
    r'\[/bloco\]'
    return t

def t_SOBRESCRITA_START(t):
    r'\[sobrescrita\]'
    t.lexer.push_state('sobrescrita')
    return t

def t_SUBESCRITAS_START(t):
    r'\[subescritas\]'
    return t

def t_SUBESCRITAS_END(t):
    r'\[/subescritas\]'
    return t

def t_COMPENSACAO_START(t):
    r'\[compensacao\]'
    t.lexer.push_state('compensacao')
    return t

def t_PLASTICO_START(t):
    r'\[plastico\]'
    t.lexer.push_state('plastico')
    return t

def t_MODULACAO_START(t):
    r'\[modulacao\]'
    t.lexer.push_state('modulacao')
    return t

def t_CODIGO_START(t):
    r'¡codigo!'
    t.lexer.push_state('gurudevcode')
    return t

def t_PYTHON_START(t):
    r'¿python\?'
    t.lexer.push_state('pythoncode')
    return t

def t_RUST_START(t):
    r'¿rust\?'
    t.lexer.push_state('rustcode')
    return t

def t_JAVASCRIPT_START(t):
    r'¿javascript\?'
    t.lexer.push_state('javascriptcode')
    return t

def t_CSHARP_START(t):
    r'¿csharp\?'
    t.lexer.push_state('csharpcode')
    return t

def t_WASM_START(t):
    r'¿wasm\?'
    t.lexer.push_state('wasmcode')
    return t

def t_CPP_START(t):
    r'¿c\+\+\?'
    t.lexer.push_state('cppcode')
    return t

def t_JAVA_START(t):
    r'¿java\?'
    t.lexer.push_state('javacode')
    return t

def t_SQL_START(t):
    r'¿sql\?'
    t.lexer.push_state('sqlcode')
    return t

def t_R_START(t):
    r'¿r\?'
    t.lexer.push_state('rcode')
    return t

def t_COMMENT_MULTI(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')

def t_COMMENT_SINGLE(t):
    r'//[^\n]*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_STRING_LITERAL(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]
    return t

def t_FLOAT_LITERAL(t):
    r'\d+\.\d+f?'
    t.value = float(t.value.replace('f', ''))
    return t

def t_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_EQUALS = r'=='
t_NOT_EQUALS = r'!='
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_AND = r'&&'
t_OR = r'\|\|'
t_ARROW = r'->'
t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_NOT = r'!'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

def t_LBRACKET(t):
    r'\['
    return t

def t_RBRACKET(t):
    r'\]'
    return t

t_SEMICOLON = r';'
t_COMMA = r','
t_DOT = r'\.'
t_COLON = r':'

def t_ID(t):
    r'[a-zA-ZÀ-ÿ_][a-zA-ZÀ-ÿ0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_error(t):
    print(f"[INITIAL] Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# ============================================================
# 5. REGRAS DO ESTADO SOBRESCRITA
# ============================================================

t_sobrescrita_ignore = ' \t'

def t_sobrescrita_NIVEL_ATTR(t):
    r'\[nivel="([^"]+)"\]'
    val = t.value[t.value.find('"')+1:t.value.rfind('"')].lower()
    t.type = nivel_map.get(val, 'NIVEL_ATTR')
    t.value = val
    return t

def t_sobrescrita_RAIZ_ATTR(t):
    r'\[raiz="([^"]+)"\]'
    t.value = t.value[t.value.find('"')+1:t.value.rfind('"')]
    return t

def t_sobrescrita_CLAVE_ATTR(t):
    r'\[clave="([^"]+)"\]'
    val = t.value[t.value.find('"')+1:t.value.rfind('"')].lower()
    t.type = clave_map.get(val, 'CLAVE_ATTR')
    t.value = val
    return t

def t_sobrescrita_ONT_ATTR(t):
    r'\[ont="([^"]+)"\]'
    val = t.value[t.value.find('"')+1:t.value.rfind('"')].lower()
    t.type = ont_map.get(val, 'ONT_ATTR')
    t.value = val
    return t

def t_sobrescrita_STRING_LITERAL(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]
    return t

def t_sobrescrita_SOBRESCRITA_END(t):
    r'\[/sobrescrita\]'
    t.lexer.pop_state()
    return t

def t_sobrescrita_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_sobrescrita_error(t):
    print(f"[SOBRESCRITA] Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# ============================================================
# 6. REGRAS DO ESTADO GURUDEVCODE
# ============================================================

t_gurudevcode_ignore = ' \t'

def t_gurudevcode_COMMENT_MULTI(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')

def t_gurudevcode_COMMENT_SINGLE(t):
    r'//[^\n]*'
    pass

def t_gurudevcode_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_gurudevcode_STRING_LITERAL(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]
    return t

def t_gurudevcode_FLOAT_LITERAL(t):
    r'\d+\.\d+f?'
    t.value = float(t.value.replace('f', ''))
    return t

def t_gurudevcode_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_gurudevcode_EQUALS = r'=='
t_gurudevcode_NOT_EQUALS = r'!='
t_gurudevcode_LESS_EQUAL = r'<='
t_gurudevcode_GREATER_EQUAL = r'>='
t_gurudevcode_AND = r'&&'
t_gurudevcode_OR = r'\|\|'
t_gurudevcode_ARROW = r'->'
t_gurudevcode_ASSIGN = r'='
t_gurudevcode_PLUS = r'\+'
t_gurudevcode_MINUS = r'-'
t_gurudevcode_MULTIPLY = r'\*'
t_gurudevcode_DIVIDE = r'/'
t_gurudevcode_MODULO = r'%'
t_gurudevcode_LESS_THAN = r'<'
t_gurudevcode_GREATER_THAN = r'>'
t_gurudevcode_NOT = r'!'
t_gurudevcode_LPAREN = r'\('
t_gurudevcode_RPAREN = r'\)'
t_gurudevcode_LBRACE = r'\{'
t_gurudevcode_RBRACE = r'\}'

def t_gurudevcode_LBRACKET(t):
    r'\['
    return t

def t_gurudevcode_RBRACKET(t):
    r'\]'
    return t

t_gurudevcode_SEMICOLON = r';'
t_gurudevcode_COMMA = r','
t_gurudevcode_DOT = r'\.'
t_gurudevcode_COLON = r':'

def t_gurudevcode_ID(t):
    r'[a-zA-ZÀ-ÿ_][a-zA-ZÀ-ÿ0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_gurudevcode_CODIGO_END(t):
    r'!/codigo!'
    t.lexer.pop_state()
    return t

def t_gurudevcode_error(t):
    print(f"[GURUDEVCODE] Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# ============================================================
# 7. REGRAS DO ESTADO COMPENSACAO
# ============================================================

t_compensacao_ignore = ' \t'

def t_compensacao_ERRO_START(t):
    r'\[erro[^\]]*\]'
    return t

def t_compensacao_ERRO_END(t):
    r'\[/erro\]'
    return t

def t_compensacao_DESEMPENHO_START(t):
    r'\[desempenho[^\]]*\]'
    return t

def t_compensacao_DESEMPENHO_END(t):
    r'\[/desempenho\]'
    return t

def t_compensacao_ALTERNATIVA_START(t):
    r'\[alternativa[^\]]*\]'
    return t

def t_compensacao_ALTERNATIVA_END(t):
    r'\[/alternativa\]'
    return t

def t_compensacao_COMPENSACAO_END(t):
    r'\[/compensacao\]'
    t.lexer.pop_state()
    return t

t_compensacao_SEMICOLON = r';'
t_compensacao_LPAREN = r'\('
t_compensacao_RPAREN = r'\)'
t_compensacao_LBRACE = r'\{'
t_compensacao_RBRACE = r'\}'
t_compensacao_DOT = r'\.'
t_compensacao_COMMA = r','
t_compensacao_COLON = r':'
t_compensacao_ASSIGN = r'='
t_compensacao_PLUS = r'\+'
t_compensacao_MINUS = r'-'
t_compensacao_MULTIPLY = r'\*'
t_compensacao_DIVIDE = r'/'

def t_compensacao_STRING_LITERAL(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]
    return t

def t_compensacao_FLOAT_LITERAL(t):
    r'\d+\.\d+f?'
    t.value = float(t.value.replace('f', ''))
    return t

def t_compensacao_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_compensacao_ID(t):
    r'[a-zA-ZÀ-ÿ_][a-zA-ZÀ-ÿ0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_compensacao_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_compensacao_error(t):
    print(f"[COMPENSACAO] Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# ============================================================
# 8. ESTADOS VAZIOS (PLASTICO, MODULACAO)
# ============================================================

t_plastico_ignore = ' \t'
def t_plastico_error(t):
    t.lexer.skip(1)

def t_plastico_PLASTICO_END(t):
    r'\[/plastico\]'
    t.lexer.pop_state()
    return t

t_modulacao_ignore = ' \t'
def t_modulacao_error(t):
    t.lexer.skip(1)

def t_modulacao_MODULACAO_END(t):
    r'\[/modulacao\]'
    t.lexer.pop_state()
    return t

# ============================================================
# 9. REGRAS PARA ESTADOS DE CÓDIGO ESTRANGEIRO
# ============================================================

def _make_foreign_rules(lang_name, end_pattern):
    state_name = f'{lang_name}code'
    
    def content(t):
        t.type = 'FOREIGN_CODE_CONTENT'
        t.lexer.lineno += t.value.count('\n')
        return t
    content.__doc__ = rf'[\s\S]+?(?={end_pattern})'
    
    def end(t):
        t.lexer.pop_state()
        return t
    end.__doc__ = end_pattern
    
    def error(t):
        t.lexer.skip(1)
    error.__doc__ = r'.'
    
    return content, end, error

_foreign_langs = {
    'python': r'\?/python\?',
    'rust': r'\?/rust\?',
    'javascript': r'\?/javascript\?',
    'csharp': r'\?/csharp\?',
    'wasm': r'\?/wasm\?',
    'cpp': r'\?/c\+\+\?',
    'java': r'\?/java\?',
    'sql': r'\?/sql\?',
    'r': r'\?/r\?',
}

_this_module = sys.modules[__name__]
for _lang, _end in _foreign_langs.items():
    _state = f'{_lang}code'
    _content, _end_func, _err = _make_foreign_rules(_lang, _end)
    setattr(_this_module, f't_{_state}_FOREIGN_CODE_CONTENT', _content)
    setattr(_this_module, f't_{_state}_{_lang.upper()}_END', _end_func)
    setattr(_this_module, f't_{_state}_error', _err)
    setattr(_this_module, f't_{_state}_ignore', ' \t')

# ============================================================
# 10. CONSTRUÇÃO E INTERFACE
# ============================================================

def build_lexer(**kwargs):
    return lex.lex(**kwargs)

def tokenize(source_code: str) -> List:
    lexer = build_lexer()
    lexer.input(source_code)
    result = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        result.append(tok)
    return result

if __name__ == '__main__':
    pass
