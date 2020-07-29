def formata_data(data):
    data_split = str(data).split('-')
    data_formatada = data_split[2] + '/' + data_split[1] + '/' + data_split[0]

    return data_formatada