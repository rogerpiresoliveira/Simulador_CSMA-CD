# Simulador CSMA/CD

Este projeto é um simulador de rede que demonstra o funcionamento do protocolo CSMA/CD (Carrier Sense Multiple Access with Collision Detection) utilizando uma interface gráfica Tkinter. Ele permite configurar vários parâmetros da rede e visualizar o processo de transmissão, detecção de colisões e retransmissões.

-----

## Funcionalidades

  * **Configuração de Parâmetros:** Ajuste o número de transmissores, quadros por transmissor, largura de banda, comprimento do cabo, fator de velocidade do cabo e número máximo de retransmissões.
  * **Simulação Interativa:** Acompanhe a simulação em tempo real, com logs detalhados sobre as transmissões, colisões e retransmissões.
  * **Estatísticas Finais:** Visualize estatísticas ao final da simulação, incluindo o número total de quadros enviados, colisões e a média de tentativas por quadro.

-----

## Como Usar

1.  **Pré-requisitos:** Certifique-se de ter o Python 3 instalado em seu sistema.

2.  **Executar o Simulador:**
    Salve o código fornecido em um arquivo Python (por exemplo, `csmacd_simulator.py`) e execute-o a partir do terminal:

    ```bash
    python csmacd_simulator.py
    ```

3.  **Configurar a Simulação:**
    Na janela do simulador, insira os valores desejados para os seguintes parâmetros:

      * **Number of Transmitters:** Quantos dispositivos tentarão enviar dados.
      * **Frames per Transmitter:** Quantos quadros cada transmissor tentará enviar.
      * **Bandwidth (Mbps):** A largura de banda da rede em Megabits por segundo.
      * **Cable Length (meters):** O comprimento físico do cabo da rede em metros.
      * **Cable Speed Factor (0.6 - 0.7):** Um fator que representa a velocidade de propagação do sinal no cabo em relação à velocidade da luz (geralmente entre 0.6 e 0.7).
      * **Max Retransmissions:** O número máximo de tentativas antes que um quadro seja descartado após colisões.

4.  **Iniciar a Simulação:**
    Clique no botão "**Start Simulation**" para iniciar o processo. Os logs da simulação aparecerão na área de texto abaixo.

-----

## Detalhes do Código

O simulador é composto por:

  * **`Transmitter` Class:** Representa um dispositivo na rede, com um ID e um contador de quadros a serem enviados e tentativas de retransmissão.
  * **Funções de Cálculo:**
      * `calculate_propagation_delay`: Calcula o atraso de propagação do sinal.
      * `calculate_slot_time`: Calcula o tempo de slot (duas vezes o atraso de propagação).
      * `transmission_time`: Calcula o tempo necessário para transmitir um quadro.
      * `generate_frame_size`: Gera tamanhos de quadros aleatórios dentro de limites definidos.
  * **`CSMACDSimulator` Class (Tkinter GUI):**
      * Configura a interface gráfica (entradas de dados, botão de início, área de log).
      * Valida as entradas do usuário.
      * Inicia a simulação em uma thread separada para não travar a interface.
  * **`simulate` Method:**
      * Contém a lógica principal da simulação CSMA/CD.
      * Utiliza uma fila de eventos para gerenciar as tentativas de transmissão dos transmissores.
      * Simula a detecção de portadora, colisões e o algoritmo de backoff exponencial binário para retransmissões.
      * Registra eventos e estatísticas na interface.

-----

## Conceitos de CSMA/CD

  * **Carrier Sense (Detecção de Portadora):** Um dispositivo ouve o meio de transmissão antes de enviar dados para verificar se está ocupado.
  * **Multiple Access (Acesso Múltiplo):** Múltiplos dispositivos podem acessar o mesmo meio de transmissão.
  * **Collision Detection (Detecção de Colisão):** Durante a transmissão, o dispositivo continua a ouvir o meio para detectar se outro dispositivo começou a transmitir simultaneamente, causando uma colisão.
  * **Backoff Exponencial Binário:** Após uma colisão, os dispositivos esperam um tempo aleatório antes de tentar retransmitir, com o tempo máximo de espera aumentando exponencialmente a cada colisão subsequente para reduzir a probabilidade de novas colisões.
  * **Slot Time:** O tempo mínimo para que uma colisão seja detectada em toda a rede.

-----
