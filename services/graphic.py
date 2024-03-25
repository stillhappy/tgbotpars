import plotly.graph_objects as go
import json
from services.watermarka import add_watermark_overlay
from datetime import datetime, timedelta
import io

async def plot_coefficientss(data, match: str, bk: str, game: str, difference):
    tour_name, team1, team2, params, bet_name = match.split('_')
    fig = go.Figure()
    for i in range(len(data)):
        data[i][0] = [float(j) for j in data[i][0].split(' ')]
    # Разделение данных на два списка
    coef1 = [item[0][0] for item in data]
    coef2 = [item[0][1] for item in data]
    dates = [item[1] for item in data]
    name1, name2 = team1, team2
    if 'Тотал Б' in bet_name:
        name1 = bet_name.lstrip('Тотал ')
        name2 = bet_name.replace('Б', 'М').lstrip('Тотал ')
    elif 'Тотал' in bet_name:
        name1 = f"Б {bet_name.lstrip('Тотал ')}"
        name2 = f"М {bet_name.lstrip('Тотал ')}"
    elif '(Odd/Even)' in bet_name:
        name1 = 'Odd'
        name2 = 'Even'
    elif 'Фора' in bet_name:
        name1 = f"{team1} {bet_name.lstrip('Фора 1 ').replace(')', '').replace('(', '')}"
        if '+' in bet_name or '-' not in bet_name:
            name2 = f"{team2} -{bet_name.lstrip('Фора 1 ').replace(')', '').replace('(', '').replace('+', '')}"
        else:
            name2 = f"{team2} {bet_name.lstrip('Фора 1 ').replace(')', '').replace('(', '').replace('-', '+')}"


    # Создание двух линий на графике
    trace1 = go.Scatter(x=dates, y=coef1, mode='lines+markers', name=name1, line_color='red', line_shape='linear')
    trace2 = go.Scatter(x=dates, y=coef2, mode='lines+markers', name=name2, line_color='green', line_shape='linear')
    fig.add_trace(trace1)
    fig.add_trace(trace2)

    fig.update_layout(
        title=f"<b>{team1} - {team2}. {params}: {bet_name}</b>",
        xaxis_title='<b>Время</b>',
        yaxis_title='<b>Коэффициенты</b>',
        showlegend=True,
        plot_bgcolor='white',
        title_font_color='black',  # Цвет заголовка
        xaxis_title_font_color='black',  # Цвет заголовка оси X
        yaxis_title_font_color='black',  # Цвет заголовка оси Y
        font_color='black'  # Цвет текста легенды
    )
    if difference != 'parser':
        file_name = f"photos/{bk.lower()}_{game.lower()}_{round(difference, 2)}_({coef1[-1]}-{coef2[-1]})_({coef1[-2]}-{coef2[-2]})_{tour_name}_{team1}_{team2}.png"
        fig.write_image(file_name)  # Сохранение графика в формате PNG
        add_watermark_overlay(file_name, file_name, 'https://t.me/futurebets')
    else:
        file_name = f"photosparser/{game}{params}{bet_name}.png"
        fig.write_image(file_name)
        add_watermark_overlay(file_name, file_name, 'https://t.me/futurebets')
        return file_name

def plot_coefficients(data, match: str, bk: str, game: str, difference):
    tour_name, team1, team2, params, bet_name = match.split('_')
    fig = go.Figure()
    for i in range(len(data)):
        data[i][0] = [float(j) for j in data[i][0].split(' ')]
    # Разделение данных на два списка
    coef1 = [item[0][0] for item in data]
    coef2 = [item[0][1] for item in data]
    dates = [item[1] for item in data]
    name1, name2 = team1, team2
    if 'Тотал Б' in bet_name:
        name1 = bet_name.lstrip('Тотал ')
        name2 = bet_name.replace('Б', 'М').lstrip('Тотал ')
    elif 'Тотал' in bet_name:
        name1 = f"Б {bet_name.lstrip('Тотал ')}"
        name2 = f"М {bet_name.lstrip('Тотал ')}"
    elif '(Odd/Even)' in bet_name:
        name1 = 'Odd'
        name2 = 'Even'
    elif 'Фора' in bet_name:
        name1 = f"{team1} {bet_name.lstrip('Фора 1 ').replace(')', '').replace('(', '')}"
        if '+' in bet_name or '-' not in bet_name:
            name2 = f"{team2} -{bet_name.lstrip('Фора 1 ').replace(')', '').replace('(', '').replace('+', '')}"
        else:
            name2 = f"{team2} {bet_name.lstrip('Фора 1 ').replace(')', '').replace('(', '').replace('-', '+')}"


    # Создание двух линий на графике
    trace1 = go.Scatter(x=dates, y=coef1, mode='lines+markers', name=name1, line_color='red', line_shape='linear')
    trace2 = go.Scatter(x=dates, y=coef2, mode='lines+markers', name=name2, line_color='green', line_shape='linear')
    fig.add_trace(trace1)
    fig.add_trace(trace2)

    fig.update_layout(
        title=f"<b>{team1} - {team2}. {params}: {bet_name}</b>",
        xaxis_title='<b>Время</b>',
        yaxis_title='<b>Коэффициенты</b>',
        showlegend=True,
        plot_bgcolor='white',
        title_font_color='black',  # Цвет заголовка
        xaxis_title_font_color='black',  # Цвет заголовка оси X
        yaxis_title_font_color='black',  # Цвет заголовка оси Y
        font_color='black'  # Цвет текста легенды
    )
    if difference != 'parser':
        file_name = f"photos/{bk.lower()}_{game.lower()}_{round(difference, 2)}_({coef1[-1]}-{coef2[-1]})_({coef1[-2]}-{coef2[-2]})_{tour_name}_{team1}_{team2}.png"
        fig.write_image(file_name)  # Сохранение графика в формате PNG
        add_watermark_overlay(file_name, file_name, 'https://t.me/futurebets')
    else:
        file_name = f"photosparser/{game}{params}{bet_name}.png"
        fig.write_image(file_name)
        add_watermark_overlay(file_name, file_name, 'https://t.me/futurebets')
        return file_name

def get_data_for_graph():
    with open('output.json', 'r') as file:
        data = json.load(file)
    now_str = datetime.now().strftime('%m-%d %H:%M')
    date_format = '%m-%d %H:%M'
    initial_date = datetime.strptime(now_str, date_format)
    updated_date = initial_date + timedelta(hours=3)
    five_minutes_ago = updated_date - timedelta(minutes=3)
    five_minutes_later = updated_date + timedelta(minutes=3)
    for bk in data:
        for game in data[bk]:
            for match in data[bk][game]:
                if len(data[bk][game][match]) >= 2:
                    date_request_last = datetime.strptime(data[bk][game][match][-1][1], '%m-%d %H:%M')
                    if five_minutes_later >= date_request_last >= five_minutes_ago:
                        cofs_new = [float(kof) for kof in data[bk][game][match][-1][0].split(' ')]
                        cofs_old = [float(kof) for kof in data[bk][game][match][-2][0].split(' ')]
                        difference = abs(cofs_new[cofs_old.index(min(cofs_old))] - min(cofs_old))
                        if difference >= 0.05:
                            plot_coefficients(data[bk][game][match], match, bk, game, difference)

if __name__ == '__main__':
    data = [['1.5 2.5', '03-23 2:20'], ['1.75 1.95', '03-23 2:40'], ['1.95 1.75', '03-23 2:50']]
    match = 'blast_Infinity_Akatsuki_Общая_Исходы'
    bk = 'fonbet'
    game = 'counter-strike'
    difference = 0.1
    plot_coefficients(data, match, bk, game, difference)

