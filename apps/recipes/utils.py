from io import BytesIO 
import base64
import matplotlib.pyplot as plt

def get_graph():
  buffer = BytesIO()
  plt.savefig(buffer, format='png')
  buffer.seek(0)
  image_png=buffer.getvalue()
  graph=base64.b64encode(image_png)
  graph=graph.decode('utf-8')
  buffer.close()
  return graph

def get_chart(chart_type, data, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(6, 3))
    
    x_label = kwargs.get('x_label', '')
    y_label = kwargs.get('y_label', '')

    if chart_type == '#1':
        plt.bar(data['name'], data['cooking_time'])
        plt.xlabel(x_label)
        plt.ylabel(y_label)

    elif chart_type == '#2':
        labels = kwargs.get('labels')
        plt.pie(data['cooking_time'], labels=labels)
        plt.ylabel(y_label)

    elif chart_type == '#3':
        plt.plot(data['cooking_time'], data['difficulty'])
        plt.xlabel('Cooking Time (minutes)') 
        plt.ylabel('Difficulty') 
    else:
        print('unknown chart type')

    plt.tight_layout()
    chart = get_graph()
    
    return chart