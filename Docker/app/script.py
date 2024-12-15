import pandas as pd
from flask import Flask, jsonify, request
import jwt
import datetime

# Configurações
SECRET_KEY = "senha"  # Chave secreta para o JWT
USERS = {"admin": "admin"}  # Credenciais 

# Dados de exemplo
dados_incorporados = {
    "CARDAPIO_MENOS_VENDIDO": [
    [
        {
            "Posiçãonoranking": "1",
            "Categoria": "Promo Porto",
            "Nomedoitem": "Combo Irresistível | 1 pizza grande + 1 Coca-Cola de 1,5",
            "Visitas": "5",
            "Vendas": "1",
            "Totalvendas": "R$ 65,90"
        },
        {
            "Posiçãonoranking": "2",
            "Categoria": "Pizza Artesanal Italiana | 8 Fatias",
            "Nomedoitem": "Quattro Formaggi",
            "Visitas": "13",
            "Vendas": "3",
            "Totalvendas": "R$ 260,70"
        },
        {
            "Posiçãonoranking": "3",
            "Categoria": "Promo Porto",
            "Nomedoitem": "Pizza em dobro | 2 pizzas grandes + 1 Coca-Cola 1,5l grátis",
            "Visitas": "35",
            "Vendas": "5",
            "Totalvendas": "R$ 692,00"
        },
        {
            "Posiçãonoranking": "4",
            "Categoria": "Pizza Artesanal Italiana | 8 Fatias",
            "Nomedoitem": "Mozzarela",
            "Visitas": "21",
            "Vendas": "7",
            "Totalvendas": "R$ 461,30"
        },
        {
            "Posiçãonoranking": "5",
            "Categoria": "Pizza Artesanal Italiana | 8 Fatias",
            "Nomedoitem": "Margherita",
            "Visitas": "38",
            "Vendas": "10",
            "Totalvendas": "R$ 599,00"
        }
    ]
    ],
    "CARDAPIO_3MESES": [
[
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":"1;Pizza Grande | 2 sabores;Escolha os sabores da sua pizza :;700;310;R$ 21.977",
       "field2":"90;1;Não",
       "field3":"obrigado!;419;R$ 0",
       "field4":"00;01/09/2024;Escolha os sabores da sua pizza :;R$ 21.977",
       "field5":"90"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":"2;Pizza Artesanal Italiana | Grande;Calabresa | Clássica;168;39;R$ 2.609",
       "field2":"10;2;Calabresa;150;R$ 5.050",
       "field3":"95;01/09/2024;Calabresa | Clássica;R$ 2.609",
       "field4":"10"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":"3;Bebidas;Coca-Cola Zero 2l;40;37;R$ 518",
       "field2":"00;3;Cream Chicken | Frango com cream cheese",
       "field3":"bacon e Catupiry;111;R$ 4.267",
       "field4":"95;01/09/2024;Coca-Cola Zero 2l;R$ 518",
       "field5":"00"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":"4;Imperdíveis + Guaraná Antarctica;Especial 2 sabores | 1 pizza 2 sabores grande + 1 Guaraná Antarctica 2l;120;32;R$ 2.428",
       "field2":"80;4;Sim",
       "field3":"copos e guardanapos!;89;R$ 0",
       "field4":"00;01/09/2024;Especial 2 sabores | 1 pizza 2 sabores grande + 1 Guaraná Antarctica 2l;R$ 2.428",
       "field5":"80"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":"5;Pizza Italiana;Calabresa;60;26;R$ 1.739",
       "field2":"40;5;Portuguesa;74;R$ 2.586",
       "field3":"30;01/09/2024;Calabresa;R$ 1.739",
       "field4":"40"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":"1;Pizza Grande | 2 sabores;Escolha os sabores da sua pizza :;734;342;R$ 24.249",
       "field2":"30;1;Kit Grátis;293;R$ 0",
       "field3":"00;01/10/2024;Escolha os sabores da sua pizza :;R$ 24.249",
       "field4":"30"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":"2;Pizza Italiana;Calabresa;254;73;R$ 4.888",
       "field2":"70;2;Não",
       "field3":"obrigado!;245;R$ 0",
       "field4":"00;01/10/2024;Calabresa;R$ 4.888",
       "field5":"70"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":"3;Pizza Italiana;Cream Chicken;147;49;R$ 3.870",
       "field2":"10;3;Calabresa;167;R$ 5.586",
       "field3":"15;01/10/2024;Cream Chicken;R$ 3.870",
       "field4":"10"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":"4;Bebidas;Coca-Cola Original 2l;52;32;R$ 448",
       "field2":"00;4;Cream Chicken | Frango com cream cheese",
       "field3":"bacon e Catupiry;122;R$ 4.810",
       "field4":"90;01/10/2024;Coca-Cola Original 2l;R$ 448",
       "field5":"00"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":"5;Bebidas;Coca-Cola Zero 2l;16;22;R$ 308",
       "field2":"00;5;Frango com Catupiry Clássica | Nova receita;76;R$ 2.732",
       "field3":"20;01/10/2024;Coca-Cola Zero 2l;R$ 308",
       "field4":"00"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":"1;Pizza Grande | 2 sabores;Escolha os sabores da sua pizza :;995;419;R$ 29.895",
       "field2":"10;1;Kit Grátis;471;R$ 0",
       "field3":"00;01/11/2024;Escolha os sabores da sua pizza :;R$ 29.895",
       "field4":"10"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":"2;Pizza Artesanal Italiana | 8 Fatias;Calabresa;305;77;R$ 5.156",
       "field2":"30;2;Calabresa;210;R$ 7.024",
       "field3":"50;01/11/2024;Calabresa;R$ 5.156",
       "field4":"30"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":"3;Pizza Artesanal Italiana | 8 Fatias;Cream Chicken;165;47;R$ 3.757",
       "field2":"80;3;Cream Chicken | Frango com cream cheese",
       "field3":"bacon e Catupiry;166;R$ 6.631",
       "field4":"70;01/11/2024;Cream Chicken;R$ 3.757",
       "field5":"80"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":"4;Bebidas;Coca-Cola Sem Açúcar 2l;26;43;R$ 602",
       "field2":"00;4;Não",
       "field3":"obrigado!;166;R$ 0",
       "field4":"00;01/11/2024;Coca-Cola Sem Açúcar 2l;R$ 602",
       "field5":"00"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":"5;Bebidas;Refrigerante Guaraná Antarctica 2l;31;31;R$ 372",
       "field2":"00;5;Frango com Catupiry Clássica | Nova receita;104;R$ 3.738",
       "field3":"80;01/11/2024;Refrigerante Guaraná Antarctica 2l;R$ 372",
       "field4":"00"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":";;;;;;;;;;;Não",
       "field2":"obrigado!;R$ 0",
       "field3":"00"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":";;;;;;;;;;;Calabresa;R$ 5.050",
       "field2":"95"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":";;;;;;;;;;;Cream Chicken | Frango com cream cheese",
       "field2":"bacon e Catupiry;R$ 4.267",
       "field3":"95"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":";;;;;;;;;;;Sim",
       "field2":"copos e guardanapos!;R$ 0",
       "field3":"00"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":";;;;;;;;;;;Portuguesa;R$ 2.586",
       "field2":"30"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":";;;;;;;;;;;Kit Grátis;R$ 0",
       "field2":"00"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":";;;;;;;;;;;Não",
       "field2":"obrigado!;R$ 0",
       "field3":"00"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":";;;;;;;;;;;Calabresa;R$ 5.586",
       "field2":"15"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":";;;;;;;;;;;Cream Chicken | Frango com cream cheese",
       "field2":"bacon e Catupiry;R$ 4.810",
       "field3":"90"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":";;;;;;;;;;;Frango com Catupiry Clássica | Nova receita;R$ 2.732",
       "field2":"20"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":";;;;;;;;;;;Kit Grátis;R$ 0",
       "field2":"00"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":";;;;;;;;;;;Calabresa;R$ 7.024",
       "field2":"50"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":";;;;;;;;;;;Cream Chicken | Frango com cream cheese",
       "field2":"bacon e Catupiry;R$ 6.631",
       "field3":"70"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":";;;;;;;;;;;Não",
       "field2":"obrigado!;R$ 0",
       "field3":"00"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Visitas;Vendas;Total vendas;Posição no ranking Complemento;Nome do item Complemento;Vendas Complemento;Total vendas Complemento;Data;Nome do item completo;Total vendas Completo":";;;;;;;;;;;Frango com Catupiry Clássica | Nova receita;R$ 3.738",
       "field2":"80"
    }
 ]

            ],
    "COMPLEMENTO_MENOS_VENDIDO": [
[
    {
        "Posiçãonoranking": "1",
        "Categoria": "Obrigatório",
        "Nomedoitem": "Molho extra",
        "Vendas": "22",
        "Totalvendas": "R$ 55,00"
    },
    {
        "Posiçãonoranking": "2",
        "Categoria": "Obrigatório",
        "Nomedoitem": "Mozzarela Especial | Duplo queijo",
        "Vendas": "45",
        "Totalvendas": "R$ 1.482,75"
    },
    {
        "Posiçãonoranking": "3",
        "Categoria": "Obrigatório",
        "Nomedoitem": "Quattro Formaggi | Quatro queijos",
        "Vendas": "45",
        "Totalvendas": "R$ 1.955,25"
    },
    {
        "Posiçãonoranking": "4",
        "Categoria": "Obrigatório",
        "Nomedoitem": "Arrabbiatta | Calabresa picante com bacon",
        "Vendas": "52",
        "Totalvendas": "R$ 1.869,40"
    },
    {
        "Posiçãonoranking": "5",
        "Categoria": "Obrigatório",
        "Nomedoitem": "Pepperoni",
        "Vendas": "56",
        "Totalvendas": "R$ 1.957,20"
    }
]

                ],
    "DIAS_MAIS_VENDAS": [

        [
    {"Dia da semana;Pedidos;Data":"Seg;1;01/09/2024"},
    {"Dia da semana;Pedidos;Data":"Ter;32;01/09/2024"},
    {"Dia da semana;Pedidos;Data":"Qua;54;01/09/2024"},
    {"Dia da semana;Pedidos;Data":"Qui;50;01/09/2024"},
    {"Dia da semana;Pedidos;Data":"Sex;72;01/09/2024"},
    {"Dia da semana;Pedidos;Data":"Sáb;95;01/09/2024"}
    ,
    {"Dia da semana;Pedidos;Data":"Dom;160;01/09/2024"},
    {"Dia da semana;Pedidos;Data":"Seg;0;01/10/2024"},
    {"Dia da semana;Pedidos;Data":"Ter;53;02/10/2024"},
    {"Dia da semana;Pedidos;Data":"Qua;40;03/10/2024"},
    {"Dia da semana;Pedidos;Data":"Qui;73;04/10/2024"},
    {"Dia da semana;Pedidos;Data":"Sex;110;05/10/2024"},
    {"Dia da semana;Pedidos;Data":"Sáb;119;06/10/2024"}
    ,
    {"Dia da semana;Pedidos;Data":"Dom;119;07/10/2024"},
    {"Dia da semana;Pedidos;Data":"Seg;0;07/11/2024"},
    {"Dia da semana;Pedidos;Data":"Ter;49;08/11/2024"},
    {"Dia da semana;Pedidos;Data":"Qua;68;09/11/2024"},
    {"Dia da semana;Pedidos;Data":"Qui;72;10/11/2024"},
    {"Dia da semana;Pedidos;Data":"Sex;144;11/11/2024"},
    {"Dia da semana;Pedidos;Data":"Sáb;145;12/11/2024"}
    ,
    {"Dia da semana;Pedidos;Data":"Dom;125;13/11/2024"},
    {"Dia da semana;Pedidos;Data":";;"},
    {"Dia da semana;Pedidos;Data":";;"},
    {"Dia da semana;Pedidos;Data":";;"},
    {"Dia da semana;Pedidos;Data":";;"},
    {"Dia da semana;Pedidos;Data":";;"},
    {"Dia da semana;Pedidos;Data":";;"},
    {"Dia da semana;Pedidos;Data":";;"},
    {"Dia da semana;Pedidos;Data":";;"},
    {"Dia da semana;Pedidos;Data":";;"},
    {"Dia da semana;Pedidos;Data":";;"},
    {"Dia da semana;Pedidos;Data":";;"},
    {"Dia da semana;Pedidos;Data":";;"},
    {"Dia da semana;Pedidos;Data":";;"},
    {"Dia da semana;Pedidos;Data":";;"},
    {"Dia da semana;Pedidos;Data":";;"}
    ]
    ],
    
    "SABOR_MAIS_VENDIDO": [

        [
    {
        "Posiçãonoranking": "1",
        "Categoria": "Opcional",
        "Nomedoitem": "Kit Grátis",
        "Vendas": "1",
        "Totalvendas": "R$ 0,00"
    },
    {
        "Posiçãonoranking": "2",
        "Categoria": "Opcional",
        "Nomedoitem": "Não, obrigado!",
        "Vendas": "1",
        "Totalvendas": "R$ 0,00"
    },
    {
        "Posiçãonoranking": "3",
        "Categoria": "Opcional",
        "Nomedoitem": "Sim, copos e guardanapos!",
        "Vendas": "2",
        "Totalvendas": "R$ 0,00"
    },
    {
        "Posiçãonoranking": "4",
        "Categoria": "Obrigatório",
        "Nomedoitem": "Molho extra",
        "Vendas": "13",
        "Totalvendas": "R$ 32,50"
    },
    {
        "Posiçãonoranking": "5",
        "Categoria": "Obrigatório",
        "Nomedoitem": "Sim, copos e guardanapos!",
        "Vendas": "22",
        "Totalvendas": "R$ 0,00"
    }
]

    ],
    
    "CARDAPIO_MAIS_VENDIDO": [

        [
    {
        "Posiçãonoranking": "1",
        "Categoria": "Imperdíveis + Guaraná Antarctica",
        "Nomedoitem": "Especial 2 sabores | 1 pizza 2 sabores grande + 1 Guaraná Antarctica 2l",
        "Visitas": "18",
        "Vendas": "3",
        "Totalvendas": "R$ 227,70"
    },
    {
        "Posiçãonoranking": "2",
        "Categoria": "Promo Porto",
        "Nomedoitem": "Pizza em dobro | 2 pizzas grandes + 1 Coca-Cola 1,5l grátis",
        "Visitas": "12",
        "Vendas": "4",
        "Totalvendas": "R$ 554,10"
    },
    {
        "Posiçãonoranking": "3",
        "Categoria": "Promo Porto",
        "Nomedoitem": "Combo Clássico | 1 pizza grande + 1 Refrigerante 2 l",
        "Visitas": "88",
        "Vendas": "5",
        "Totalvendas": "R$ 329,50"
    },
    {
        "Posiçãonoranking": "4",
        "Categoria": "Promo Porto",
        "Nomedoitem": "Combo Irresistível | 1 pizza grande + 1 Coca-Cola de 1,5",
        "Visitas": "42",
        "Vendas": "5",
        "Totalvendas": "R$ 329,50"
    },
    {
        "Posiçãonoranking": "5",
        "Categoria": "Pizza Italiana",
        "Nomedoitem": "Quattro Formaggi",
        "Visitas": "22",
        "Vendas": "8",
        "Totalvendas": "R$ 698,20"
    }
]
    ],
    "PEDIDOS_CLIENTES_OUT": [

        [
    {
        "Etapa": "Visitas",
        "Quantidade": "3534",
        "Percentualcomparativoaoperíodoanterior": "+5,9%",
        "Percentualatual": "+100%",
        "Percentualanterior": "+100%"
    },
    {
        "Etapa": "Visualizações",
        "Quantidade": "1325",
        "Percentualcomparativoaoperíodoanterior": "+12,57%",
        "Percentualatual": "+37,49%",
        "Percentualanterior": "+35,27%"
    },
    {
        "Etapa": "Revisão",
        "Quantidade": "759",
        "Percentualcomparativoaoperíodoanterior": "+1,07%",
        "Percentualatual": "+21,48%",
        "Percentualanterior": "+22,51%"
    },
    {
        "Etapa": "Sacola",
        "Quantidade": "773",
        "Percentualcomparativoaoperíodoanterior": "+2,25%",
        "Percentualatual": "+21,87%",
        "Percentualanterior": "+22,66%"
    },
    {
        "Etapa": "Concluídos",
        "Quantidade": "514",
        "Percentualcomparativoaoperíodoanterior": "+10,78%",
        "Percentualatual": "+14,54%",
        "Percentualanterior": "+13,9%"
    }
]
    ],
    
    "PEDIDO_CLIENTES_SET": [

        [
    {
        "Etapa": "Visitas",
        "Quantidade": "3337",
        "Percentualcomparativoaoperíodoanterior": "-21,06%",
        "Percentualatual": "+100%",
        "Percentualanterior": "+100%"
    },
    {
        "Etapa": "Visualizações",
        "Quantidade": "1177",
        "Percentualcomparativoaoperíodoanterior": "-24,5%",
        "Percentualatual": "+35,27%",
        "Percentualanterior": "+36,88%"
    },
    {
        "Etapa": "Revisão",
        "Quantidade": "751",
        "Percentualcomparativoaoperíodoanterior": "-19,25%",
        "Percentualatual": "+22,51%",
        "Percentualanterior": "+22%"
    },
    {
        "Etapa": "Sacola",
        "Quantidade": "756",
        "Percentualcomparativoaoperíodoanterior": "-19,49%",
        "Percentualatual": "+22,66%",
        "Percentualanterior": "+22,21%"
    },
    {
        "Etapa": "Concluídos",
        "Quantidade": "464",
        "Percentualcomparativoaoperíodoanterior": "-20,27%",
        "Percentualatual": "+13,9%",
        "Percentualanterior": "+13,77%"
    }
]
    ],


    "PIZZA_VENDIDA_DOIS_SABORES": [

        [
    {
        "Posiçãonoranking": "1",
        "Categoria": "Obrigatório",
        "Nomedoitem": "Mozzarela Especial | Duplo queijo",
        "Vendas": "38",
        "Totalvendas": "R$ 1.265,55"
    },
    {
        "Posiçãonoranking": "2",
        "Categoria": "Obrigatório",
        "Nomedoitem": "Quattro Formaggi | Quatro queijos",
        "Vendas": "40",
        "Totalvendas": "R$ 1.758,00"
    },
    {
        "Posiçãonoranking": "3",
        "Categoria": "Obrigatório",
        "Nomedoitem": "Pepperoni",
        "Vendas": "42",
        "Totalvendas": "R$ 1.530,90"
    },
    {
        "Posiçãonoranking": "4",
        "Categoria": "Obrigatório",
        "Nomedoitem": "Arrabbiatta | Calabresa picante com bacon",
        "Vendas": "51",
        "Totalvendas": "R$ 1.756,95"
    },
    {
        "Posiçãonoranking": "5",
        "Categoria": "Obrigatório",
        "Nomedoitem": "Frango com Catupiry Clássica | Nova receita",
        "Vendas": "55",
        "Totalvendas": "R$ 1.977,25"
    }
]
    ],
    
    "MAIS_VENDIDOS_OUT": [
	
	[
    {
        "Posiçãonoranking": "1",
        "Categoria": "Pizza Artesanal Italiana | Grande",
        "Nomedoitem": "Quattro Formaggi | Quatro queijos",
        "Visitas": "3",
        "Vendas": "1",
        "Totalvendas": "R$ 87,90"
    },
    {
        "Posiçãonoranking": "2",
        "Categoria": "Pizza Italiana",
        "Nomedoitem": "Quattro Formaggi",
        "Visitas": "14",
        "Vendas": "2",
        "Totalvendas": "R$ 175,80"
    },
    {
        "Posiçãonoranking": "3",
        "Categoria": "Pizza Italiana",
        "Nomedoitem": "Frango com Catupiry",
        "Visitas": "5",
        "Vendas": "2",
        "Totalvendas": "R$ 143,80"
    },
    {
        "Posiçãonoranking": "4",
        "Categoria": "Pizza Italiana",
        "Nomedoitem": "Mozzarela",
        "Visitas": "6",
        "Vendas": "2",
        "Totalvendas": "R$ 129,80"
    },
    {
        "Posiçãonoranking": "5",
        "Categoria": "Imperdíveis + Guaraná Antarctica",
        "Nomedoitem": "Pizza Margherita + Guaraná Antarctica 2 l",
        "Visitas": "11",
        "Vendas": "4",
        "Totalvendas": "R$ 267,60"
    }
]

    ],
    
    "HORARIO_MAIS_VENDA": [
   
        [
    {"Horário;Pedidos;Mês":"00:00 - 02:00;1;01/09/2024"}
    ,
    {"Horário;Pedidos;Mês":"02:00 - 04:00;0;01/09/2024"}
    ,
    {"Horário;Pedidos;Mês":"04:00 - 06:00;0;01/09/2024"}
    ,
    {"Horário;Pedidos;Mês":"06:00 - 08:00;0;01/09/2024"}
    ,
    {"Horário;Pedidos;Mês":"08:00 - 10:00;0;01/09/2024"}
    ,
    {"Horário;Pedidos;Mês":"10:00 - 12:00;0;01/09/2024"}
    ,
    {"Horário;Pedidos;Mês":"12:00 - 14:00;0;01/09/2024"}
    ,
    {"Horário;Pedidos;Mês":"14:00 - 16:00;0;01/09/2024"}
    ,
    {"Horário;Pedidos;Mês":"16:00 - 18:00;0;01/09/2024"}
    ,
    {"Horário;Pedidos;Mês":"18:00 - 20:00;49;01/09/2024"}
    ,
    {"Horário;Pedidos;Mês":"20:00 - 22:00;62;01/09/2024"}
    ,
    {"Horário;Pedidos;Mês":"22:00 - 00:00;25;01/09/2024"}
    ,
    {"Horário;Pedidos;Mês":"00:00 - 02:00;0;01/10/2024"}
    ,
    {"Horário;Pedidos;Mês":"02:00 - 04:00;0;01/10/2024"}
    ,
    {"Horário;Pedidos;Mês":"04:00 - 06:00;0;01/10/2024"}
    ,
    {"Horário;Pedidos;Mês":"06:00 - 08:00;0;01/10/2024"}
    ,
    {"Horário;Pedidos;Mês":"08:00 - 10:00;0;01/10/2024"}
    ,
    {"Horário;Pedidos;Mês":"10:00 - 12:00;0;01/10/2024"}
    ,
    {"Horário;Pedidos;Mês":"12:00 - 14:00;0;01/10/2024"}
    ,
    {"Horário;Pedidos;Mês":"14:00 - 16:00;0;01/10/2024"}
    ,
    {"Horário;Pedidos;Mês":"16:00 - 18:00;0;01/10/2024"}
    ,
    {"Horário;Pedidos;Mês":"18:00 - 20:00;68;01/10/2024"}
    ,
    {"Horário;Pedidos;Mês":"20:00 - 22:00;76;01/10/2024"}
    ,
    {"Horário;Pedidos;Mês":"22:00 - 00:00;22;01/10/2024"}
    ,
    {"Horário;Pedidos;Mês":"00:00 - 02:00;0;01/11/2024"}
    ,
    {"Horário;Pedidos;Mês":"02:00 - 04:00;0;01/11/2024"}
    ,
    {"Horário;Pedidos;Mês":"04:00 - 06:00;0;01/11/2024"}
    ,
    {"Horário;Pedidos;Mês":"06:00 - 08:00;0;01/11/2024"}
    ,
    {"Horário;Pedidos;Mês":"08:00 - 10:00;0;01/11/2024"}
    ,
    {"Horário;Pedidos;Mês":"10:00 - 12:00;0;01/11/2024"}
    ,
    {"Horário;Pedidos;Mês":"12:00 - 14:00;0;01/11/2024"}
    ,
    {"Horário;Pedidos;Mês":"14:00 - 16:00;0;01/11/2024"}
    ,
    {"Horário;Pedidos;Mês":"16:00 - 18:00;1;01/11/2024"}
    ,
    {"Horário;Pedidos;Mês":"18:00 - 20:00;63;01/11/2024"}
    ,
    {"Horário;Pedidos;Mês":"20:00 - 22:00;94;01/11/2024"}
    ,
    {"Horário;Pedidos;Mês":"22:00 - 00:00;31;01/11/2024"}
    
    ]
    ],
    
    "MENOS_VENDIDO_3MESES": [
        [
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"1;Obrigatório;Mozzarela Especial | Duplo queijo;38;R$ 1.265",
       "field2":"55;01/09/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"2;Obrigatório;Quattro Formaggi | Quatro queijos;40;R$ 1.758",
       "field2":"00;02/09/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"3;Obrigatório;Pepperoni;42;R$ 1.530",
       "field2":"90;03/09/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"4;Obrigatório;Arrabbiatta | Calabresa picante com bacon;51;R$ 1.756",
       "field2":"95;04/09/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"5;Obrigatório;Frango com Catupiry Clássica | Nova receita;55;R$ 1.977",
       "field2":"25;05/09/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"1;Pizza Artesanal Italiana | Grande;Quattro Formaggi | Quatro queijos;1;R$ 87",
       "field2":"90;06/09/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"2;Pizza Italiana;Quattro Formaggi;2;R$ 175",
       "field2":"80;07/09/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"3;Pizza Italiana;Frango com Catupiry;2;R$ 143",
       "field2":"80;08/09/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"4;Pizza Italiana;Mozzarela;2;R$ 129",
       "field2":"80;09/09/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"5;Imperdíveis + Guaraná Antarctica;Pizza Margherita + Guaraná Antarctica 2 l;4;R$ 267",
       "field2":"60;10/09/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"1;Opcional;Kit Grátis;1;R$ 0",
       "field2":"00;01/10/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"2;Opcional;Não",
       "field2":"obrigado!;1;R$ 0",
       "field3":"00;02/10/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"3;Opcional;Sim",
       "field2":"copos e guardanapos!;2;R$ 0",
       "field3":"00;03/10/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"4;Obrigatório;Molho extra;13;R$ 32",
       "field2":"50;04/10/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"5;Obrigatório;Sim",
       "field2":"copos e guardanapos!;22;R$ 0",
       "field3":"00;05/10/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"1;Imperdíveis + Guaraná Antarctica;Especial 2 sabores | 1 pizza 2 sabores grande + 1 Guaraná Antarctica 2l;3;R$ 227",
       "field2":"70;06/10/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"2;Promo Porto;Pizza em dobro | 2 pizzas grandes + 1 Coca-Cola 1",
       "field2":"5l grátis;4;R$ 554",
       "field3":"10;07/10/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"3;Promo Porto;Combo Clássico | 1 pizza grande + 1 Refrigerante 2 l;5;R$ 329",
       "field2":"50;08/10/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"4;Promo Porto;Combo Irresistível | 1 pizza grande + 1 Coca-Cola de 1",
       "field2":"5;5;R$ 329",
       "field3":"50;09/10/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"5;Pizza Italiana;Quattro Formaggi;8;R$ 698",
       "field2":"20;10/10/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"1;Promo Porto;Combo Irresistível | 1 pizza grande + 1 Coca-Cola de 1",
       "field2":"5;1;R$ 65",
       "field3":"90;01/11/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"2;Pizza Artesanal Italiana | 8 Fatias;Quattro Formaggi;3;R$ 260",
       "field2":"70;02/11/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"3;Promo Porto;Pizza em dobro | 2 pizzas grandes + 1 Coca-Cola 1",
       "field2":"5l grátis;5;R$ 692",
       "field3":"00;03/11/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"4;Pizza Artesanal Italiana | 8 Fatias;Mozzarela;7;R$ 461",
       "field2":"30;04/11/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"5;Pizza Artesanal Italiana | 8 Fatias;Margherita;10;R$ 599",
       "field2":"00;05/11/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"1;Obrigatório;Molho extra;22;R$ 55",
       "field2":"00;06/11/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"2;Obrigatório;Mozzarela Especial | Duplo queijo;45;R$ 1.482",
       "field2":"75;07/11/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"3;Obrigatório;Quattro Formaggi | Quatro queijos;45;R$ 1.955",
       "field2":"25;08/11/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"4;Obrigatório;Arrabbiatta | Calabresa picante com bacon;52;R$ 1.869",
       "field2":"40;09/11/2024"
    },
    {
       "Posição no ranking;Categoria;Nome do item;Vendas;Total vendas;Mês":"5;Obrigatório;Pepperoni;56;R$ 1.957",
       "field2":"20;10/11/2024"
    }
 ]
    ],
    
    
    "TOTAL_VENDA_3MESES": [
   	[
    {
       "Total de vendas realizadas;Valor total das vendas;Ticket médio;Novos clientes;Mês":"464;R$ 38.822",
       "field2":"14;R$ 83",
       "field3":"67;127;01/09/2024"
    },
    {
       "Total de vendas realizadas;Valor total das vendas;Ticket médio;Novos clientes;Mês":"514;R$ 42.515",
       "field2":"08;R$ 82",
       "field3":"71;132;01/10/2024"
    },
    {
       "Total de vendas realizadas;Valor total das vendas;Ticket médio;Novos clientes;Mês":"603;R$ 48.080",
       "field2":"07;R$ 79",
       "field3":"73;179;01/11/2024"
    },
    {
       "Total de vendas realizadas;Valor total das vendas;Ticket médio;Novos clientes;Mês":";;;;"
    },
    {
       "Total de vendas realizadas;Valor total das vendas;Ticket médio;Novos clientes;Mês":";;;;"
    }
 ]
    ]
}

dados = {nome: pd.DataFrame(conteudo) for nome, conteudo in dados_incorporados.items()}

# Inicializa Flask
app = Flask(__name__)

# Função auxiliar para criar tokens
def criar_token(username):
    return jwt.encode(
        {"sub": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET_KEY,
        algorithm='HS256'
    )

# Rota padrão para gerar token(autenticação básica)
@app.route('/')
def home():
    auth_data = request.authorization
    if not auth_data or not auth_data.username or not auth_data.password:
        return jsonify({"erro": "Usuário ou senha não fornecidos no cabeçalho Authorization"}), 401

    username = auth_data.username
    password = auth_data.password

    if username in USERS and USERS[username] == password:
        token = criar_token(username)
        return jsonify({
            "token": token,
            "rota_para_dados": "/dados"
        })

    return jsonify({"erro": "Usuário ou senha inválidos"}), 401


@app.route('/auth', methods=['POST'])
def gerar_token():
    if not request.is_json:  
        return jsonify({"erro": "O corpo da requisição precisa estar em JSON"}), 400

    auth_data = request.get_json()
    username = auth_data.get("user")
    password = auth_data.get("password")

    if not username or not password:
        return jsonify({"erro": "Campos 'user' e 'password' são obrigatórios"}), 400

    if username in USERS and USERS[username] == password:
        token = criar_token(username)
        return jsonify({
            "token": token,
            "rota_para_dados": "/dados"
        })

    return jsonify({"erro": "Usuário ou senha inválidos"}), 401

# Rota protegida para acessar os dados
@app.route('/dados', methods=['GET'])
def obter_dados():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"erro": "Token não fornecido no cabeçalho 'Authorization'"}), 401

    try:
        
        if token.startswith("Bearer "):
            token = token.split(" ")[1]

        jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({"erro": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"erro": "Token inválido"}), 401

    dados_combinados = pd.concat(dados.values(), ignore_index=True)
    return jsonify(dados_combinados.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
