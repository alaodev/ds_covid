import json
from app import app, mysql, charts
from app.models.casos_dao import CasosDao
from app.helpers.data import formata_data
from app.helpers.soma import somatorio
from flask import render_template, request, redirect
from flask_googlecharts import BarChart, ColumnChart, AreaChart, ComboChart, GeoChart, PieChart

dao = CasosDao(mysql)

area_chart = AreaChart("area_chart", options={'title': 'Casos de COVID-19', 'height': 400, 'colors':['#81d4fa', ]})
area_chart.add_column("string", "Data")
area_chart.add_column("number", "Casos")

pie_chart = PieChart("pie_chart", options={'title': 'Relação de Casos Confirmados/Mortes', 'height': 325, 'colors':['#007BFF', '#004691']})
pie_chart.add_column("string", "Data")
pie_chart.add_column("number", "Casos")

pie_chart_uf = PieChart("pie_chart_uf", options={'title': 'Confirmados por Estado - Filtrado por Data', 'height': 325, 'colors':['#007BFF', '#0079FA', '#0076F5', '#0074F0', '#0071EB', '#006FE6', '#006CE0', '#006ADB', '#0068D6', '#0065D1', '#0060C7', '#005EC2', '#00A0F0', '#005EC2', '#005BBD', '#0059B8', '#0056B3', '#0054AD', '#0051A8', '#004FA3','#004C9E', '#0BC4DB', '#004A99', '#004794', '#00458F', '#00438A', '#004085']})
pie_chart_uf.add_column("string", "Data")
pie_chart_uf.add_column("number", "Casos")

@app.route('/')
def graficos():
    # Registra os gráficos.
    charts.register(area_chart)
    charts.register(pie_chart)
    charts.register(pie_chart_uf)
    # Buscas no Banco e conversões.
    casos = dao.busca_dados() # <----------------------Apresentação.
    confirmados_uf = dao.confirmados_uf('')
    confirmados_uf_desc = dao.confirmados_uf_desc('')
    intervalo_pesquisas = [[dado[0], formata_data(dado[1]), formata_data(dado[2])] for dado in dao.intervalo_pesquisas()]
    mapa_confirmados = [['País', 'Confirmados']]
    for dado in confirmados_uf:
        mapa_confirmados.append([dado[0], int(dado[1])])

    # Renderizando o template.
    return render_template(
        'graficos.html',
        titulo = 'Covid-19 - Análise Gráfica',
        css = 'graficos.css',
        casos = casos, # <----------------------Apresentação.
        mapa_confirmados = json.dumps(mapa_confirmados),
        confirmados_uf_desc = confirmados_uf_desc,
        total = somatorio(confirmados_uf_desc),
        uf = 'UF',
        data_inicial = 'Data Inicial',
        data_final = 'Data Final',
        intervalo_pesquisas = intervalo_pesquisas
    )

@app.route('/atualiza', methods=['GET', 'POST', ])
def atualiza():
    uf = request.form['select_uf']
    data_inicial = request.form['data_inicial']
    data_final = request.form['data_final']
    min_max = dao.min_max(uf)
    if data_inicial == '' and data_final == '':
        data_inicial = min_max[0]
        data_final = min_max[1]
        casos = dao.filtra_uf(uf)
        confirmados_mortes = dao.confirmados_mortes_uf(uf)
    else:
        casos = dao.filtra_dados(uf, data_inicial, data_final)
        confirmados_mortes = dao.confirmados_mortes(uf, data_final)
    confirmados_uf = dao.confirmados_uf(data_final)
    confirmados_uf_desc = dao.confirmados_uf_desc(data_final)
    intervalo_pesquisas = [[dado[0], formata_data(dado[1]), formata_data(dado[2])] for dado in dao.intervalo_pesquisas()]
    frequencia_area = [[dado.data,int(dado.confirmados)] for dado in casos]
    frequencia_pie = [['Confirmados', int(confirmados_mortes[0])],['Mortes', int(confirmados_mortes[1])]]
    mapa_confirmados = [['País', 'Confirmados']]
    for dado in confirmados_uf:
        mapa_confirmados.append([dado[0], int(dado[1])])
    pie_confirmados = [[dado[0], int(dado[1])] for dado in confirmados_uf]
    # Registra gráficos.
    charts.register(area_chart)
    charts.register(pie_chart)
    charts.register(pie_chart_uf)
    # Limpa conteúdo existênte nos gráficos.
    area_chart._rows.clear()
    pie_chart._rows.clear()
    pie_chart_uf._rows.clear()
    # Atualiza os gráficos.
    area_chart.add_rows(frequencia_area)
    pie_chart.add_rows(frequencia_pie)
    pie_chart_uf.add_rows(pie_confirmados)

    return render_template(
        'graficos.html',
        titulo = 'Covid-19 - Análise Gráfica',
        css = 'graficos.css',
        casos = casos,
        data_min = formata_data(min_max[0]),
        data_max = formata_data(min_max[1]),
        mapa_confirmados = json.dumps(mapa_confirmados),
        confirmados_uf_desc = confirmados_uf_desc,
        total = somatorio(confirmados_uf_desc),
        uf = uf,
        data_inicial = formata_data(data_inicial),
        data_final = formata_data(data_final),
        intervalo_pesquisas = intervalo_pesquisas
    )