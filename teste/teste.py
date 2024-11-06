import threading
import time

def play_bot():
    
    def Começar_bot():
        from selenium import webdriver
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        from selenium.webdriver.edge.service import Service
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import WebDriverWait
        import json

        servico = Service(EdgeChromiumDriverManager().install())
        options = webdriver.EdgeOptions()
        options.add_argument("--incognito")
        # options.add_argument("--headless")

        def AbrirNav(url):
            global navegador
            navegador = webdriver.Edge(service=servico, options=options)
            navegador.get(url)
        def definir_tamanho():
            navegador.set_window_size(1024, 768)

        global links_antigos
        links_antigos = ["Nulo"]

        global pagina
        pagina = 0
        
        global novos_carro
        novos_carro = []

        while True:
            pagina = pagina + 1

            AbrirNav(f'https://www.nettiauto.com/uusimmat?posted_by=seller&page={pagina}')
            WebDriverWait(navegador, 10)

            global links
            links = []

            for num in range(1,35):
                definir_tamanho()
                try:
                    elemento = navegador.find_element(By.XPATH, f'//*[@id="listingData"]/div[1]/div[{num}]/a')
                    link_carros = elemento.get_attribute('href')
                    links.append(link_carros)
                    
                except:
                    continue
            navegador.quit()

            if links == links_antigos[0]:
                pagina = 0
                break
            else:
                links_antigos.clear()

            links_antigos.append(links)

            time.sleep(1)

            for link in links:
                AbrirNav(link)

                WebDriverWait(navegador, 10)
                time.sleep(1)
                navegador.execute_script("window.scrollBy(0, 1200);")
                navegador.set_window_size(1300, 768)
                time.sleep(1)


                # vendedor
                try:
                    nome_dono = navegador.find_element(By.XPATH, '//*[@id="slideEffect"]/div[19]/div/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div').text
                except:
                    try:
                        nome_dono = navegador.find_element(By.XPATH, '//*[@id="slideEffect"]/div[19]/div/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div').text
                    except:
                        nome_dono = "Não encontrado"

                # Modelo do carro
                try:
                    nome_carro = navegador.find_element(By.XPATH, '//*[@id="slideEffect"]/div[20]/div/div[1]/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/h1').text
                except:
                    try:
                        nome_carro = navegador.find_element(By.XPATH, '//*[@id="slideEffect"]/div[19]/div/div[1]/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/h1').text
                    except:
                        nome_carro = "Não encontrado"

                # preço do carro
                try:
                    preco_carro = navegador.find_element(By.XPATH, '//*[@id="slideEffect"]/div[20]/div/div[1]/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/div/font').text
                except:
                    try:
                        preco_carro = navegador.find_element(By.XPATH, '//*[@id="slideEffect"]/div[19]/div/div[1]/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/div').text
                    except:
                        preco_carro = "Não encontrado"

                # numero de telefone
                try:
                    valor = navegador.find_element(By.XPATH, '//*[@id="showUserNumber"]/span')
                    valor.click()
                except:
                    valor = "Não encontrado"

                # Quilometragem
                try:
                    Quilometragem_carro = navegador.find_element(By.XPATH, '//*[@id="slideEffect"]/div[20]/div/div[1]/div[2]/div[1]/div[4]/div/div[3]/div/div[1]/div[2]').text
                except:
                    try:
                        Quilometragem_carro = navegador.find_element(By.XPATH, '//*[@id="slideEffect"]/div[19]/div/div[1]/div[2]/div[1]/div[4]/div/div[3]/div/div[1]/div[2]').text
                    except:
                        Quilometragem_carro = "Não encontrado"

                # Ano
                try:
                    ano_carro = navegador.find_element(By.XPATH, '//*[@id="slideEffect"]/div[20]/div/div[1]/div[2]/div[1]/div[4]/div/div[3]/div/div[3]/div[2]').text
                except:
                    try:
                        ano_carro = navegador.find_element(By.XPATH, '//*[@id="slideEffect"]/div[19]/div/div[1]/div[2]/div[1]/div[4]/div/div[3]/div/div[3]/div[2]').text
                    except:
                        ano_carro = "Não encontrado"
                
                # Motor
                try:
                    motor_carro = navegador.find_element(By.XPATH, '//*[@id="slideEffect"]/div[20]/div/div[1]/div[2]/div[1]/div[4]/div/div[3]/div/div[2]/div[2]').text
                except:
                    try:
                        motor_carro = navegador.find_element(By.XPATH, '//*[@id="slideEffect"]/div[19]/div/div[1]/div[2]/div[1]/div[4]/div/div[3]/div/div[2]/div[2]').text
                    except:
                        motor_carro = "Não encontrado"

                # Cambio
                try:
                    cambio_carro = navegador.find_element(By.XPATH, '//*[@id="slideEffect"]/div[20]/div/div[1]/div[2]/div[1]/div[4]/div/div[3]/div/div[4]/div[2]').text
                except:
                    try:
                        cambio_carro = navegador.find_element(By.XPATH, '//*[@id="slideEffect"]/div[19]/div/div[1]/div[2]/div[1]/div[4]/div/div[3]/div/div[4]/div[2]').text
                    except:
                        cambio_carro = "Não encontrado"


                if type(valor) == str:

                    print(f'\033[1;32m \n Nome: {nome_carro} \n Preço: {preco_carro} \n Contato: {valor} \n Quilometragem: {Quilometragem_carro} \n Ano: {ano_carro} \n Motor: {motor_carro} \n Câmbio: {cambio_carro} \n \033[m')

                else:

                    print(f'\033[1;32m \n Nome: {nome_carro} \n Preço: {preco_carro} \n Contato: {valor.text} \n Quilometragem: {Quilometragem_carro} \n Ano: {ano_carro} \n Motor: {motor_carro} \n Câmbio: {cambio_carro} \n \033[m')

                    DADOS_carro = {
                        "nome": nome_carro,
                        "preço": preco_carro,
                        "contato": valor.text,
                        "quilometragem": Quilometragem_carro,
                        "ano": ano_carro,
                        "motor": motor_carro,
                        "câmbio": cambio_carro
                    }
                    
                    try:
                        with open('./teste/fones.json', 'r') as file:
                            dados_carros = json.load(file)

                    except:
                        dados_carros = []

                    if DADOS_carro in novos_carro:
                        pass
                    else:
                        novos_carro.append(DADOS_carro)
                    
                    if DADOS_carro in dados_carros:
                        pass
                    else:
                        dados_carros.append(DADOS_carro)
                              
                    with open('./teste/fones.json', 'w') as file:
                        json.dump(dados_carros, file, ensure_ascii=False, indent=4)


                navegador.quit()

        with open('./teste/fones.json', 'w') as file:
            json.dump(novos_carro, file, ensure_ascii=False, indent=4)

        '''
            AbrirNav('https://api.whatsapp.com/send?phone=')

            telefones = []
            with open('fones.txt', 'r') as arquivo:
                for linha in arquivo:
                    # Remove espaços em branco, colchetes e apóstrofos
                    telefone = linha.strip().replace('[', '').replace(']', '').replace("'", "").replace('+', '').replace('-', '')
                    telefones.append(telefone)

            for telefone in telefones:
                try:
                    navegador.get(f'https://api.whatsapp.com/send?phone={telefone}')
                    WebDriverWait(navegador, 10)
                    navegador.find_element(By.XPATH, '//*[@id="action-button"]').click()
                    time.sleep(2)
                    navegador.find_element(By.XPATH, '//*[@id="fallback_block"]/div/div/h4[2]/a/span').click()

                    wait = WebDriverWait(navegador, 200)
                    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p')))

                    navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p').send_keys("ok" + Keys.RETURN)
                    time.sleep(1)
                except:
                    continue
        '''
    while True:
        Começar_bot()

        time.sleep(7200)

thread1 = threading.Thread(target=play_bot)
thread1.start()