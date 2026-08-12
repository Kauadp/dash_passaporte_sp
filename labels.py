"""
Textos legíveis pra cada etapa / pergunta / opção da jornada.
Fonte: Matriz Estruturada de Perguntas e Captura de Dados por Totem V2
(docx enviado) + os templates HTML de cada formulário.
Usado só pra exibição (troca slug por texto) — nunca pra filtrar dado.
"""

ETAPA_LABELS = {
    "boas_vindas": "Boas-vindas",
    "entrada_juquita": "Entrada Juquita",
    "acao_guerrilha": "Ação Guerrilha",
    "lounge_vip": "Lounge VIP",
    "estacionamento": "Estacionamento",
    "cenografia": "Cenografia",
    "dentro_lojas": "Dentro das Lojas",
    "saida_juquita": "Saída Juquita (Brindes)",
    "saida_nps": "Saída & NPS",
}

PERGUNTA_LABELS = {
    "oque_trouxe": "O que te trouxe ao Ibirapuera hoje?",
    "regiao": "Qual é a sua região de origem?",
    "quem_eh_voce": "Quem é você hoje no Exagerado?",
    "qual_foco": "Qual é o seu foco principal hoje?",
    "como_veio": "Como você veio pro Exagerado?",
    "quanto_tempo": "Quanto tempo levou no corre até chegar?",
    "item_ritmo": "Esse item vai te acompanhar em qual ritmo?",
    "faixa_etaria": "Qual é a sua vibe de época/geração?",
    "ficou_sabendo_onde": "Ficou sabendo do rolê por onde?",
    "oque_mais_garimpou": "O que você mais gostou de garimpar até agora?",
    "prioridade": "Qual é a sua prioridade no Lounge VIP?",
    "quantas_sacolas": "Quantas sacolas você planeja levar pra casa hoje?",
    "melhor_dia": "Qual o melhor dia pra curtir?",
    "forma_pagamento": "Como tá pagando as compritas?",
    "qual_renda": "E o money? Qual sua renda?",
    "quanto_pretende_gastar": "Quanto vc pretende gastar ou gastou nessa brincadeira?",
    "com_quem_veio": "Veio com quem curtir o rolê?",
    "maior_destaque": "Qual foi o maior destaque do seu dia no Exagerado?",
    "te_vejo_proxima_edicao": "Te vejo na próxima edição SP?",
}

_REGIAO = {
    "vizinho_parque": "Vizinho do Parque (Moema, Vila Mariana, Jardins, Itaim)",
    "zona_sul": "Outros bairros da Zona Sul",
    "zona_oeste_centro_zona_norte_zona_leste": "Zona Oeste / Centro / Zona Norte / Zona Leste",
    "grande_sp_interior_outro_estado": "Grande SP / Interior / Outro Estado",
}

OPCOES_LABELS = {
    "oque_trouxe": {
        "trabalho_treino_exercicio": "Trabalho / Treino / Exercício",
        "passeio_piquenique_relaxar": "Passeio, piquenique ou relaxar",
        "exagerado": "Vim especialmente para o Exagerado",
        "familia_pet": "Passeando com pet / família",
    },
    "regiao": _REGIAO,
    "quem_eh_voce": {
        "caçador_de_marcas_fod4s": "Caçador de marcas fod4s",
        "passeador_profissional_só_vim_acompanhar": "Passeador profissional / Só acompanhando",
        "veio_comer_tomar_uma": "Veio pra comer e tomar uma",
        "cansado_buscando_promoção": "Cansado buscando promoção",
    },
    "qual_foco": {
        "roupas_e_calçados": "Roupas e calçados",
        "casa_e_decoracao": "Casa e decoração",
        "infantil_kids": "Infantil / Kids",
        "gastronomia_e_entretenimento": "Gastronomia e entretenimento",
        "outros_segmentos": "Outros segmentos",
    },
    "como_veio": {
        "carro_proprio": "Carro próprio / Estacionamento",
        "app_mobilidade": "Uber / App de Mobilidade",
        "transporte_publico": "Transporte Público (Metrô / Ônibus)",
        "pe_bike_patinete": "A pé / Bike / Patinete",
    },
    "quanto_tempo": {
        "menos_trinta_minutos": "Menos de 30 min",
        "trinta_a_uma_hora": "30 min a 1 hora",
        "mais_de_uma_hora": "Mais de 1 hora",
    },
    "item_ritmo": {
        "acessibilidade_conforto": "Acessibilidade / Conforto",
        "modo_familia": "Modo família com crianças",
        "maratonando_compras": "Maratonando as compras",
        "colecionador_itens": "Colecionador de itens exclusivos",
    },
    "faixa_etaria": {
        "geracao_z": "Geração Z (até 24 anos)",
        "millennial": "Millennial (25 a 40 anos)",
        "experiente_chique": "Experiente & Chique (41 a 55 anos)",
        "exagerado_classico": "Exagerado Clássico (56+ anos)",
    },
    "ficou_sabendo_onde": {
        "redes_sociais_evento": "Redes sociais do evento",
        "pelo_whatsapp": "WhatsApp",
        "familia_amigos": "Família e amigos",
        "ativacoes": "Ativações",
        "influenciadores": "Influenciadores digitais",
    },
    "oque_mais_garimpou": {
        "marcas_famosas_desconto": "Marcas famosas com desconto real",
        "achadinhos_nao_esperados": "Achadinhos inesperados",
        "experiencia": "Experiência / Espaço gastronômico",
    },
    "prioridade": {
        "recarregar_bateria": "Recarregar a bateria (minha e do celular)",
        "network_e_bons_drinks": "Networking e bons drinks",
        "fazer_pausa_estrategica": "Pausa estratégica entre compras",
    },
    "quantas_sacolas": {
        "um_a_tres": "1 a 3 itens",
        "quatro_a_sete": "4 a 7 itens",
        "mais_de_oito": "Mais de 8 itens",
    },
    "melhor_dia": {
        "quarta_feira": "Quarta-feira",
        "quinta_feira": "Quinta-feira",
        "sexta_feira": "Sexta-feira",
        "sabado": "Sábado",
        "domingo": "Domingo",
    },
    "forma_pagamento": {
        "pix": "PIX",
        "cartao_debito": "Cartão de Débito",
        "cartao_credito": "Cartão de Crédito",
        "dinheiro": "Dinheiro",
    },
    "qual_renda": {
        "ate_mil": "Até R$1.000",
        "entre_mil_e_tres_mil": "R$1.000 a R$3.000",
        "entre_tres_mil_e_seis_mil": "R$3.000 a R$6.000",
        "acima_de_seis_mil": "Acima de R$6.000",
    },
    "quanto_pretende_gastar": {
        "ate_duzentos": "Até R$200",
        "entre_duzentos_e_seiscentos": "R$200 a R$600",
        "entre_seiscentos_e_mil_e_duzentos": "R$600 a R$1.200",
        "entre_mil_e_duzentos_e_mil_e_quinhentos": "R$1.200 a R$1.500",
        "acima_de_mil_e_quinhentos": "Acima de R$1.500",
    },
    "com_quem_veio": {
        "sozinho": "Sozinho",
        "com_familia": "Com a família",
        "com_amigos": "Com amigos",
    },
    "maior_destaque": {
        "precos_descontos": "Preços e descontos",
        "estrutura_espaco": "Estrutura e espaço no Ibirapuera",
        "atendimento": "Atendimento e facilidade do evento",
        "variedade_marcas": "Variedade de marcas",
    },
    "te_vejo_proxima_edicao": {
        "com_certeza": "Com certeza",
        "depende_data": "Depende da data",
        "talvez": "Talvez",
    },
}


def rotular_opcao(pergunta: str, valor: str) -> str:
    return OPCOES_LABELS.get(pergunta, {}).get(valor, valor)


def rotular_pergunta(pergunta: str) -> str:
    return PERGUNTA_LABELS.get(pergunta, pergunta)


def rotular_etapa(etapa: str) -> str:
    return ETAPA_LABELS.get(etapa, etapa)