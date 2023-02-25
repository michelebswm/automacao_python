### Pegando Blogs HashTag Treinamentos
# Criando um navegador
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Criando o navegador
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)

# Abrindo o link
navegador.get('https://www.hashtagtreinamentos.com/')
time.sleep(2)  # Esperar carregar

# Esperar o PopUp aparecer na tela
elemento = WebDriverWait(navegador, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "eicon-close")))
time.sleep(1)  # Espera o PopUp carregar totalmente na tela
elemento.click()

# Pegando a lista de links da classe nav-link
links = navegador.find_elements(By.CLASS_NAME, 'nav-link')
# print(links)
for link in links:
    #print(link.text)
    if 'blog' in link.text.lower():  # transformando o nome do link em minusculo para comparar
        link_inicial = link.get_attribute('href')
        link.click()  # Abrindo o link do Blog localizado
        break
#### Pegando o Assunto e o link de cada artigo
lista_assunto = []
lista_link = []
i = 1
while navegador.find_elements(By.CLASS_NAME, 'cont'):
    list_artigos = navegador.find_elements(By.CLASS_NAME, 'cont')  # Localizando tag que possui os links
    # print(list_artigos)

    for artigo in list_artigos:
        assuntos = artigo.find_elements(By.TAG_NAME, 'h4')  # para cada artigo quero pegar a tag h4 que é o assunto
        links = artigo.find_elements(By.TAG_NAME, 'a')  # para cada artigo quero pegar a tag a
        for assunto in assuntos:
            if assunto.text is None:
                lista_assunto.append('None')
            lista_assunto.append(assunto.text)
        for link in links:
            if link.get_attribute('href') is None:
                lista_link.append('None')
            lista_link.append(link.get_attribute('href'))  # para cada link quero pegar o link


    i += 1
    pages = link_inicial + f'/page/{i}'
    navegador.get(pages)
# Fechar o navegador
navegador.quit()


time.sleep(2)
# Validação para criar um Dataframe as listas devem ter o mesmo tamanho
tamanho_assunto = len(lista_assunto)
tamanho_link = len(lista_link)

if tamanho_assunto < tamanho_link:
    lista_assunto = lista_assunto + [None] * (len(lista_link) - len(lista_assunto))
else:
    lista_link = lista_link + [None] * (len(lista_assunto) - len(lista_link))

dic_blogs = {
    'assunto': lista_assunto,
    'link_blog': lista_link
}
print(dic_blogs)

# Exportar para csv/excel
df = pd.DataFrame(dic_blogs)
df.to_excel('Blogs Hashtag.xlsx', index=False)
print('Arquivo exportado com sucesso!')