def save_output_as_html(text):
    f = open('sample.html','w',encoding='utf-8')
    f.write(text)
    f.close()