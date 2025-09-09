# 🚧 Controle de Insumos das Obras
Este projeto é uma aplicação interativa desenvolvida em **Streamlit** para controlar, cadastrar e analisar insumos utilizados em obras.  
O sistema permite registrar entradas, exportar relatórios em Excel e visualizar indicadores e gráficos dinâmicos.

## 🎯 Objetivo
O objetivo deste sistema é padronizar os registros de controle dos caminhões que chegam às obras com insumos, uma vez que antes cada obra realizava esse processo de forma diferente.
Com a aplicação, os dados ficam centralizados, organizados e disponíveis em relatórios e análises visuais.

## 🛠️ Funcionalidades
- 📥 **Cadastro de lançamentos** com informações sobre obra, CR responsável, motorista, material, quantidade, ticket/nota, etc.  
- 📅 **Filtros por período e CR** para análises específicas.  
- 📊 **Painel de monitoramento** com:
  - Total de carradas
  - Quantidade total
  - Número de registros
  - Gráficos interativos (por CR, por material e por motorista)
- ⬇️ **Exportação de dados filtrados ou completos** em formato Excel.  
- 🎨 Interface amigável e responsiva feita no **Streamlit** com gráficos do **Plotly Express**.

## 📦 Dependências
- Python 3.9+
- Streamlit
- Pandas
- Plotly
- OpenPyXL (para salvar/exportar Excel)

## 📌Instalar as Bibliotecas
pip install streamlit pandas plotly openpyxl
