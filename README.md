# RentInsight 🏠📊

**Análise e previsão de preços de aluguel em Lisboa**  
Este projeto é um estudo prático e iterativo de Ciência de Dados aplicado ao mercado imobiliário da cidade de Lisboa, com foco em imóveis residenciais para aluguel.  
---
## 💡 Objetivo
Desenvolver um pipeline completo de dados — desde a coleta e limpeza até a visualização e modelagem — com foco em:
- Entender a distribuição de imóveis disponíveis para alugar por bairro
- Identificar regiões com maior oferta
- Criar modelos preditivos de valor de aluguel com base em atributos do imóvel e localização
---
## 📁 Estrutura de Pastas
	rentinsight/
	├── data/ # Dados brutos e tratados
	│ ├── raw/ # (vazio por ora)
	│ ├── processed/ # (vazio por ora)
	│ └── imoveis_lisboa_pronto.csv # dataset principal limpo
	├── notebooks/ # notebooks Jupyter
	├── reports/ # gráficos e visualizações exportadas
	├── src/ # código modular (futuro)
	├── requirements.txt # bibliotecas usadas
	└── README.md # este arquivo
---
## 🧠 O que foi feito até agora
### ✅ Conquistas
- 🔍 **Limpeza robusta dos dados**:
  - Tipos convertidos corretamente (números, categorias, booleanos)
  - Preenchimento de campos ausentes com valores medianos (quando apropriado)
  - Remoção de registros incompletos
- 📊 **Visualizações informativas**:
  - **Heatmap por bairro** usando `seaborn`, com cor proporcional à quantidade de imóveis
  - **Gráfico de barras empilhadas** por tipo de imóvel (T0, T1, T2...) para cada bairro
- 📦 **Dataset tratado**:
  - 2.000 imóveis prontos para modelagem
  - Dados como `rooms`, `area_m2`, `property_type`, `furnished`, `dist_metro_m`, entre outros
---
## ⚠️ Tentativas que foram descartadas

- ❌ **Integração com API da OLX**:
  - Acesso inicial por token funcionou
  - Mas endpoints `/locations` e `/adverts` retornavam erros (400/404)
  - Testamos com latitude, longitude, postalCode, cityId e districtId sem sucesso confiável
  - Decidimos abandonar a API por instabilidade, limitações e tempo de debug
---
## 📈 Próximos passos (em aberto)
- [ ] Engenharia de features (ex: criar `price_per_m2`, `is_furnished`, etc.)
- [ ] Modelagem preditiva (regressão linear, árvore de decisão, etc.)
- [ ] Deploy de um modelo simples (ex: via Streamlit ou Flask)
- [ ] Dashboard final com insights por bairro
---
🗂️ Fontes dos Dados Imobiliários — Lisboa (.csv de 2.000 imóveis)

    Idealista.pt
        📅 Coletado em: 11/05/2025
        📊 Contribuição: 72% dos registros (~1.440 imóveis)
        📝 Inclui: preço, tipologia, área, andar, bairro, mobiliado (quando disponível)
    Imovirtual.com
        📅 Coletado em: 11/05/2025
        📊 Contribuição: 20% dos registros (~400 imóveis)
        📝 Inclui: preço, tipologia, bairro, mobiliado
    Casa Sapo (supersite.pt)
        📅 Coletado em: 11/05/2025
        📊 Contribuição: 8% dos registros (~160 imóveis)
        📝 Inclui: área, idade do prédio, distância ao metrô (estimada a partir da localização)
