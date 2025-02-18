import pygal
import json
from urllib.request import urlopen # python 3 syntax


from flask import Flask
from pygal.style import DarkSolarizedStyle

app = Flask(__name__)

#----------------------------------------------------------------------
@app.route('/')
def get_weather_data(date='20140415', state='IA', city='Ames'):
    """
    Date must be in YYYYMMDD
    """
    api_key = 'API_KEY'
    url = 'http://api.wunderground.com/api/{key}/history_{date}/q/{state}/{city}.json'
    new_url = url.format(key=api_key,
                         date=date,
                         state=state,
                         city=city)
    result = urlopen(new_url)
    js_string = result.read()
    parsed = json.loads(js_string)
    history = parsed['history']['observations']

    imp_temps = [float(i['tempi']) for i in history]
    times = ['%s:%s' % (i['utcdate']['hour'], i['utcdate']['min']) for i in history]

    # create a bar chart
    title = 'Temps for %s, %s on %s' % (city, state, date)
    bar_chart = pygal.Bar(width=1200, height=600,
                          explicit_size=True, title=title, style=DarkSolarizedStyle)
    #bar_chart = pygal.StackedLine(width=1200, height=600,
    #                      explicit_size=True, title=title, fill=True)

    bar_chart.x_labels = times
    bar_chart.add('Temps in F', imp_temps)

    html = """
        <html>
             <head>
                  <title>%s</title>
             </head>
              <body>
                 %s
             </body>
        </html>
        """ % (title, bar_chart.render())
    return html


#----------------------------------------------------------------------
if __name__ == '__main__':
    app.run()
