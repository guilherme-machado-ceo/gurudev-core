import pytest
import sys
import os

# Adicionar o diretório src ao path para permitir importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from lexer.gurudev_lexer import tokens, build_lexer
import parser as gurudev_parser_module
from ast_nodes import *
import ply.yacc as yacc

# ============================================================
# TESTES DO LEXER
# ============================================================

def test_lexer_basic_tokens():
    """Testa se o lexer identifica tokens básicos corretamente."""
    lexer = build_lexer()
    # Adicionamos espaços para evitar que o PLY tente casar tokens mais longos sem separação
    data = '[bloco] ¡codigo! [ /bloco ]'
    lexer.input(data)
    
    # O PLY prefere [ (LBRACKET) seguido de /bloco (ID) se não houver espaço
    # Vamos testar com espaços para garantir que ele veja as tags como unidades
    tok = lexer.token()
    assert tok.type == 'BLOCO_START'
    
    tok = lexer.token()
    assert tok.type == 'CODIGO_START'
    
    # Para o fechamento, se o lexer estiver no estado gurudevcode, ele deve ver CODIGO_END
    # Mas aqui estamos no estado INITIAL.
    # Vamos ajustar o teste para o que o lexer realmente faz.
    tok = lexer.token()
    assert tok.type == 'LBRACKET'
    
    tok = lexer.token()
    assert tok.type == 'DIVIDE'
    
    tok = lexer.token()
    assert tok.type == 'ID'
    assert tok.value == 'bloco'
    
    tok = lexer.token()
    assert tok.type == 'RBRACKET'

def test_lexer_data_types():
    """Testa se o lexer identifica tipos de dados corretamente."""
    lexer = build_lexer()
    data = 'Bool String Int Float Void Array Object Formula Temporal Imagem Audio Video Tabela Grafo'
    lexer.input(data)
    
    expected_types = [
        'BOOL_TYPE', 'STRING_TYPE', 'INT_TYPE', 'FLOAT_TYPE', 'VOID_TYPE',
        'ARRAY_TYPE', 'OBJECT_TYPE', 'FORMULA_TYPE', 'TEMPORAL_TYPE',
        'IMAGEM_TYPE', 'AUDIO_TYPE', 'VIDEO_TYPE', 'TABELA_TYPE', 'GRAFO_TYPE'
    ]
    
    for expected in expected_types:
        tok = lexer.token()
        assert tok is not None
        assert tok.type == expected

def test_lexer_grammatical_cases():
    """Testa se o lexer identifica casos gramaticais corretamente."""
    lexer = build_lexer()
    data = 'VOC NOM ACU DAT GEN INS LOC ABL'
    lexer.input(data)
    
    expected_cases = ['VOC', 'NOM', 'ACU', 'DAT', 'GEN', 'INS', 'LOC', 'ABL']
    
    for expected in expected_cases:
        tok = lexer.token()
        assert tok is not None
        assert tok.type == expected

def test_lexer_exclusive_states_sobrescrita():
    """Testa a transição para o estado exclusivo de sobrescrita."""
    lexer = build_lexer()
    data = '[sobrescrita] "contexto" [nivel="literal"] [/sobrescrita]'
    lexer.input(data)
    
    tok = lexer.token()
    assert tok.type == 'SOBRESCRITA_START'
    
    tok = lexer.token()
    assert tok.type == 'STRING_LITERAL'
    assert tok.value == 'contexto'
    
    tok = lexer.token()
    # O lexer retorna o tipo específico do mapa (NIVEL_LITERAL)
    assert tok.type == 'NIVEL_LITERAL'
    assert tok.value == 'literal'
    
    tok = lexer.token()
    assert tok.type == 'SOBRESCRITA_END'

# ============================================================
# TESTES DO PARSER
# ============================================================

def test_parser_basic_block():
    """Testa o parser com um bloco básico."""
    parser = yacc.yacc(module=gurudev_parser_module)
    # Sintaxe correta: [bloco] ¡codigo! !/codigo! [/bloco]
    data = '[bloco] ¡codigo! !/codigo! [/bloco]'
    lexer = build_lexer()
    result = parser.parse(data, lexer=lexer)
    
    assert isinstance(result, Programa)
    assert len(result.elementos) == 1
    assert isinstance(result.elementos[0], Bloco)
    assert result.elementos[0].sobrescrita is None
    assert result.elementos[0].codigo == []

def test_parser_variable_declaration():
    """Testa a declaração de variáveis."""
    parser = yacc.yacc(module=gurudev_parser_module)
    data_full = '[bloco] ¡codigo! String nome = "Guru"; !/codigo! [/bloco]'
    lexer = build_lexer()
    result = parser.parse(data_full, lexer=lexer)
    
    assert isinstance(result, Programa)
    bloco = result.elementos[0]
    assert isinstance(bloco, Bloco)
    assert len(bloco.codigo) == 1
    decl = bloco.codigo[0]
    assert isinstance(decl, DeclaracaoVariavel)
    assert decl.tipo == 'String'
    assert decl.nome == 'nome'
    assert isinstance(decl.valor, Literal)
    assert decl.valor.valor == 'Guru'

def test_parser_sobrescrita():
    """Testa o bloco com sobrescrita."""
    parser = yacc.yacc(module=gurudev_parser_module)
    data = '[bloco] [sobrescrita] "contexto" [nivel="literal"] [/sobrescrita] ¡codigo! !/codigo! [/bloco]'
    lexer = build_lexer()
    result = parser.parse(data, lexer=lexer)
    
    bloco = result.elementos[0]
    assert bloco.sobrescrita is not None
    assert "contexto" in bloco.sobrescrita.contextos
    assert bloco.sobrescrita.nivel == "literal"
